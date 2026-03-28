import os
import json
import numpy as np
import faiss
from PIL import Image
from embeddings.clip_embedder import CLIPEmbedder

FAISS_INDEX_PATH = "vectorstore/image_faiss.index"
METADATA_PATH    = "vectorstore/image_metadata.json"

clip = CLIPEmbedder()


def _load_index():
    try:
        return faiss.read_index(FAISS_INDEX_PATH)
    except Exception:
        raise FileNotFoundError( "Image FAISS index not found. Run image_ingest.py first.")


def _load_metadata() -> dict:
    try:
        with open(METADATA_PATH) as f:
            return json.load(f)
    except Exception:
        raise FileNotFoundError( "image_metadata.json not found. Run image_ingest.py first." )



def _search(query_vector: list, n: int = 3) -> list:
    index = _load_index()
    meta  = _load_metadata()

    if index.ntotal == 0:
        print("[Search] Index is empty — run ingest first.")
        return []

    n = min(n, index.ntotal) 
    query_np = np.array([query_vector], dtype=np.float32)  
    scores, positions = index.search(query_np, n)

    results = []
    for score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue  

        entry = meta.get(str(pos), {})
        if not entry:
            continue

        results.append({
            "image_path"  : entry.get("image_path", ""),
            "filename"    : entry.get("filename", ""),
            "caption"     : entry.get("caption", ""),
            "ocr_text"    : entry.get("ocr_text", ""),
            "source_type" : entry.get("source_type", ""),
            "source_file" : entry.get("source_file", ""),
            "page_num"    : entry.get("page_num"),
            "similarity"  : round(float(score), 4),
            "faiss_pos"   : int(pos)
        })

    return results



def text_to_image(query_text: str, n: int = 3) -> list:
    print(f"\n[Text→Image] '{query_text}'")
    vec     = clip.embed_text(query_text)

    results = _search(vec, n)

    _print_results(results)
    return results


def image_to_image(query_image_path: str, n: int = 3) -> list:

    print(f"\n[Image→Image] '{os.path.basename(query_image_path)}'")
    img = Image.open(query_image_path).convert("RGB")

    vec = clip.embed_image(img)

    results = _search(vec, n)
    _print_results(results)
    return results


def image_to_text_answer(query_image_path: str, n: int = 3) -> str:

    print(f"\n[Image→Text] '{os.path.basename(query_image_path)}'")
    results = image_to_image(query_image_path, n)

    if not results:
        return "No matching images found."

    lines = ["=== IMAGE CONTEXT ===", ""]
    for i, r in enumerate(results, 1):
        src = f"[PDF p.{r['page_num']}]" if r['source_type'] == 'pdf_page' else "[IMG]"

        lines.append(f"Match {i} {src}  similarity={r['similarity']}")
        lines.append(f"  File    : {r['filename']}")
        lines.append(f"  Caption : {r['caption']}")

        if r['ocr_text']:
            ocr = r['ocr_text'][:400] + ("..." if len(r['ocr_text']) > 400 else "")
            lines.append(f"  OCR     : {ocr}")
        lines.append("")

    return "\n".join(lines)


def _print_results(results: list):
    if not results:
        print("  No results.")
        return
    for i, r in enumerate(results, 1):
        tag = f"[PDF p.{r['page_num']}]" if r['source_type'] == 'pdf_page' else "[IMG]"
        print(f"  {i}. {tag} {r['filename']}  (sim={r['similarity']})")
        print(f"  {r['caption']}")

