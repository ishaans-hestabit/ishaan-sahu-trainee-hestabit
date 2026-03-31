import os, json
import numpy as np
import faiss
from PIL import Image
from embeddings.clip_embedder import CLIPEmbedder

FAISS_INDEX_PATH = "vectorstore/image_faiss.index"
METADATA_PATH    = "vectorstore/image_metadata.json"

_clip = None

def get_clip():
    global _clip
    if _clip is None:
        _clip = CLIPEmbedder()
    return _clip

def _load_index():
    try:
        return faiss.read_index(FAISS_INDEX_PATH)
    except:
        raise FileNotFoundError("Image FAISS index not found. Run image_ingest.py first.")

def _load_metadata():
    try:
        with open(METADATA_PATH) as f:
            return json.load(f)
    except:
        raise FileNotFoundError("image_metadata.json not found. Run image_ingest.py first.")

def _keyword_score(query: str, entry: dict) -> float:
    
    query_words = set(query.lower().split())
    text        = (entry.get("caption", "") + " " + entry.get("ocr_text", "")).lower()
    if not query_words:
        return 0.0
    matches = sum(1 for w in query_words if w in text)
    return matches / len(query_words)

def _search(query_vector: list, n: int = 3, query_text: str = "") -> list:
    index = _load_index()
    meta  = _load_metadata()

    if index.ntotal == 0:
        return []

   
    fetch_n  = min(max(n * 3, 10), index.ntotal)
    query_np = np.array([query_vector], dtype=np.float32)
    scores, positions = index.search(query_np, fetch_n)

    results = []
    for clip_score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue
        entry = meta.get(str(pos), {})
        if not entry:
            continue

        kw_score    = _keyword_score(query_text, entry) if query_text else 0.0
        final_score = (0.7 * float(clip_score)) + (0.3 * kw_score)

        results.append({
            "image_path"  : entry.get("image_path", ""),
            "filename"    : entry.get("filename", ""),
            "caption"     : entry.get("caption", ""),
            "ocr_text"    : entry.get("ocr_text", ""),
            "source_type" : entry.get("source_type", ""),
            "source_file" : entry.get("source_file", ""),
            "page_num"    : entry.get("page_num"),
            "similarity"  : round(final_score, 4),
            "faiss_pos"   : int(pos)
        })

    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:n]