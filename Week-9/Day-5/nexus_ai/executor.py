import os
import sys
import asyncio
import autogen
from contextlib import contextmanager
from nexus_ai.agents import make_agent, THINKING_AGENTS

MAX_CONTEXT_CHARS = 3000
MAX_VALIDATOR_RETRIES = 3


@contextmanager
def _suppress_output():
    devnull = open(os.devnull, "w")
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = devnull, devnull
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        devnull.close()


async def think(agent, prompt):
    result = await asyncio.to_thread(
        agent.generate_reply,
        messages=[{"role": "user", "content": prompt}],
    )
    return (result.get("content") if isinstance(result, dict) else result or "").strip()


def extract_code_block(text):
    
    if "```python" not in text:
        return ""
    start = text.find("```python")
    end = text.find("```", start + 9)
    if end == -1:
        return ""
    return text[start: end + 3]


def find_last_meaningful_message(assistant, proxy):
    
    all_messages = []
    if proxy in assistant.chat_messages:
        all_messages.extend(assistant.chat_messages[proxy])
    if assistant in proxy.chat_messages:
        all_messages.extend(proxy.chat_messages[assistant])

    for msg in reversed(all_messages):
        content = msg.get("content", "")
        if not isinstance(content, str):
            continue
        cleaned = content.replace("TERMINATE", "").strip()
        if cleaned:
            return cleaned
    return ""


def run_tool_agent(agent_type, task, tool_agents):
    result = ""
    try:
        if agent_type == "code":
            writer, executor = tool_agents["code"]
            executor.initiate_chat(writer, message=task, max_turns=5, silent=True)

            code_block = ""
            for msg in writer.chat_messages[executor]:
                if msg.get("role") != "assistant":
                    continue
                content = msg.get("content", "")
                if isinstance(content, str):
                    block = extract_code_block(content)
                    if block:
                        code_block = block
                        break

            exec_output = ""
            for msg in executor.chat_messages[writer]:
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
            result = "\n\n".join(parts)

            if not result:
                result = "[code agent produced no code or output]"

        elif agent_type == "db":
            assistant, proxy = tool_agents["db"]
            proxy.initiate_chat(assistant, message=task, max_turns=8, silent=True)
            result = find_last_meaningful_message(assistant, proxy)
            if not result:
                result = "[db agent returned no output]"

        elif agent_type == "file":
            assistant, proxy = tool_agents["file"]
            proxy.initiate_chat(assistant, message=task, max_turns=5, silent=True)
            result = find_last_meaningful_message(assistant, proxy)
            if not result:
                result = "[file agent returned no output]"

    except Exception as e:
        result = f"[{agent_type} agent failed: {e}]"

    return result.replace("TERMINATE", "").strip()


def build_step_context(history):
    if not history:
        return ""
    lines = [
        f"[Step {e['step']} - {e['agent'].upper()}]\nJob: {e['reason']}\nOutput:\n{e['output']}"
        for e in history
    ]
    full = "\n\n".join(lines)
    if len(full) <= MAX_CONTEXT_CHARS:
        return "=== PREVIOUS STEPS ===\n" + full + "\n=== END ==="

    keep_full = history[-2:]
    summarize = history[:-2]
    summary = [f"[Step {e['step']} - {e['agent'].upper()}]: {e['reason']} done" for e in summarize]
    full_entries = "\n\n".join(
        f"[Step {e['step']} - {e['agent'].upper()} - FULL]:\n{e['output']}"
        for e in keep_full
    )
    return (
        "=== PREVIOUS STEPS (summarized) ===\n" + "\n".join(summary) +
        f"\n\n{full_entries}\n=== END ==="
    )


async def validate_and_improve(task, answer):
    validator = make_agent("Validator",
        "You are the Validator. Check if the answer fully solves the task.\n"
        "Reply ONLY with:\n  STATUS: PASS\nor:\n  STATUS: FAIL\n  CRITIQUE: <specific issues>")

    optimizer = THINKING_AGENTS["optimizer"]

    for attempt in range(1, MAX_VALIDATOR_RETRIES + 1):
        print(f"  Attempt {attempt}/{MAX_VALIDATOR_RETRIES}...")
        raw = await think(validator, f"Task: {task}\n\nAnswer:\n{answer}")

        if "STATUS: PASS" in raw:
            print("  Passed")
            return answer

        critique = raw.split("CRITIQUE:", 1)[-1].strip() if "CRITIQUE:" in raw else raw
        print("  Needs work")

        if attempt < MAX_VALIDATOR_RETRIES:
            answer = await think(optimizer,
                f"Task: {task}\n\nRejected answer:\n{answer}\n\nFix these issues:\n{critique}")

    print("  Max retries reached")
    return answer