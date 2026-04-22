import json
from nexus_ai.agents import make_agent

VALID_AGENTS = {"code", "db", "file", "planner", "researcher", "analyst", "critic", "optimizer"}


def plan_pipeline(task, memory_ctx):
    orchestrator = make_agent("Orchestrator", """You are the Orchestrator of Nexus AI. Given a task, decide which agents to run and in what order.

        TOOL AGENTS (they execute):
        "code"  - write and execute Python code
        "db"    - run SQL queries on SQLite (SELECT, INSERT, UPDATE, DELETE, CREATE TABLE)
        "file"  - read or write files on disk (txt, csv, json, html, py, etc.)

        THINKING AGENTS (they reason):
        "planner"    - break complex task into steps
        "researcher" - gather relevant facts
        "analyst"    - extract key insights
        "critic"     - identify weaknesses
        "optimizer"  - improve based on feedback

        RULES:
        - For execution tasks (create file, run code, query db): use ONLY tool agents
        - For analytical tasks (plan, explain, research): use ONLY thinking agents
        - For complex tasks: mix both — tool agents first, thinking agents after
        - Do NOT split a single coding task into multiple steps
        - Keep the pipeline minimal (2-4 steps max)
        - Output ONLY a valid JSON array. No explanation, no markdown, no backticks.

        Examples:
        "write a fibonacci program" ->
        [{"agent": "code", "reason": "Write and run a Fibonacci program"}]

        "what is machine learning" ->
        [{"agent": "researcher", "reason": "Explain machine learning concepts"},
        {"agent": "analyst", "reason": "Extract key insights"}]

        "read sales.csv and find insights" ->
        [{"agent": "file", "reason": "Read sales.csv"},
        {"agent": "analyst", "reason": "Extract key insights from the data"},
        {"agent": "critic", "reason": "Find gaps in the analysis"},
        {"agent": "optimizer", "reason": "Produce final improved analysis"}]

        "create a users table in the database" ->
        [{"agent": "db", "reason": "Create a users table in SQLite"}]

        "update salary of employee id 5 to 90000" ->
        [{"agent": "db", "reason": "Update salary for employee id 5"}]""")

    prompt = f"{memory_ctx}Task: {task}" if memory_ctx else f"Task: {task}"
    response = orchestrator.generate_reply(messages=[{"role": "user", "content": prompt}])

    raw = (response.get("content") if isinstance(response, dict) else response or "").strip()


    if "```" in raw:
        
        start = raw.find("```")
        end = raw.find("```", start + 3)
        if end != -1:
            raw = raw[start + 3: end].strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()
  
    bracket_start = raw.find("[")
    bracket_end = raw.rfind("]")
    if bracket_start != -1 and bracket_end != -1:
        raw = raw[bracket_start: bracket_end + 1]

    try:
        steps = json.loads(raw)
        valid = [s for s in steps if isinstance(s, dict) and s.get("agent") in VALID_AGENTS]
        if valid:
            return valid
    except Exception:
        pass


    print("  [WARN] Orchestrator plan invalid, using keyword fallback")
    t = task.lower()
    if any(k in t for k in ["file", "read", "write", "csv", "save", "txt", "json", "html"]):
        return [{"agent": "file", "reason": task}]
    if any(k in t for k in ["sql", "database", "query", "table", "insert", "update", "delete", "select"]):
        return [{"agent": "db", "reason": task}]
    if any(k in t for k in ["code", "script", "program", "run", "execute", "python", "html", "create", "build"]):
        return [{"agent": "code", "reason": task}]
    return [
        {"agent": "planner", "reason": "Break the task into steps"},
        {"agent": "researcher", "reason": "Gather relevant knowledge"},
        {"agent": "analyst", "reason": "Extract key insights"},
    ]


def display_plan(steps):
    print("\n  EXECUTION PLAN")
    print("  " + "=" * 45)
    for i, step in enumerate(steps, 1):
        agent = step["agent"].upper()
        reason = step["reason"]
        print(f"  Step {i}  [{agent:>10}]  {reason}")
    print("  " + "-" * 45)
    has_thinking = any(s["agent"] in ("planner", "researcher", "analyst", "critic", "optimizer") for s in steps)
    if has_thinking:
        print("         [  VALIDATOR]  quality check (auto, max 3 retries)")
    print("  " + "=" * 45)