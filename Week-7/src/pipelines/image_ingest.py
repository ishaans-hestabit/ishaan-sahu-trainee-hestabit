import os
import json
import numpy as np
import faiss
import pytesseract
import fitz
from PIL import Image
from io import BytesIO
from pathlib import Path
from langchain_core.documents import Document
from transformers import BlipProcessor, BlipForConditionalGeneration
from embeddings.clip_embedder import CLIPEmbedder
from pipelines.ingest import chunk_documents, build_vector_pipeline
from vectorstore.bm25_store import build_bm25_index

FAISS_INDEX_PATH = "vectorstore/image_faiss.index"
METADATA_PATH    = "vectorstore/image_metadata.json"
VECTORSTORE_DIR  = Path("vectorstore")
EMBEDDING_DIM    = 512

print("[Setup] Loading CLIP...")
clip = CLIPEmbedder()

print("[Setup] Loading BLIP...")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model     = BlipForConditionalGeneration.from_pretrained( "Salesforce/blip-image-captioning-base")
print("[Setup] Done.\n")


def _load_or_create_faiss():
    os.makedirs("vectorstore", exist_ok=True)
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        print(f"[FAISS-image] Loaded — {index.ntotal} vectors")
    else:
        index = faiss.IndexFlatIP(EMBEDDING_DIM)
        print("[FAISS-image] Created new index")
    return index

def _save_faiss(index):
    faiss.write_index(index, FAISS_INDEX_PATH)

def _load_metadata() -> dict:
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH) as f:
            return json.load(f)
    return {}

def _save_metadata(meta: dict):
    with open(METADATA_PATH, "w") as f:
        json.dump(meta, f, indent=2)

def _is_already_indexed(image_id: str, meta: dict) -> bool:
    return any(v.get("image_path") == image_id for v in meta.values())


def run_ocr(image: Image.Image) -> str:
    try:
        x = pytesseract.image_to_string(image).strip()
        print(x)
        return x
    except Exception as e:
        print(f"  [OCR] Skipped: {e}")
        return ""

def run_caption(image: Image.Image) -> str:
    inputs = blip_processor(image, return_tensors="pt")
    out    = blip_model.generate(**inputs, max_new_tokens=60)
    return blip_processor.decode(out[0], skip_special_tokens=True)


def _store_one_image(image: Image.Image, image_id: str, source_type: str, source_file: str, page_num: int = None):
    image = image.convert("RGB")
    index = _load_or_create_faiss()
    meta  = _load_metadata()

    if _is_already_indexed(image_id, meta):
        print(f"  [Skip] Already indexed: {os.path.basename(image_id)}")
        return

    ocr = run_ocr(image)
    print(f"  [OCR] {ocr[:70]}..." if ocr else "  [OCR]     (none)")

    embedding = np.array([clip.embed_image(image)], dtype=np.float32)

    caption = run_caption(image)
    print(f"  [Caption] {caption}")

    position = index.ntotal
    index.add(embedding)
    _save_faiss(index)

    meta[str(position)] = {
        "image_path"  : image_id,
        "caption"     : caption,
        "ocr_text"    : ocr,
        "source_type" : source_type,
        "source_file" : source_file,
        "page_num"    : page_num,
        "filename"    : os.path.basename(source_file)
    }
    _save_metadata(meta)
    print(f"[Stored] FAISS pos={position}\n")


def ingest_image_file(image_path: str):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"  [Error] Cannot open {image_path}: {e}")
        return
    _store_one_image(
        image       = image,
        image_id    = image_path,
        source_type = "image_file",
        source_file = image_path
    )


def ingest_pdf(pdf_path: str):
    print(f"\n[PDF] Processing: {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"  [Error] Cannot open PDF: {e}")
        return

    text_documents = []
    total_images   = 0

    for page_num in range(len(doc)):
        page      = doc[page_num]
        page_text = page.get_text().strip()
        page_imgs = page.get_images(full=True)

        if page_text:
            lc_doc = Document(
                page_content=page_text,
                metadata={
                    "source" : pdf_path,
                    "page"   : page_num + 1,
                    "type"   : "pdf_text"
                }
            )
            text_documents.append(lc_doc)
            print(f"  Page {page_num+1}: {len(page_text)} chars of text → text pipeline")

        if page_imgs:
            print(f"  Page {page_num+1}: {len(page_imgs)} image(s) → image pipeline")
            for img_idx, img_info in enumerate(page_imgs):
                xref = img_info[0]
                try:
                    base_img  = doc.extract_image(xref)
                    pil_image = Image.open(BytesIO(base_img["image"]))
                    image_id  = f"{pdf_path}::page_{page_num+1}::img_{img_idx}"
                    _store_one_image(
                        image       = pil_image,
                        image_id    = image_id,
                        source_type = "pdf_page",
                        source_file = pdf_path,
                        page_num    = page_num + 1
                    )
                    total_images += 1
                except Exception as e:
                    print(f"  [Warning] img {img_idx} page {page_num+1}: {e}")

        if not page_text and not page_imgs:
            print(f"  Page {page_num+1}: empty — skipped")

    doc.close()

    if text_documents:
        print(f"\n  [Text] {len(text_documents)} pages → chunking + embedding...")

        chunks = chunk_documents(text_documents)

        build_vector_pipeline(chunks, VECTORSTORE_DIR)

        build_bm25_index(chunks, VECTORSTORE_DIR)

        print(f"  [Text] {len(chunks)} chunks → text FAISS + BM25 ✅")

    print(f"\n[PDF Done] images={total_images}, text_pages={len(text_documents)}")


def ingest_folder(folder_path: str):
    supported_img = ('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')
    supported_pdf = ('.pdf',)

    all_files = os.listdir(folder_path)
    img_files = [f for f in all_files if f.lower().endswith(supported_img)]
    pdf_files = [f for f in all_files if f.lower().endswith(supported_pdf)]

    print(f"\n[Ingest] '{folder_path}'  —  {len(img_files)} images, {len(pdf_files)} PDFs")
    print("=" * 55)

    for fname in img_files:
        print(f"\n→ Image: {fname}")
        ingest_image_file(os.path.join(folder_path, fname))

    for fname in pdf_files:
        ingest_pdf(os.path.join(folder_path, fname))

    index = _load_or_create_faiss()
    meta  = _load_metadata()
    print("=" * 55)
    print(f"[Done] Image FAISS vectors   : {index.ntotal}")
    print(f"[Done] Image metadata entries: {len(meta)}")