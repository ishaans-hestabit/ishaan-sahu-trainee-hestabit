import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

VECTOR_FILE = "memory/vectors.index"
TEXT_FILE = "memory/vectors_text.json"
DIMENSION = 384

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
texts = []

def load():
    global index, texts
    if index is not None:
        return  
    if os.path.exists(VECTOR_FILE) and os.path.exists(TEXT_FILE):
        index = faiss.read_index(VECTOR_FILE)
        with open(TEXT_FILE, "r") as f:
            texts = json.load(f)
    else:
        index = faiss.IndexFlatL2(DIMENSION)
        texts = []

def save():
    os.makedirs(os.path.dirname(VECTOR_FILE), exist_ok=True)
    faiss.write_index(index, VECTOR_FILE)
    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f)

def add_to_vector_store(text):
    load()
    vector = np.array(model.encode([text])).astype("float32")
    index.add(vector)
    texts.append(text)
    save()

def search_vector_store(query, top_k=3):
    load()
    if index.ntotal == 0:
        return []
    vector = np.array(model.encode([query])).astype("float32")
    distances, indices = index.search(vector, min(top_k, index.ntotal))
    return [texts[i] for i in indices[0] if i != -1]