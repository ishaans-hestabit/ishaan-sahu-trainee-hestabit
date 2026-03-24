from langchain_community.vectorstores import FAISS
from pathlib import Path

def create_vectorstore(texts, metadatas, vectors, embedding_model):

    vectorstore = FAISS.from_embeddings(
        text_embeddings=list(zip(texts, vectors)),
        metadatas=metadatas,
        embedding=embedding_model,
    )
    return vectorstore


def save_vectorstore(vectorstore, path : Path):
    vectorstore.save_local(str(path))  


def load_vectorstore(path: Path, embedding_model):
    """
    Load FAISS index from disk.
    """
    return FAISS.load_local(
        str(path),
        embedding_model,
        allow_dangerous_deserialization=True
    )