import os
from pipelines.image_ingest import ingest_folder
from retriever.image_search  import text_to_image, image_to_image, image_to_text_answer, show_stats

DATA_FOLDER = "data/raw/images"
os.makedirs(DATA_FOLDER, exist_ok=True)


ingest_folder(DATA_FOLDER)

img_files = [
    os.path.join(DATA_FOLDER, f)
    for f in os.listdir(DATA_FOLDER)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
]

if not img_files:
    print("\nNo images found — add PNG/JPG files to data/raw/images/ and rerun.")
else:
    # sample = img_files[0]
    sample = "/home/ishaansahu/HestaBit/Week-7/src/data/raw/test/cat2.jpeg"
    print(sample)

    # Mode 1: text → image
    text_to_image("what is Somatosensory?", n=3)

    # Mode 2: image → image
    # image_to_image(sample, n=3)

    # # Mode 3: image → text (LLM-ready output)
    # answer = image_to_text_answer(sample, n=2)
    # print("\n--- LLM-ready context block ---")
    # print(answer)
