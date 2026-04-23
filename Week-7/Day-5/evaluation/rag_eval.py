import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")

GROQ_MODEL = "llama-3.3-70b-versatile"


def _call_llm(messages: list) -> str:
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY not found in .env file")

    client   = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def rewrite_query_with_history(question: str, chat_history: list) -> str:
    

    if not chat_history:
        return question

    if len(question.split()) > 8:
        return question

    recent = chat_history[-4:]
    history_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in recent
    )
    print(history_text + "---------$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--==============================================")
    prompt = (
        "You are a search query rewriter.\n\n"
        "Given this recent conversation:\n"
        f"{history_text}\n\n"
        f"And this new message from the user: \"{question}\"\n\n"
        "Rewrite the user's message as a clear, standalone search query "
        "that a search engine could understand WITHOUT the conversation context.\n"
        "Keep it concise (under 15 words).\n"
        "Return ONLY the rewritten query, nothing else."
    )

    try:
        rewritten = _call_llm([{"role": "user", "content": prompt}])
        
        if len(rewritten.split()) > 20 or len(rewritten) < 3:
            return question
        print(f"[Query Rewrite] '{question}' → '{rewritten}'")
        return rewritten
    except Exception as e:
        
        print(f"[Query Rewrite] Failed, using original: {e}")
        return question



def generate_answer(question: str, context: str, chat_history: list) -> str:

    system_message = {
        "role": "system",
        "content": (
            "You are a helpful assistant for an enterprise knowledge base.\n"
            "Answer the user's question using ONLY the information in the CONTEXT provided.\n"
            "If the context doesn't contain enough information, say: "
            "'I don't have enough information in the documents to answer this.'\n"
            "Do not make up facts. Be clear and concise.\n"
            "You have access to the conversation history above — use it to "
            "understand follow-up questions like 'tell me more' or 'explain that'."
        )
    }

    current_user_message = {
        "role": "user",
        "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"
    }

    messages = [system_message] + chat_history + [current_user_message]

    return _call_llm(messages)

