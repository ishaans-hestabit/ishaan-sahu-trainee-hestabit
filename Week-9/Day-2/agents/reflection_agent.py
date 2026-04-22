import asyncio
import autogen
from config import LLM_CONFIG

reflection = autogen.AssistantAgent(
    name="reflection",
    system_message=(
        "You are a reflection agent. You receive results from multiple worker agents "
        "and must merge them into one complete, well-structured answer to the original question. "
        "Remove any repetition. Ensure the answer flows naturally. "
        "If a critique is provided, fix exactly the issues mentioned and improve the answer. "
        "Return only the final answer. No preamble, no meta-commentary."
    ),
    llm_config=LLM_CONFIG,
)


async def reflect(user_query, task_results, critique=None):
    combined = "\n\n".join(
        f"[{task_id}]: {result}" for task_id, result in task_results.items()
    )

    message = f"Original question: {user_query}\n\nSubtask results:\n{combined}"

    if critique:
        message += f"\n\nPrevious answer was rejected. Fix these issues:\n{critique}"

    return await asyncio.to_thread(
        reflection.generate_reply,
        messages=[{"role": "user", "content": message}],
    )