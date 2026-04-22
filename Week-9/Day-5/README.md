# Nexus AI — Week 9 Capstone

Autonomous multi-agent AI system built with AutoGen + Groq.

## What it does

```
Takes any complex task and runs it through a 9-agent pipeline:
Orchestrator → Planner + Researcher → Coder → Analyst →
Critic → Optimizer → Validator → Reporter

```
## How to run

pip install faiss-cpu sentence-transformers "ag2[groq]"
export GROQ_API_KEY=your_key_here
cd nexus_ai
python -m nexus_ai.main

## Example tasks

"Plan a startup in AI for healthcare"
"Design a RAG pipeline for 50k documents"
"Generate backend architecture for a scalable app"
"Analyze a CSV and create a business strategy"

## Deliverables

nexus_ai/main.py     — main pipeline
nexus_ai/config.py   — all configuration
memory/              — session + vector memory from Day 4
logs/                — all agent outputs + final reports
ARCHITECTURE.md      — system design
FINAL-REPORT.md      — project summary