# SQL Question Answering System (Text → SQL → Answer)


## What it does

- Takes a question like:
  "Show total sales by region"
- Converts it into SQL using an LLM  
- Validates the query (only SELECT allowed)  
- Executes it on a SQLite database  
- Summarizes the result into a human-readable answer  

---

## Main pipeline

```mermaid
flowchart LR
    A[User Question] --> B[Schema Loader]
    B --> C[Generate SQL]
    C --> D[Validate SQL]
    D --> E[Execute Query]
    E --> F[Summarize Result]
    F --> G[Final Answer]
```

## Tasks Performed
- **Built schema extraction from SQLite**
- **Implemented SQL generation using LLM**
- **Added query validation layer**
- **Implemented safe execution (read-only DB)**
- **Built result summarization step**

## Learning Outcomes
- **Learned how to convert natural language → SQL**
- **Understood importance of schema**
- **Built safe SQL execution**
- **Learned how we can run**
- **Implemented result summarization**

