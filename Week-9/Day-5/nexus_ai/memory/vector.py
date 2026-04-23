import os
import sys
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from nexus_ai.config import VECTOR_FILE, TEXT_FILE, VECTOR_DIR

DIMENSION = 384


SIMILARITY_THRESHOLD = 1.2

model = None
index = None
texts = []


def get_model():
    global model
    if model is None:
        stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")
        try:
            
            model = SentenceTransformer("all-MiniLM-L6-v2")
        finally:
            sys.stderr.close()
            sys.stderr = stderr
    return model


def load():
    global index, texts
    if index is not None:
        return
    os.makedirs(VECTOR_DIR, exist_ok=True)
    if os.path.exists(VECTOR_FILE) and os.path.exists(TEXT_FILE):
        index = faiss.read_index(VECTOR_FILE)
        with open(TEXT_FILE, "r") as f:
            texts = json.load(f)
    else:
        index = faiss.IndexFlatL2(DIMENSION)
        texts = []


def save():
    os.makedirs(VECTOR_DIR, exist_ok=True)
    faiss.write_index(index, VECTOR_FILE)
    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f)


def add_to_vector_store(text):
    load()
    vector = np.array(get_model().encode([text])).astype("float32")
    index.add(vector)
    texts.append(text)
    save()


def search_vector_store(query, top_k=3):

    load()
    if index.ntotal == 0:
        return []
    vector = np.array(get_model().encode([query])).astype("float32")
    distances, indices = index.search(vector, min(top_k, index.ntotal))

    
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1 and dist < SIMILARITY_THRESHOLD:
            results.append(texts[idx])
    return results