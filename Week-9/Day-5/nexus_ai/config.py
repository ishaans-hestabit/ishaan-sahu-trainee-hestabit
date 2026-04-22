import os
import warnings
import logging
from pathlib import Path
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

warnings.filterwarnings("ignore")
logging.getLogger("autogen").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = str(BASE_DIR / "workspace")
LOGS_DIR = str(BASE_DIR / "logs")
SCRATCH_DIR = str(BASE_DIR / "workspace" / ".scratch")
DB_PATH = str(BASE_DIR / "workspace" / "nexus.db")
VECTOR_DIR = str(BASE_DIR / "workspace" / "memory")
VECTOR_FILE = str(BASE_DIR / "workspace" / "memory" / "vectors.index")
TEXT_FILE = str(BASE_DIR / "workspace" / "memory" / "vectors_text.json")

LLM_CONFIG = {
    "config_list": [{
        "model": "llama-3.3-70b-versatile",
        "api_key": os.environ.get("GROQ_API_KEY", ""),
        "api_type": "groq",
        "price": [0, 0],
    }],
    "temperature": 0.3,
    "cache_seed": None,
    "max_tokens": 2048,
}