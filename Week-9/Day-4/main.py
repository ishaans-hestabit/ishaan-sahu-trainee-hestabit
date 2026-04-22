import os
import sqlite3
import warnings
import autogen
warnings.filterwarnings("ignore", message="Cost calculation not available")
from dotenv import load_dotenv
from memory.session_memory import add_to_session, get_session_context
from memory.vector_store import add_to_vector_store, search_vector_store

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to .env"
    )

DB_PATH = "memory/long_term.db"


def get_llm_config():
    return {
        "config_list": [
            {
                "model": "llama-3.3-70b-versatile",
                "api_key": GROQ_API_KEY,
                "api_type": "groq",
                "price": [0, 0],
            }
        ],
        "temperature": 0.3,
        "cache_seed": None,
    }


def init_db():
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_fact(fact: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO facts (fact) VALUES (?)", (fact,))
    conn.commit()
    conn.close()


def get_facts():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT fact FROM facts ORDER BY created_at DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return [row[0] for row in rows]


def extract_fact(query: str, response: str, agent: autogen.AssistantAgent) -> str:
    result = agent.generate_reply(messages=[{
        "role": "user",
        "content": (
            f"From this exchange, extract ONE short fact worth remembering "
            f"for future conversations (e.g. user preferences, names, key topics).\n"
            f"If nothing is worth remembering, reply with exactly: NONE\n\n"
            f"Query: {query}\nResponse: {response}"
        )
    }])
    fact = (result.get("content") if isinstance(result, dict) else result or "").strip()
    return None if not fact or fact.upper() == "NONE" else fact


def build_prompt(query: str) -> tuple[str, list[str]]:
    memory_used = []
    prompt = query

    session_context = get_session_context()
    if session_context:
        prompt = f"Conversation so far:\n{session_context}\n\nUser: {query}"
        memory_used.append("session")

    
    background = []

    similar = search_vector_store(query, top_k=3)
    if similar:
        items = "\n".join(f"- {item}" for item in similar)
        background.append(f"[Similar past conversations]\n{items}")
        memory_used.append("vector")

    facts = get_facts()
    if facts:
        items = "\n".join(f"- {fact}" for fact in facts)
        background.append(f"[Known facts]\n{items}")
        memory_used.append("long-term")

    if background:
        prompt += (
            "\n\n--- optional background (use only if relevant) ---\n"
            + "\n\n".join(background)
            + "\n---"
        )

    return prompt, memory_used


def main():
    init_db()
    llm_config = get_llm_config()

    agent = autogen.AssistantAgent(
        name="MemoryAgent",
        system_message="""You are a helpful, knowledgeable assistant.
            Answer the user's question directly and accurately.
            You may receive context from past conversations — use it ONLY if
            it is genuinely relevant to the current question.
            If the context is unrelated, ignore it completely and just answer
            the question from your own knowledge.
            Be concise and clear. Never mention the memory system to the user.""",
        llm_config=llm_config,
    )

    print()
    print("========================================")
    print("||   Day 4 - Memory-Augmented Agent     ||")
    print("||   Session - Vector - Long-Term       ||")
    print("========================================")
    print("  Type your question below.")
    print("  Type 'quit' to exit.\n")

    while True:
        try:
            query = input("-> You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if query.lower() == "quit":
            print("Goodbye.")
            break
        if not query:
            continue

        prompt, _ = build_prompt(query)

        try:
            result = agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )

            response = (result.get("content") if isinstance(result, dict) else result or "").strip()

            print(f"\n  {response}\n")

           
            add_to_session("user", query)
            add_to_session("agent", response)
            add_to_vector_store(f"User asked: {query}\nAgent answered: {response}")

            fact = extract_fact(query, response, agent)
            if fact:
                save_fact(fact)
        except Exception as e:
            print(f"\n  Error: {e}\n  Please try again.\n")


if __name__ == "__main__":
    main()