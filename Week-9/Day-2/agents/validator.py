import asyncio
import autogen
from config import LLM_CONFIG

validator = autogen.AssistantAgent(
    name="validator",
    system_message=(
        "You are a validator agent. Check if the given answer fully and correctly addresses "
        "the original question. Be strict — a vague or incomplete answer should fail.\n\n"
        "Reply in exactly one of these two formats:\n\n"
        "If the answer is good:\n"
        "STATUS: PASS\n"
        "ANSWER: <reproduce the full answer exactly, word for word, without any changes>\n\n"
        "If the answer has problems:\n"
        "STATUS: FAIL\n"
        "CRITIQUE: <list the specific problems clearly so they can be fixed>\n\n"
        "Never summarize the answer. Never paraphrase it. On PASS, copy it fully and exactly."
    ),
    llm_config=LLM_CONFIG,
)


async def validate(user_query, answer):
    message = f"Original question: {user_query}\n\nAnswer to validate:\n{answer}"

    raw = await asyncio.to_thread(
        validator.generate_reply,
        messages=[{"role": "user", "content": message}],
    )

    raw = (raw or "").strip()

    if "STATUS: PASS" in raw:
        answer_part = raw.split("ANSWER:", 1)[-1].strip() if "ANSWER:" in raw else answer
        return {"status": "PASS", "answer": answer_part}

    critique_part = raw.split("CRITIQUE:", 1)[-1].strip() if "CRITIQUE:" in raw else raw
    return {"status": "FAIL", "critique": critique_part}