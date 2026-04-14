from rank_bm25 import BM25Okapi
import pickle
import re


def tokenize(text: str) -> list:
    return re.findall(r'[a-z0-9]+', text.lower())

def build_bm25_index(chunks, output_dir):
    texts = [chunk.page_content for chunk in chunks]

    tokenized = [tokenize(text) for text in texts]

    bm25 = BM25Okapi(tokenized)

    data = {
        "index" : bm25,
        "texts" : texts,
        "metadatas" : [chunk.metadata for chunk in chunks]
    }

    with open(output_dir / "bm25_index.pkl", "wb") as f:
        pickle.dump(data, f)

    print(f"BM25 index built with {len(texts)} chunks")

    

def load_bm25_data(vectorstore_dir):
    with open(vectorstore_dir / "bm25_index.pkl", "rb") as f:
        bm25_data = pickle.load(f)

    return bm25_data