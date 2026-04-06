import os, json
import numpy as np
import faiss
import fitz
import pytesseract
from PIL import Image
from io import BytesIO
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, CSVLoader, Docx2txtLoader
from transformers import BlipProcessor, BlipForConditionalGeneration

from embeddings.clip_embedder import CLIPEmbedder
from pipelines.ingest import chunk_documents, build_vector_pipeline
from vectorstore.bm25_store import build_bm25_index

RAW_DIR             = Path("data/raw")
VECTORSTORE_DIR     = Path("vectorstore")
IMAGES_SAVE_DIR     = Path("data/pdf_extracted")
IMAGE_FAISS_PATH    = "vectorstore/image_faiss.index"
IMAGE_META_PATH     = "vectorstore/image_metadata.json"
IMAGE_EMBEDDING_DIM = 512

SUPPORTED_IMAGES = ('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')
SUPPORTED_DOCS   = ('.pdf', '.txt', '.csv', '.docx')

clip = None
blip_processor = None
blip_model = None

def get_clip():
    global clip
    if clip is None:
        clip = CLIPEmbedder()
    return clip

def get_blip():
    global blip_processor, blip_model
    if blip_model is None:
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return blip_processor, blip_model

def load_image_index():
    os.makedirs("vectorstore", exist_ok=True)
    if os.path.exists(IMAGE_FAISS_PATH):
        return faiss.read_index(IMAGE_FAISS_PATH)
    return faiss.IndexFlatIP(IMAGE_EMBEDDING_DIM)

def load_image_meta():
    if os.path.exists(IMAGE_META_PATH):
        with open(IMAGE_META_PATH) as f:
            return json.load(f)
    return {}

def save_image_index(index):
    faiss.write_index(index, IMAGE_FAISS_PATH)

def save_image_meta(meta):
    with open(IMAGE_META_PATH, "w") as f:
        json.dump(meta, f, indent=2)

def run_ocr(image):
    try:
        return pytesseract.image_to_string(image).strip()
    except:
        return ""

def run_caption(image):
    processor, model = get_blip()
    inputs = processor(image, return_tensors="pt")
    out    = model.generate(**inputs, max_new_tokens=60)
    return processor.decode(out[0], skip_special_tokens=True)

def store_image(image, saved_image_path, source_type, source_file, page_num=None):
    image = image.convert("RGB")
    index = load_image_index()
    meta  = load_image_meta()

    if any(v.get("image_path") == saved_image_path for v in meta.values()):
        print(f"  [Skip] {os.path.basename(saved_image_path)}")
        return

    ocr       = run_ocr(image)
    caption   = run_caption(image)
    embedding = np.array([get_clip().embed_image(image)], dtype=np.float32)
    position  = index.ntotal

    index.add(embedding)
    save_image_index(index)

    meta[str(position)] = {
        "image_path"  : saved_image_path,
        "caption"     : caption,
        "ocr_text"    : ocr,
        "source_type" : source_type,
        "source_file" : source_file,
        "page_num"    : page_num,
        "filename"    : os.path.basename(saved_image_path)
    }
    save_image_meta(meta)
    print(f"  [Image stored] pos={position} | {caption[:60]}")

def process_image_file(path, text_docs):
    try:
        store_image(Image.open(path), path, "image_file", path)
    except Exception as e:
        print(f"  [Error] {path}: {e}")

def process_pdf(path, text_docs):
    print(f"\n  PDF: {os.path.basename(path)}")
    try:
        pdf = fitz.open(path)
    except Exception as e:
        print(f"  [Error] {e}")
        return

    pdf_name = Path(path).stem

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        text = page.get_text().strip()
        imgs = page.get_images(full=True)

        if text:
            text_docs.append(Document(
                page_content = text,
                metadata     = {"source": path, "page": page_num + 1, "type": "pdf_text"}
            ))

        for idx, img_info in enumerate(imgs):
            try:
                raw = pdf.extract_image(img_info[0])
                img = Image.open(BytesIO(raw["image"]))

                IMAGES_SAVE_DIR.mkdir(parents=True, exist_ok=True)
                save_filename = f"{pdf_name}_page{page_num + 1}_img{idx}.png"
                save_path     = str(IMAGES_SAVE_DIR / save_filename)

                img.convert("RGB").save(save_path)

                store_image(img, save_path, "pdf_page", path, page_num + 1)

            except Exception as e:
                print(f"  [Warning] page {page_num+1} img {idx}: {e}")

    pdf.close()

def process_text_file(path, text_docs):
    ext = Path(path).suffix.lower()
    try:
        if ext == ".txt":
            loader = TextLoader(path, encoding="utf-8")
        elif ext == ".csv":
            loader = CSVLoader(path, encoding="utf-8")
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        else:
            return
        docs = loader.load()
        for doc in docs:
            doc.metadata.setdefault("page", 0)
            doc.metadata["source"] = path
        text_docs.extend(docs)
        print(f"  [{ext.upper()}] {os.path.basename(path)} → {len(docs)} section(s)")
    except Exception as e:
        print(f"  [Error] {path}: {e}")

def ingest_folder(folder_path=None):
    folder = Path(folder_path or RAW_DIR)
    if not folder.exists():
        print(f"Folder not found: {folder}. Create data/raw/ and add your files.")
        return

    all_files = list(folder.rglob("*"))
    img_files = [f for f in all_files if f.suffix.lower() in SUPPORTED_IMAGES]
    doc_files = [f for f in all_files if f.suffix.lower() in SUPPORTED_DOCS]

    print(f"\nFound {len(img_files)} images and {len(doc_files)} documents in {folder}\n")

    text_docs = []

    for f in img_files:
        process_image_file(str(f), text_docs)

    for f in doc_files:
        if f.suffix.lower() == ".pdf":
            process_pdf(str(f), text_docs)
        else:
            process_text_file(str(f), text_docs)

    if text_docs:
        print(f"\nBuilding text index from {len(text_docs)} pages across all files...")
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        chunks = chunk_documents(text_docs)
        build_vector_pipeline(chunks, VECTORSTORE_DIR)
        build_bm25_index(chunks, VECTORSTORE_DIR)
        print(f"Text index saved: {len(chunks)} chunks")
    else:
        print("No text content found.")

    index = load_image_index()
    meta  = load_image_meta()
    print(f"\nDone — {index.ntotal} image vectors, {len(meta)} image entries, {len(text_docs)} text pages")

if __name__ == "__main__":
    ingest_folder()