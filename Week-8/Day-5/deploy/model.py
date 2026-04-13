from llama_cpp import Llama
from config import MODEL_PATH

_model = None

def load_model():
    global _model
    if _model is None:
        print("Loading GGUF model...")
        _model = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
        print("Model ready!")
    return _model

def get_type(prompt):
    p = prompt.lower()
    if any(w in p for w in ["extract", "parse", "find all", "retrieve"]):
        return "extraction"
    elif any(w in p for w in ["explain", "why", "how does", "what is", "difference"]):
        return "reasoning"
    return "qa"

def generate(prompt, history, max_new_tokens, temperature, top_p, top_k):
    model = load_model()

    context = ""

    for turn in history:
        context += f"### Task Type: {get_type(turn['user'])}\n\n"
        context += f"### Instruction:\n{turn['user']}\n\n"
        context += f"### Input:\n\n"
        context += f"### Response:\n{turn['assistant']}\n\n"

    context += f"### Task Type: {get_type(prompt)}\n\n"
    context += f"### Instruction:\n{prompt}\n\n"
    context += f"### Input:\n\n"
    context += f"### Response:\n"

    out = model(
        context,
        max_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        echo=False,
        stop=["### Instruction:", "### Input:", "### Response:", "### Task Type:"]
    )

    response = out["choices"][0]["text"].strip()

    for s in ["### Instruction:", "### Input:", "### Response:", "### Task"]:
        if s in response:
            response = response.split(s)[0].strip()

    return response