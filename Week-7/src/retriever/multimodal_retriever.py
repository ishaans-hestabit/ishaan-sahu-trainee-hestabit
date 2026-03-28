import os
from pathlib import Path
from PIL import Image

from pipelines.image_ingest import run_ocr, run_caption
from retriever.hybrid_retriever import load_indexes, hybrid_retrieve
from retriever.reranker import rerank
from retriever.image_search import _search as image_faiss_search
from embeddings.clip_embedder import CLIPEmbedder
from pipelines.context_builder import build_context

VECTORSTORE_DIR = Path("vectorstore")
clip = CLIPEmbedder()

def _get_image_results(query_vector: list, n: int = 3) -> list:
    try:
        return image_faiss_search(query_vector, n)
    except FileNotFoundError:
        print("  [Image] No image index found — skipping image retrieval.")
        return []


def _image_to_text_description(image_path: str) -> str:
    
    image = Image.open(image_path).convert("RGB")

    caption  = run_caption(image)
    ocr_text = run_ocr(image)

    parts = [caption]
    if ocr_text:
        parts.append(ocr_text)

    combined = " ".join(parts).strip()
    print(f"  [Image→Text query] '{combined[:100]}...'")
    return combined


def _build_combined_context(text_results: list, image_results: list) -> str:
    parts = []

    if text_results:
        text_ctx = build_context("", text_results)
        parts.append("=== TEXT CONTEXT ===\n" + text_ctx["context_string"])

    if image_results:
        img_lines = ["=== IMAGE CONTEXT ==="]
        for i, r in enumerate(image_results, 1):

            src = f"[PDF p.{r['page_num']}]" if r.get("source_type") == "pdf_page" else "[IMG]"

            img_lines.append(f"\n[Image {i}] {src} {r['filename']}  (similarity={r['similarity']})")
            img_lines.append(f"  Caption : {r['caption']}")
            
            if r.get("ocr_text"):
                ocr = r["ocr_text"][:300] + ("..." if len(r["ocr_text"]) > 300 else "")
                img_lines.append(f"  OCR text: {ocr}")
        parts.append("\n".join(img_lines))

    return "\n\n" + ("\n\n" + "─" * 50 + "\n\n").join(parts)


def retrieve_from_text(query: str, top_k_text: int = 5, top_k_images: int = 3) -> dict:
    
    print(f"\n{'='*55}")
    print(f"[Multimodal Retrieve — TEXT] '{query}'")
    print(f"{'='*55}")

    print("\nHybrid text retrieval (FAISS + BM25 + RRF)...")
    vectorstore, bm25_data = load_indexes(VECTORSTORE_DIR)
    raw_results = hybrid_retrieve(query, vectorstore, bm25_data, top_k=top_k_text * 2)

    print("Reranking text results...")
    text_results = rerank(query, raw_results, top_k=top_k_text)

    print("Image retrieval via CLIP text embedding...")
    query_vector  = clip.embed_text(query)
    image_results = _get_image_results(query_vector, n=top_k_images)

    context = _build_combined_context(text_results, image_results)

    text_ctx = build_context(query, text_results) if text_results else {"sources": []}

    print(f"\n[Done] text={len(text_results)} chunks, images={len(image_results)}")

    return {
        "query_type"   : "text",
        "query"        : query,
        "text_results" : text_results,
        "image_results": image_results,
        "context"      : context,
        "sources"      : text_ctx.get("sources", [])
    }


def retrieve_from_image(image_path: str, top_k_text: int = 5, top_k_images: int = 3) -> dict:

    print(f"\n{'='*55}")
    print(f"[Multimodal Retrieve — IMAGE] '{os.path.basename(image_path)}'")
    print(f"{'='*55}")

    print("\nVisual similarity search (CLIP image embedding)...")
    query_image  = Image.open(image_path).convert("RGB")
    query_vector = clip.embed_image(query_image)
    image_results = _get_image_results(query_vector, n=top_k_images)

    print("Converting image to text description for text retrieval...")
    text_query = _image_to_text_description(image_path)

    print("Hybrid text retrieval using image description...")
    text_results = []
    try:
        vectorstore, bm25_data = load_indexes(VECTORSTORE_DIR)
        raw_results  = hybrid_retrieve(text_query, vectorstore, bm25_data, top_k=top_k_text * 2)
        text_results = rerank(text_query, raw_results, top_k=top_k_text)
    except Exception as e:
        print(f"[Text] Retrieval failed: {e}")

    context = _build_combined_context(text_results, image_results)
    text_ctx = build_context(text_query, text_results) if text_results else {"sources": []}

    print(f"\n[Done] text={len(text_results)} chunks, images={len(image_results)}")
    return {
        "query_type"    : "image",
        "query"         : image_path,
        "derived_query" : text_query,
        "text_results"  : text_results,
        "image_results" : image_results,
        "context"       : context,
        "sources"       : text_ctx.get("sources", [])
    }

def retrieve(query: str, top_k_text: int = 5, top_k_images: int = 3) -> dict:
   
    supported_img_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff'}
    ext = Path(query).suffix.lower()

    if ext in supported_img_exts and os.path.exists(query):
        return retrieve_from_image(query, top_k_text, top_k_images)
    else:
        return retrieve_from_text(query, top_k_text, top_k_images)