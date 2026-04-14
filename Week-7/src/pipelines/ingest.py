import glob
from pathlib import Path
from vectorstore.bm25_store import build_bm25_index

from langchain_community.document_loaders import(
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings.embedder import get_embedding_model, generate_embeddings
from vectorstore.store import create_vectorstore,save_vectorstore

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")
CHUNKS_DIR = Path("data/chunks")
VECTORSTORE_DIR = Path("vectorstore")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

SUPPORTED_EXTENSIONS = [".pdf", ".csv", ".txt", ".docx"]

def ensure_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_DIR.mkdir(parents=True, exist_ok=True) 
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    print("Directories ready.")


def load_document(file_path: str) -> list:

   
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)

    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")

    elif ext == ".csv":
        loader = CSVLoader(file_path, encoding="utf-8")

    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)

    else:
        print(f"  Skipping unsupported file: {file_path}")
        return []   

    try:
        documents = loader.load()
    except Exception as e:
        print(f"  [ERROR] Could not load {Path(file_path).name}: {e}")
        return []
    
    for doc in documents:
        if "page" not in doc.metadata:
            doc.metadata["page"] = 0

    print(f"  Loaded {len(documents)} document(s) from {Path(file_path).name}")
    return documents


def load_all_documents() -> list:

    all_documents = []
    failed_files  = []


    for ext in SUPPORTED_EXTENSIONS:

        pattern = str(RAW_DIR / "**" / f"*{ext}")
        matched_files = glob.glob(pattern, recursive=True)

        for file_path in matched_files:
            print(f"Processing: {file_path}")

            docs = load_document(file_path)

            if not docs:
                failed_files.append(file_path)
            else:
                all_documents.extend(docs)

    print(f"\n{'─' * 50}")
    print(f"  Loaded : {len(all_documents)} document(s)")
    print(f"  Failed : {len(failed_files)} file(s)")
    if failed_files:
        print("  Failed files:")
        for f in failed_files:
            print(f"    - {f}")
    print(f"{'─' * 50}\n")

    return all_documents



def chunk_documents(documents: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
            chunk.metadata["id"] = f"chunk_{i}"

    print(f"  Chunked {len(documents)} document(s)  →  {len(chunks)} chunks")
    return chunks


def build_vector_pipeline(chunks, output_dir : Path):
    print("Generating Embeddings...")

    embedding_model = get_embedding_model()

    texts, metadatas, vectors = generate_embeddings(chunks, embedding_model)

    print("Creating vector store...")

    vector_store = create_vectorstore(texts, metadatas,vectors, embedding_model)

    save_vectorstore(vector_store, output_dir)

    print(f"Vectorstore saved at: {output_dir}")



def inspect_chunks(chunks: list, sample_size: int = 3):
    print(f"\n── Chunk sample ({sample_size} of {len(chunks)}) ──")
    for i, chunk in enumerate(chunks[:sample_size]):
        print(f"\nChunk {i+1}")
        print(f"  source : {chunk.metadata.get('source', 'unknown')}")
        print(f"  page   : {chunk.metadata.get('page', '?')}")
        print(f"  chars  : {len(chunk.page_content)}")
        print(f"  preview: {chunk.page_content[:120].strip()}...")
    print()


if __name__ == "__main__":
    ensure_directories()

    documents = load_all_documents()

    chunks = chunk_documents(documents)

    # inspect_chunks(chunks)

    build_vector_pipeline(chunks, VECTORSTORE_DIR)

    build_bm25_index(chunks, VECTORSTORE_DIR) 