import os
import re
import json
from groq import Groq

from dotenv import load_dotenv
load_dotenv(".env") 

GROQ_MODEL = "llama-3.3-70b-versatile"


def _call_llm(prompt: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in your .env file")
    
    client   = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,        # 0 = deterministic, best for SQL generation
    )
    return response.choices[0].message.content.strip()

def generate_sql(question: str, schema: str) -> dict:
    prompt = f"""You are an expert SQL developer working with a SQLite database.

        DATABASE SCHEMA:
        {schema}

        USER QUESTION: "{question}"

        Write a single SQL SELECT query that answers this question.

        RULES:
        - Only write SELECT queries — never DROP, DELETE, INSERT, UPDATE, ALTER
        - Use only tables and columns that exist in the schema
        - Use SQLite syntax (use strftime() for date functions, not DATE_FORMAT)
        - Add LIMIT 50 unless the user explicitly asks for everything
        - Use column aliases (AS) to make results readable

        Respond with ONLY a JSON object — no explanation, no markdown fences:
        {{"sql": "SELECT ...", "explanation": "one sentence describing what this query does"}}"""

    try:
        raw = _call_llm(prompt)
        
        clean  = re.sub(r"```json|```", "", raw).strip()
        parsed = json.loads(clean)

        sql         = parsed.get("sql", "").strip()
        explanation = parsed.get("explanation", "")

        if not sql:
            return {"success": False, "sql": "", "explanation": "", "error": "Grok returned empty SQL"}

        return {"success": True, "sql": sql, "explanation": explanation, "error": None}

    except json.JSONDecodeError:

        match = re.search(r"(SELECT\s.+?)(?:;|$)", raw, re.IGNORECASE | re.DOTALL)
        if match:
            sql = match.group(1).strip()
            return {"success": True, "sql": sql, "explanation": "", "error": None}
        return {"success": False, "sql": "", "explanation": "", "error": f"Could not parse response: {raw[:300]}"}

    except Exception as e:
        return {"success": False, "sql": "", "explanation": "", "error": str(e)}


def summarize_result(question: str, sql: str, columns: list, rows: list) -> str:
    if not rows:
        return "The query ran successfully but returned no results. There may be no data matching your criteria."

    
    header    = " | ".join(columns)
    separator = "-" * len(header)
    data_lines = "\n".join(" | ".join(str(v) for v in row) for row in rows[:25])
    table_str  = f"{header}\n{separator}\n{data_lines}"

    if len(rows) > 25:
        table_str += f"\n... ({len(rows) - 25} more rows not shown)"

    prompt = f"""A user asked this question about a database: "{question}"

        The following SQL was executed:
        {sql}

        Results ({len(rows)} rows):
        {table_str}

        Write a clear, specific 2-3 sentence answer to the user's question based on these results.
        - Use actual numbers and names from the data
        - Do NOT mention SQL, databases, or technical terms
        - Do NOT use any markdown formatting (no backticks, no bold, no bullet points)
        - Write as if you're a human analyst explaining findings to a business user"""

    try:
        return _call_llm(prompt)

    except Exception as e:

        return f"Query returned {len(rows)} result(s):\n\n{table_str}\n\n(Auto-summary failed: {e})"