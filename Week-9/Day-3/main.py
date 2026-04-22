import os
import warnings
import autogen
import json
warnings.filterwarnings("ignore", message="Cost calculation not available")
from pathlib import Path
from dotenv import load_dotenv
from tools.code_executor import get_code_agent
from tools.db_agent import get_db_agent
from tools.file_agent import get_file_agent

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MAX_CONTEXT_CHARS = 3000


def get_llm_config():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("Set GROQ_API_KEY environment variable first.")
    return {
        "config_list": [
            {
                "model": "llama-3.3-70b-versatile",
                "api_key": api_key,
                "api_type": "groq",
                "price": [0, 0],
            }
        ],
        "temperature": 0.3,
        "cache_seed": None,
    }


def orchestrate_task(task: str, llm_config: dict) -> list[dict]:

    orchestrator = autogen.AssistantAgent(
        name="Orchestrator",
        system_message="""You are a task orchestrator.
        Given a user task, break it into an ordered sequence of agent steps.

        Available agents:
        - "file": reading/writing .txt or .csv files on disk
        - "db"  : anything involving SQL, SQLite, tables, queries
        - "code": calculations, scripts, data analysis, anything else

        Rules:
        - Same agent can appear multiple times if needed
        - Only include agents that are actually needed
        - CRITICAL: Do NOT split a single coding task into multiple steps.
          If the task is just "write a program", that is ONE code step.
          Multiple steps are only for tasks that genuinely involve different agents
          e.g. read a file THEN analyze it THEN store in DB.
        - Output MUST be a JSON list of objects: [{"agent": string, "reason": string}]
        - No explanation, no markdown, no backticks - raw JSON only

        Examples:
        "write a fibonacci program" →
        [{"agent": "code", "reason": "Write and run a complete Fibonacci program"}]

        "read sales.csv and store top 5 rows in database" →
        [
            {"agent": "file", "reason": "Read the sales CSV"},
            {"agent": "code", "reason": "Find top 5 rows"},
            {"agent": "db",   "reason": "Store the top 5 rows"}
        ]
        """,
        llm_config={**llm_config, "temperature": 0},
    )

    response = orchestrator.generate_reply(
        messages=[{"role": "user", "content": task}]
    )

    raw = (response.get("content") if isinstance(response, dict) else response) or ""
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        steps = json.loads(raw)
        valid = [
            s for s in steps
            if isinstance(s, dict) and s.get("agent") in ("file", "db", "code")
        ]
        if valid:
            return valid
    except Exception:
        pass

    print("[WARN] Orchestrator returned invalid JSON, falling back to single code step.")
    return [{"agent": "code", "reason": task}]


def build_context(history: list[dict]) -> str:

    if not history:
        return ""

    full_lines = []
    for entry in history:
        full_lines.append(
            f"[Step {entry['step']} - {entry['agent'].upper()} AGENT]\n"
            f"Job: {entry['reason']}\n"
            f"Output:\n{entry['output']}"
        )

    full_context = "\n\n".join(full_lines)

    
    if len(full_context) <= MAX_CONTEXT_CHARS:
        return "=== CONTEXT FROM PREVIOUS STEPS ===\n" + full_context + "\n=== END OF CONTEXT ==="

   
    summary_lines = [
        f"[Step {e['step']} - {e['agent'].upper()} AGENT]: {e['reason']} ✔ (completed)"
        for e in history[:-1]
    ]

    last = history[-1]
    last_full = (
        f"[Step {last['step']} - {last['agent'].upper()} AGENT]\n"
        f"Job: {last['reason']}\n"
        f"Output:\n{last['output']}"
    )

    return (
        "=== CONTEXT FROM PREVIOUS STEPS ===\n"
        "Earlier steps (summarized):\n" + "\n".join(summary_lines) +
        "\n\nMost recent step (full):\n" + last_full +
        "\n=== END OF CONTEXT ==="
    )


def run_agent(agent_type: str, task: str, agents: dict) -> str:

    result = ""

    if agent_type == "file":
        assistant, user_proxy = agents["file"]
        try:
            user_proxy.initiate_chat(
                recipient=assistant, message=task, max_turns=5, silent=True,
            )
            
            last = assistant.last_message()
            result = last.get("content", "") if last else ""
        except Exception as e:
            result = f"Agent failed: {str(e)}"

    elif agent_type == "db":
        assistant, user_proxy = agents["db"]
        try:
            user_proxy.initiate_chat(
                recipient=assistant, message=task, max_turns=8, silent=True,
            )
            
            last = assistant.last_message()
            result = last.get("content", "") if last else ""
        except Exception as e:
            result = f"Agent failed: {str(e)}"

    elif agent_type == "code":
        code_writer, code_executor = agents["code"]
        try:
            code_executor.initiate_chat(
                recipient=code_writer, message=task, max_turns=5, silent=True,
            )
            
            code_block = ""
            for msg in code_writer.chat_messages[code_executor]:
                content = msg.get("content", "")
                if isinstance(content, str) and "```python" in content:
                    code_block = content  

            
            exec_output = ""
            for msg in code_executor.chat_messages[code_writer]:
                content = msg.get("content", "")
                if isinstance(content, str) and "exitcode:" in content.lower():
                    
                    if "Code output:" in content:
                        exec_output = content.split("Code output:", 1)[1].strip()
                    else:
                        exec_output = content

           
            parts = []
            if code_block:
                parts.append(code_block)
            if exec_output:
                parts.append(f"--- Execution Output ---\n{exec_output}")
            result = "\n\n".join(parts) if parts else ""

            
            if not result:
                for msg in reversed(code_writer.chat_messages[code_executor]):
                    content = msg.get("content", "").replace("TERMINATE", "").strip()
                    if content:
                        result = content
                        break
        except Exception as e:
            result = f"Agent failed: {str(e)}"

    return (result or "").replace("TERMINATE", "").strip()


def run_task(task: str):
    llm_config = get_llm_config()

    print("=" * 50)
    print("TASK:", task)
    print("=" * 50)

    steps = orchestrate_task(task, llm_config)

    
    print("\nEXECUTION PLAN:")
    print("-" * 40)
    for i, step in enumerate(steps, 1):
        print(f"  Step {i}: [{step['agent'].upper()} AGENT] - {step['reason']}")
    print("-" * 40 + "\n")


    agents = {
        "file": get_file_agent(llm_config),
        "db":   get_db_agent(llm_config),
        "code": get_code_agent(llm_config),
    }

    
    history: list[dict] = []

    for i, step in enumerate(steps, 1):
        agent_type = step["agent"]
        reason = step["reason"]

        print(f"--> Step {i}/{len(steps)}: {agent_type.upper()} AGENT - {reason}")

        context_block = build_context(history)
        agent_task = (
            f"Original task: {task}\n\n"
            f"Your specific job in this step: {reason}\n\n"
            + (context_block if context_block else "This is the first step, no prior context.")
        )

        output = run_agent(agent_type, agent_task, agents)

        history.append({
            "step": i,
            "agent": agent_type,
            "reason": reason,
            "output": output,
        })

        print(f" Done\n")

    print("=" * 50)
    print(">>> FINAL ANSWER <<<")
    print("=" * 50)
    print(history[-1]["output"] if history else "[No result returned]")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("  Day 3 - Tool-Using Agents")
    print("  Orchestrated: FILE | DB | CODE agents")
    print("=" * 50)
    print("  Type a task and press Enter.")
    print("  Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Task: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        try:
            run_task(user_input)
        except Exception as e:
            print(f"\n  Error: {e}")
            print("  Please try again.\n")