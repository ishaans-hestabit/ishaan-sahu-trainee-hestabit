import os, json
import numpy as np
import faiss
from PIL import Image
from embeddings.clip_embedder import CLIPEmbedder

FAISS_INDEX_PATH = "vectorstore/image_faiss.index"
METADATA_PATH    = "vectorstore/image_metadata.json"

clip = None

def get_clip():
    global clip
    if clip is None:
        clip = CLIPEmbedder()
    return clip

def load_index():
    try:
        return faiss.read_index(FAISS_INDEX_PATH)
    except:
        raise FileNotFoundError("Image FAISS index not found. Run image_ingest.py first.")

def load_metadata():
    try:
        with open(METADATA_PATH) as f:
            return json.load(f)
    except:
        raise FileNotFoundError("image_metadata.json not found. Run image_ingest.py first.")

def keyword_score(query: str, entry: dict) -> float:
    stop_words = {"a", "an", "the", "and", "or", "but", "in", "on", "with", "to", "for", "of", "is", "are", "this", "that", "it"}
    query_words = set(w.strip('.,?!;') for w in query.lower().split()) - stop_words
    
    text = (entry.get("caption", "") + " " + entry.get("ocr_text", "")).lower()
    text_words = set(w.strip('.,?!;') for w in text.split())
    
    if not query_words:
        return 0.0
    
    matches = len(query_words.intersection(text_words))
    return matches / len(query_words)

def _search(query_vector: list, n: int = 3, query_text: str = "", is_image_query: bool = False) -> list:
    index = load_index()
    meta  = load_metadata()

    if index.ntotal == 0:
        return []

    fetch_n  = min(max(n * 3, 10), index.ntotal)
    query_np = np.array([query_vector], dtype=np.float32)
    faiss.normalize_L2(query_np)
    scores, positions = index.search(query_np, fetch_n)

    results = []
    for clip_score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue
        entry = meta.get(str(pos), {})
        if not entry:
            continue

        kw_score = keyword_score(query_text, entry) if query_text else 0.0
        
        clip_multiplier = 1.0 if is_image_query else 2.5
        adjusted_clip_score = float(clip_score) * clip_multiplier

        
        final_score = min(1.0, adjusted_clip_score + (0.15 * kw_score))

        if final_score < 0.45:
            continue

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