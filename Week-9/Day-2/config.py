import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 3

LLM_CONFIG = {
    "config_list": [
        {
            "model": MODEL,
            "api_key": GROQ_API_KEY,
            "base_url": "https://api.groq.com/openai/v1",
            "api_type": "openai",
        }
    ],
    "temperature": 0.3,
}