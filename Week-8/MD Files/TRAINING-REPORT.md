# LoRA / QLoRA Fine-Tuning (Day 2)

In this step, I fine-tuned a small LLM using **QLoRA** to adapt it to my dataset without training the full model.

---

## What this step does

- Loads a base LLM in **4-bit (memory efficient)**
- Applies **LoRA adapters (~1% trainable params)**
- Fine-tunes on instruction dataset
- Saves adapter weights

---

## Pipeline Flow

```mermaid
flowchart LR
    A[Base Model] --> B[Load in 4-bit]
    B --> C[Apply LoRA]
    C --> D[Train on Dataset]
    D --> E[Save Adapters]
```

## Training Setup
- LoRA (rank) = 16
- Learning Rate = 2e-4
- Batch Size = 4
- Epochs = 3
- Quantization = 4-bit(QLoRA)

## Tasks Performed
- Load model using ```bitsandbytes``` (4-bit)
- Applied LoRA using ```peft```
- trained model using ```trl```
- Monitored training loss
- Saved adapter weights

## Loss Image
![loss image](../Day-2/loss%20image.png)

## Learning Outcomes
- Understood parameter-efficient fine-tuning (LoRA)
- Learned how QLoRA reduces memory usage
- Fine-tuned an LLM on limited resources (Colab)
- Understood trainable vs frozen parameters

## Deliverables
- **notebooks/lora_train.ipynb**
- **adapters/adapter_model.bin** now it has changed to adapter_model.safetensors
- **TRAINING-REPORT.md**