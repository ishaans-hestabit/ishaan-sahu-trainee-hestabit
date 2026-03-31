import os
from pathlib import Path
from PIL import Image

from pipelines.image_ingest import run_ocr, run_caption
from retriever.hybrid_retriever import load_indexes, hybrid_retrieve
from retriever.reranker import rerank
from retriever.image_search import _search as image_faiss_search
from embeddings.clip_embedder import CLIPEmbedder
from pipelines.context_builder import build_context

VECTORSTORE_DIR    = Path("vectorstore")
SUPPORTED_IMG_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff'}

_clip = None

def get_clip():
    global _clip
    if _clip is None:
        _clip = CLIPEmbedder()
    return _clip


def _search_images(query_vector, query_text, n):
    if n <= 0:
        return []
    try:
       
        return image_faiss_search(query_vector, n=n, query_text=query_text)
    except FileNotFoundError:
        return []



def _image_to_text(image_path):
    image    = Image.open(image_path).convert("RGB")
    caption  = run_caption(image)
    ocr_text = run_ocr(image)
    return (caption + " " + ocr_text).strip() if ocr_text else caption



def _build_context(text_results, image_results):
    parts = []

    if text_results:
        ctx = build_context("", text_results)
        parts.append("=== TEXT CONTEXT ===\n" + ctx["context_string"])


    if image_results:
        lines = ["=== IMAGE CONTEXT ==="]

        for i, r in enumerate(image_results, 1):

            src = f"[PDF p.{r['page_num']}]" if r.get("source_type") == "pdf_page" else "[IMG]"
            lines.append(f"\n[Image {i}] {src} {r['filename']} (similarity={r['similarity']})")
            lines.append(f"  Caption : {r['caption']}")
            
            if r.get("ocr_text"):
                lines.append(f"  OCR text: {r['ocr_text'][:300]}")
        parts.append("\n".join(lines))

    return "\n\n" + ("\n\n" + "─" * 50 + "\n\n").join(parts)




def _text_retrieve(query, top_k):

    vectorstore, bm25_data = load_indexes(VECTORSTORE_DIR)

    raw = hybrid_retrieve(query, vectorstore, bm25_data, top_k=top_k * 2)

    return rerank(query, raw, top_k=top_k)



def retrieve_from_text(query, top_k_text=5, top_k_images=3):

    text_results  = _text_retrieve(query, top_k_text) if top_k_text > 0 else []

    query_vector  = get_clip().embed_text(query)

    image_results = _search_images(query_vector, query_text=query, n=top_k_images)

    context       = _build_context(text_results, image_results)

    sources       = build_context(query, text_results)["sources"] if text_results else []


    return {
        "query_type"   : "text",
        "query"        : query,
        "text_results" : text_results,
        "image_results": image_results,
        "context"      : context,
        "sources"      : sources
    }


def retrieve_from_image(image_path, top_k_text=5, top_k_images=3):

    query_image   = Image.open(image_path).convert("RGB")

    query_vector  = get_clip().embed_image(query_image)

    text_query    = _image_to_text(image_path)

    image_results = _search_images(query_vector, query_text=text_query, n=top_k_images)
    
    text_results  = []

    if top_k_text > 0:
        try:
            text_results = _text_retrieve(text_query, top_k_text)
        except Exception as e:
            print(f"[Text retrieval failed] {e}")

    context = _build_context(text_results, image_results)

    sources = build_context(text_query, text_results)["sources"] if text_results else []

    return {
        "query_type"    : "image",
        "query"         : image_path,
        "derived_query" : text_query,
        "text_results"  : text_results,
        "image_results" : image_results,
        "context"       : context,
        "sources"       : sources
    }

def retrieve(query, top_k_text=5, top_k_images=3):
    
    ext = Path(query).suffix.lower()

    if ext in SUPPORTED_IMG_EXTS and os.path.exists(query):
        return retrieve_from_image(query, top_k_text, top_k_images)
    
    return retrieve_from_text(query, top_k_text, top_k_images)