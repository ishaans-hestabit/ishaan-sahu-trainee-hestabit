import streamlit as st
import asyncio
import datetime
import os
import sys
import traceback
import concurrent.futures

st.set_page_config(page_title="Nexus AI", layout="centered")

st.title("Nexus AI")
st.divider()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if "messages" not in st.session_state:
    st.session_state.messages = []


def run_nexus(task: str) -> str:

    from nexus_ai.config import LOGS_DIR
    from nexus_ai.memory import build_memory_context, update_memory
    from nexus_ai.agents import THINKING_AGENTS, get_tool_agents
    from nexus_ai.planner import plan_pipeline, display_plan
    from nexus_ai.executor import think, run_tool_agent, build_step_context, validate_and_improve

    os.makedirs(LOGS_DIR, exist_ok=True)
    log_file = os.path.join(LOGS_DIR, "nexus_log.txt")

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"\n{'='*60}\nTASK: {task}\nTIME: {ts}\n{'='*60}\n\n")

    
    print("\n" + "=" * 55)
    print("  NEXUS AI")
    print(f"  TASK: {task}")
    print("=" * 55)

    async def _pipeline():
        memory_ctx = build_memory_context(task)

        print("\n[1/4] Planning...")
        steps = plan_pipeline(task, memory_ctx)
        display_plan(steps)  

        tool_agents = get_tool_agents()
        history = []

        print("[2/4] Executing...")
        for i, step in enumerate(steps, 1):
            agent_type = step["agent"]
            reason = step["reason"]

            print(f"  Step {i}/{len(steps)}: [{agent_type.upper()}] - {reason}")

            ctx = build_step_context(history)

            
            if agent_type in ("code", "db", "file"):
                prompt = (
                    f"Original task: {task}\n\n"
                    f"Your job in this step: {reason}\n\n"
                    + (ctx if ctx else "This is the first step.")
                )
                output = await asyncio.to_thread(run_tool_agent, agent_type, prompt, tool_agents)
            else:
                prompt = (
                    f"{memory_ctx}"
                    f"Original task: {task}\n\n"
                    f"Your job in this step: {reason}\n\n"
                    + (ctx if ctx else "This is the first step.")
                )
                output = await think(THINKING_AGENTS[agent_type], prompt)

            history.append({"step": i, "agent": agent_type, "reason": reason, "output": output})

            with open(log_file, "a") as f:
                f.write(f"[Step {i} - {agent_type.upper()}]\nJob: {reason}\nOutput:\n{output}\n{'-'*40}\n\n")

            print("    done")

        has_thinking = any(s["agent"] in THINKING_AGENTS for s in steps)
        if has_thinking and len(history) > 1:
            combined = "\n\n".join(f"[{e['agent'].upper()}]: {e['output']}" for e in history)
            final = await think(
                THINKING_AGENTS["optimizer"],
                f"Task: {task}\n\nOutputs from all agents:\n{combined}\n\n"
                "Combine into one clear, complete, direct answer. Do NOT describe what agents did."
            )
        else:
            final = history[-1]["output"] if history else "No output."

        if has_thinking:
            print("\n[3/4] Validating...")
            final = await validate_and_improve(task, final)
        else:
            print("\n[3/4] Skipping validation (execution task)")

        print("[4/4] Saving to memory...")
        update_memory(task, final)

        with open(log_file, "a") as f:
            f.write(f"FINAL ANSWER:\n{final}\n{'='*60}\n\n")

        print("\n" + "=" * 55)
        print("  DONE")
        print("=" * 55 + "\n")

        return final

    def _run_in_thread():
        return asyncio.run(_pipeline())

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run_in_thread)
        return future.result()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Enter your task here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Running agents..."):
            try:
                answer = run_nexus(user_input)
                if not answer or not str(answer).strip():
                    answer = " Pipeline completed but produced no output. Check logs/nexus_log.txt for details."
            except Exception as e:
                err_type = type(e).__name__
                err_msg = str(e) if str(e) else repr(e)
                tb = traceback.format_exc()
                answer = f" **{err_type}:** {err_msg}"
                with st.expander("Full traceback "):
                    st.code(tb, language="text")

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})