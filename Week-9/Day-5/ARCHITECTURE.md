# ARCHITECTURE.md

## Nexus AI — System Architecture

## Agent Pipeline

```
Orchestrator → decides what each agent should focus on
     |
     +---> Planner (parallel) → breaks task into 3 steps
     |
     +---> Researcher (parallel) → finds key facts and concepts
                    |
                    v
               Coder → writes technical implementation
                    |
                    v
               Analyst → extracts top 3 insights
                    |
                    v
               Critic → finds 2 specific problems
                    |
                    v
               Optimizer → fixes the problems
                    |
                    v
               Validator → approves or sends back for revision
                    |
                    v
               Reporter → writes the final clean report
```
## Failure Recovery

If Validator returns NEEDS WORK:
  Optimizer runs again with validator feedback
  This loop can run once automatically

## Memory

Session memory  → current run context (RAM)
Vector memory   → past task context (FAISS, persists to disk)
Both injected into Orchestrator prompt at start of each run

## Logs

Every agent output logged to logs/nexus_log.txt
Final report saved to logs/final_report.txt

## Key Design Principles

One agent, one job
Parallel where no dependency exists
Memory improves answers over time
Validator gates the output
Reporter hides internal complexity from the user