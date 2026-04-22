import os
import asyncio
import datetime
from nexus_ai.config import LOGS_DIR
from nexus_ai.memory import build_memory_context, update_memory
from nexus_ai.agents import THINKING_AGENTS, get_tool_agents
from nexus_ai.planner import plan_pipeline, display_plan
from nexus_ai.executor import think, run_tool_agent, build_step_context, validate_and_improve

os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "nexus_log.txt")


def _start_log(task):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n{'='*60}\nTASK: {task}\nTIME: {ts}\n{'='*60}\n\n")


def _log_step(step_num, agent, reason, output):
    with open(LOG_FILE, "a") as f:
        f.write(f"[Step {step_num} - {agent.upper()}]\nJob: {reason}\nOutput:\n{output}\n{'-'*40}\n\n")


def _log_final(answer):
    with open(LOG_FILE, "a") as f:
        f.write(f"FINAL ANSWER:\n{answer}\n{'='*60}\n\n")


async def run_nexus(user_task):
    print("\n" + "=" * 55)
    print("  NEXUS AI")
    print(f"  TASK: {user_task}")
    print("=" * 55)
    _start_log(user_task)

    memory_ctx = build_memory_context(user_task)

    print("\n[1/4] Planning...")
    steps = plan_pipeline(user_task, memory_ctx)

    display_plan(steps)
    input("  Press Enter to start execution...\n")

    tool_agents = get_tool_agents()

    print("[2/4] Executing...")
    history = []

    for i, step in enumerate(steps, 1):
        agent_type = step["agent"]
        reason = step["reason"]

        print(f"  Step {i}/{len(steps)}: [{agent_type.upper()}] - {reason}")

        ctx = build_step_context(history)
        prompt = (
            f"{memory_ctx}"
            f"Original task: {user_task}\n\n"
            f"Your job in this step: {reason}\n\n"
            + (ctx if ctx else "This is the first step.")
        )

        if agent_type in ("code", "db", "file"):
            output = run_tool_agent(agent_type, prompt, tool_agents)
        else:
            output = await think(THINKING_AGENTS[agent_type], prompt)

        history.append({"step": i, "agent": agent_type, "reason": reason, "output": output})
        _log_step(i, agent_type, reason, output)
        print("    done")

    has_thinking = any(s["agent"] in THINKING_AGENTS for s in steps)
    if has_thinking and len(history) > 1:
        combined = "\n\n".join(
            f"[{e['agent'].upper()}]: {e['output']}" for e in history
        )
        final_output = await think(THINKING_AGENTS["optimizer"],
            f"Task: {user_task}\n\nHere are the outputs from all agents:\n{combined}\n\n"
            f"Combine these into one clear, complete, direct answer to the task. "
            f"Do NOT summarize what the agents did. Just answer the question directly.")
    else:
        final_output = history[-1]["output"] if history else "No output."

    if has_thinking:
        print("\n[3/4] Validating...")
        final_output = await validate_and_improve(user_task, final_output)
    else:
        print("\n[3/4] Skipping validation (execution task)")

    print("[4/4] Saving to memory...")
    update_memory(user_task, final_output)
    _log_final(final_output)

    print("\n" + "=" * 55)
    print("  FINAL ANSWER")
    print("=" * 55)
    print(final_output)
    print("=" * 55 + "\n")


async def main():
    print("=" * 55)
    print("  Nexus AI - Autonomous Multi-Agent System")
    print("  Type your task. Type 'exit' to quit.")
    print("=" * 55)

    while True:
        try:
            task = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not task:
            continue
        if task.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        try:
            await run_nexus(task)
        except Exception as e:
            print(f"\n  Error: {e}\n  Please try again.")


if __name__ == "__main__":
    asyncio.run(main())