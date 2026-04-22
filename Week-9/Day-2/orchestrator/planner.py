import json
from groq import Groq
from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

PLANNER_PROMPT = """
        You are a task planner. Break the user query into subtasks.

        Return ONLY a valid JSON object like this:
        {
        "task_1": {"description": "...", "dependencies": []},
        "task_2": {"description": "...", "dependencies": []},
        "task_3": {"description": "...", "dependencies": ["task_1", "task_2"]}
        }

        Rules:
        - Tasks with empty dependencies run in parallel.
        - A task lists dependency task IDs only if it truly needs their output first.
        - Create as many or as few tasks as the query actually needs.
        - No explanation, no markdown, just the JSON object.
"""

def build_dag(user_query):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_query},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        dag = json.loads(raw)
    except json.JSONDecodeError:
        dag = {}

    sanitized = {}
    for tid, info in dag.items():
        if not isinstance(info, dict):
            continue
        sanitized[tid] = {
            "description": info.get("description", user_query),
            "dependencies": info.get("dependencies", []),
        }

    if not sanitized:
        sanitized = {
            "task_1": {"description": user_query, "dependencies": []}
        }

    return sanitized