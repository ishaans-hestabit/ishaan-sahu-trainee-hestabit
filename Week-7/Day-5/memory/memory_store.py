import json
from pathlib import Path
from datetime import datetime

MEMORY_DIR   = Path(__file__).resolve().parent
HISTORY_FILE = MEMORY_DIR / "chat_history.json"

MAX_MESSAGES = 10


def save_message(role: str, content: str):
    history = _load_raw()

    history.append({
        "role":      role,
        "content":   content,
        "timestamp": datetime.now().isoformat()
    })

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_last_n_messages() -> list:
    history = _load_raw()

    recent = history[-MAX_MESSAGES:]

    cleaned = [
        {"role": m["role"], "content": m["content"]}
        for m in recent
        if "role" in m and "content" in m
    ]

    return cleaned


def _load_raw() -> list:
    
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text())
        return data if isinstance(data, list) else []
    except Exception:
        return []   # corrupted file — start fresh