# Benchmark Report — Day 4

## Models Tested
- FP16 : full precision fine-tuned model (GPU)
- INT8 : 8-bit quantised model (GPU)
- INT4 : 4-bit quantised model (GPU)
- GGUF : q8_0 quantised model (CPU via llama.cpp)

## Results

| Format | Tokens/sec | Avg Latency | Memory | Accuracy |
|--------|------------|-------------|--------|----------|
| FP16   | 29.9 | 2.773s | 2.714GB VRAM | 2/3 |
| INT8   | 8.1 | 8.359s | 1.745GB VRAM | 2/3 |
| INT4   | 13.96 | 3.984s | 0.796GB VRAM | 3/3 |
| GGUF   | 5.89 | 14.101s | 2663.2MB RAM | 2/3 |

## Features Demonstrated
- Streaming output — tokens appear live as generated
- Batch inference — 3 prompts processed simultaneously
- Multi-prompt testing — 3 different prompts per format

## Key Findings
- INT8 uses less VRAM than FP16 with near-identical output quality
- INT4 uses the least VRAM of the GPU formats
- GGUF runs with zero GPU — works on any laptop
- Batch inference handles multiple users faster than one by one
