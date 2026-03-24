from pathlib import Path
from vectorstore.store import load_vectorstore
from embeddings.embedder import get_embedding_model

TOP_K = 4


def load_retriever(vectorstore_dir: Path):
    print("Loading vectorstore...")

    embedding_model = get_embedding_model()

    vectorstore = load_vectorstore(vectorstore_dir, embedding_model)

    print(f"  Vectorstore loaded from {vectorstore_dir}")
    return vectorstore


def retrieve(query: str, vectorstore, top_k: int = TOP_K) -> list:

    results = vectorstore.similarity_search(query, k=top_k)

    return results


def display_results(query: str, results: list):

    print(f"\n── Query: '{query}' ──")
    print(f"── Top {len(results)} results ──\n")

    for i, doc in enumerate(results):
        print(f"Result {i+1}")
        print(f"  source : {doc.metadata.get('source', 'unknown')}")
        print(f"  page   : {doc.metadata.get('page', '?')}")
        print(f"  preview: {doc.page_content}")
        print()


if __name__ == "__main__":
    from pathlib import Path

    VECTORSTORE_DIR = Path("vectorstore")

    vectorstore = load_retriever(VECTORSTORE_DIR)

    test_queries = [
        
        "What is the email of Andrew?"
    ]

    for query in test_queries:
        results = retrieve(query, vectorstore)
        display_results(query, results)