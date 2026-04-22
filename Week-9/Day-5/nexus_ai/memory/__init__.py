import os
import sqlite3
from nexus_ai.config import WORKSPACE_DIR
from nexus_ai.memory.session import add_to_session, get_session_context
from nexus_ai.memory.vector import add_to_vector_store, search_vector_store

_DB_PATH = os.path.join(WORKSPACE_DIR, "long_term.db")


def _init_db():
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


def _save_fact(fact):
    _init_db()
    conn = sqlite3.connect(_DB_PATH)
    conn.execute("INSERT INTO facts (fact) VALUES (?)", (fact,))
    conn.commit()
    conn.close()


def _get_facts():
    _init_db()
    conn = sqlite3.connect(_DB_PATH)
    rows = conn.execute("SELECT fact FROM facts ORDER BY created_at DESC LIMIT 10").fetchall()
    conn.close()
    return [r[0] for r in rows]


def build_memory_context(query):
    parts = []

    session = get_session_context()
    if session:
        parts.append(f"[Recent conversation]\n{session}")

    similar = search_vector_store(query, top_k=2)
    if similar:
        items = "\n".join(f"- {s}" for s in similar)
        parts.append(f"[Similar past tasks]\n{items}")

    facts = _get_facts()
    if facts:
        items = "\n".join(f"- {f}" for f in facts)
        parts.append(f"[Known facts]\n{items}")

    if parts:
        return "--- optional background (use only if relevant) ---\n" + "\n\n".join(parts) + "\n---\n\n"
    return ""


def update_memory(task, report):
    add_to_session("user", task)
    add_to_session("nexus", report[:300])
    add_to_vector_store(f"Task: {task}\nReport: {report[:400]}")
    _save_fact(f"Completed: {task[:100]}")
