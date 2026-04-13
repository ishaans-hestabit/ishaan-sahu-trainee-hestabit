import torch, time, os
from transformers import AutoTokenizer, AutoModelForCausalLM

DRIVE_BASE = "/content/drive/MyDrive/Week-8 Local"
FP16_PATH  = f"{DRIVE_BASE}/quantized/model-fp16"

tokenizer = AutoTokenizer.from_pretrained(FP16_PATH)
tokenizer.pad_token = tokenizer.eos_token


test_prompts = [
    "### Instruction:\nWhat is machine learning?\n\n### Input:\n\n### Response:\n",
    "### Instruction:\nExplain neural networks in simple terms.\n\n### Input:\n\n### Response:\n",
    "### Instruction:\nWhat is the difference between AI and ML?\n\n### Input:\n\n### Response:\n",
]

def benchmark(model, tokenizer, prompts, label):
    results = []

    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        torch.cuda.reset_peak_memory_stats()

        start = time.time()
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=100, do_sample=False)
        elapsed = time.time() - start

        new_tokens = out.shape[1] - inputs["input_ids"].shape[1]
        tok_per_sec = round(new_tokens / elapsed, 2)
        latency = round(elapsed, 3)
        vram = round(torch.cuda.max_memory_allocated() / 1e9, 3)

        response = tokenizer.decode(out[0], skip_special_tokens=True)
        response = response.split("### Response:")[-1].strip()[:150]

        print(f"[{label}] {tok_per_sec} tok/s | {latency}s | {vram}GB VRAM")
        print(f"Output: {response[:80]}\n")

        results.append({
            "format": label,
            "prompt": prompt.split("\n")[1][:40],
            "tokens_per_sec": tok_per_sec,
            "latency_sec": latency,
            "vram_gb": vram,
            "output": response,
            "accuracy": None 
        })

    return results


if __name__ == "__main__":
    model = AutoModelForCausalLM.from_pretrained(FP16_PATH, dtype=torch.float16, device_map="auto")
    results = benchmark(model, tokenizer, test_prompts, "FP16")
    for r in results:
        print(f"\nPrompt: {r['prompt']}")
        print(f"Output: {r['output']}")
        print(f"Speed : {r['tokens_per_sec']} tok/s | Latency: {r['latency_sec']}s | VRAM: {r['vram_gb']}GB | Accuracy: {r['accuracy']}")