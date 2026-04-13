from fastapi import FastAPI
from pydantic import BaseModel
from model import generate
from config import MAX_NEW_TOKENS, TEMPERATURE, TOP_P, TOP_K
import time, uuid

app = FastAPI(title="Local LLM API")

class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = MAX_NEW_TOKENS
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K

class ChatRequest(BaseModel):
    message: str
    history: list = []
    max_new_tokens: int = MAX_NEW_TOKENS
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K

@app.post("/generate")
def generate_endpoint(req: GenerateRequest):
    request_id = str(uuid.uuid4())[:8]
    start = time.time()
    response = generate(req.prompt, [], req.max_new_tokens, req.temperature, req.top_p, req.top_k)
    elapsed = round(time.time() - start, 2)
    return {"request_id": request_id, "response": response, "latency_sec": elapsed}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    request_id = str(uuid.uuid4())[:8]
    start = time.time()
    response = generate(req.message, req.history, req.max_new_tokens, req.temperature, req.top_p, req.top_k)
    elapsed = round(time.time() - start, 2)
    return {"request_id": request_id, "response": response, "latency_sec": elapsed}

@app.get("/health")
def health():
    return {"status": "ok"}