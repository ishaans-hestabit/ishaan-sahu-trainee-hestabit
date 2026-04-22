import asyncio
import autogen
from config import LLM_CONFIG

worker = autogen.AssistantAgent(
    name="worker",
    system_message=(
        "You are a worker agent. You will receive one specific subtask and optionally "
        "context from previous tasks. Complete your subtask thoroughly and return only "
        "the result. Be specific, accurate, and concise. No preamble, no closing remarks."
    ),
    llm_config=LLM_CONFIG,
)


def get_worker_message(user_query, task_description, dep_context=""):
    message = f"Original query: {user_query}\n\nYour subtask: {task_description}"
    if dep_context:
        message += f"\n\nContext from previous tasks:\n{dep_context}"
    return message


async def run_worker(user_query, task_description, dep_context=""):
    message = get_worker_message(user_query, task_description, dep_context)
    result = await asyncio.to_thread(
        worker.generate_reply,
        messages=[{"role": "user", "content": message}],
    )
    return result