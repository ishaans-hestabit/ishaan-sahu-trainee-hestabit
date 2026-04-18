# Quantisation Report — Day 3

## What We Did
Converted the fine-tuned TinyLlama model into 4 formats:
FP16 (baseline) → INT8 → INT4 → GGUF

## Results

| Format | Size (GB) | Speed (tok/s) | Quality |
|--------|-----------|---------------|---------|
| FP16   | 2.204      | 18.94          | Best    |
| INT8   | 1.236      | 8.22          | Good    |
| INT4   | 0.766      | 14.77          | Good    |
| GGUF   | 1.17      | CPU inference | Good    |

## Conclusion
- INT8 is ~2x smaller than FP16 with almost no quality loss
- INT4 is ~3x smaller than FP16, runs faster, slight quality drop
- GGUF (q4_0) allows the model to run on CPU without any GPU
