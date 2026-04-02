import json, os

def is_valid(row):

    return bool(row["instruction"].strip() and row["output"].strip())

def clean_and_save(dataset, path="data/cleaned.jsonl"):
    os.makedirs("data", exist_ok=True)
    cleaned = []

    for row in dataset:
        if is_valid(row):
            cleaned.append({
                "instruction": row["instruction"].strip(),
                "input": row["input"].strip(),
                "output": row["output"].strip(),
                "type": row["type"]
            })

    with open(path, "w") as f:
        for row in cleaned:
            f.write(json.dumps(row) + "\n")

    print(f"Original: {len(dataset)} | Cleaned: {len(cleaned)} | Saved to {path}")
    return cleaned

cleaned = clean_and_save(labeled)
print(f"After cleaning: {len(cleaned)} samples (removed {len(labeled) - len(cleaned)})")