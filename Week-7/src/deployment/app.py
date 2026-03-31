import sys, os, json, tempfile
from pathlib import Path
from datetime import datetime
import streamlit as st

SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_DIR))


try:
    from retriever.multimodal_retriever import retrieve_from_text, retrieve_from_image
    RETRIEVER_OK = True
except Exception as e:
    RETRIEVER_OK, RETRIEVER_ERROR = False, str(e)

try:
    from pipelines.sql_pipeline import answer_question as sql_answer_question
    SQL_OK = True
except Exception as e:
    SQL_OK, SQL_ERROR = False, str(e)

try:
    from memory.memory_store import save_message, get_last_n_messages
    MEMORY_OK = True
except Exception as e:
    MEMORY_OK = False

try:
    from evaluation.rag_eval import generate_answer, check_faithfulness, rewrite_query_with_history
    EVAL_OK = True
except Exception as e:
    EVAL_OK, EVAL_ERROR = False, str(e)

DB_PATH        = SRC_DIR / "data" / "enterprise.db"
CHAT_LOGS_FILE = SRC_DIR / "CHAT-LOGS.json"

st.set_page_config(page_title="Week-7 Dashboard")


def save_to_chat_log(entry):
    logs = []
    if CHAT_LOGS_FILE.exists():
        try: logs = json.loads(CHAT_LOGS_FILE.read_text())
        except: pass
    entry["timestamp"] = datetime.now().isoformat()
    logs.append(entry)
    CHAT_LOGS_FILE.write_text(json.dumps(logs, indent=2))


def build_context(results):
    parts = []
    for i, r in enumerate(results):
        doc = r["doc"]
        src = Path(doc.metadata.get("source", "unknown")).name
        pg  = doc.metadata.get("page", "?")
        parts.append(f"[Chunk {i+1}] {src} (p{pg})\n{doc.page_content.strip()}")
    return "\n\n---\n\n".join(parts)


def get_history():
    return get_last_n_messages() if MEMORY_OK else []



def show_text_answer(question, text_results, mode):
    if not text_results:
        return st.info("No relevant text found.")
    if not EVAL_OK:
        return st.error(EVAL_ERROR)

    context = build_context(text_results)
    with st.spinner("Generating answer..."):
        answer = generate_answer(question, context, get_history())
    score = check_faithfulness(answer, context)

    st.subheader("💬 Answer")
    st.write(answer)
    col1, col2 = st.columns(2)
    col1.write(f"Faithfulness: {score:.0%}")
    col2.write(f"Chunks used: {len(text_results)}")

    if MEMORY_OK:
        save_message("user", question)
        save_message("assistant", answer)
    save_to_chat_log({"mode": mode, "question": question, "answer": answer, "faithfulness": score})


def show_images(results, question):
    st.subheader("Images")
    if not results:
        return st.info("No images found.")
    cols = st.columns(min(3, len(results)))
    for i, r in enumerate(results):
        with cols[i % len(cols)]:
            path = r.get("image_path", "")
            if path and os.path.exists(path):
                st.image(path)
            st.caption(r.get("filename", "unknown"))
            st.caption(f"Similarity: {r.get('similarity', 0):.2f}")
    save_to_chat_log({"mode": "image", "question": question, "count": len(results)})



def handle_text(question, mode):
    query = rewrite_query_with_history(question, get_history()) if EVAL_OK else question
    res   = retrieve_from_text(query, top_k_text=5 if "Text" in mode else 0, top_k_images=3 if "Images" in mode else 0)
    if "Text"   in mode: show_text_answer(question, res.get("text_results", []),  "text")
    if "Images" in mode: show_images(res.get("image_results", []), question)


def handle_image(path, name, mode):
    res = retrieve_from_image(path, top_k_text=5, top_k_images=3)
    if "Text"   in mode: show_text_answer(res.get("derived_query", name), res.get("text_results", []), "image_text")
    if "Images" in mode: show_images(res.get("image_results", []), name)


def handle_sql(question):
    res = sql_answer_question(question, str(DB_PATH))
    if not res["success"]:
        return st.error(res["error"])
    st.subheader("Generated SQL")
    st.code(res["sql"], language="sql")
    st.subheader("Answer")
    st.write(res["answer"])




def main():
    st.title("Week-7 Dashboard")
    tab1, tab2 = st.tabs(["Ask", "SQL"])

    with tab1:
        subtab1, subtab2 = st.tabs(["Text Query", "Image Upload"])

        with subtab1:
            q    = st.text_input("Ask something")
            mode = st.radio("Mode", ["Text only", "Images only", "Text + Images"], key="text_mode")
            if st.button("Search", key="text_search"):
                if q.strip(): handle_text(q, mode)
                else: st.warning("Please enter a question.")

        with subtab2:
            file = st.file_uploader("Upload image")
            mode = st.radio("Mode", ["Text only", "Images only", "Text + Images"], key="image_mode")
            if file: st.image(file, caption="Uploaded Image", width=250)
            if st.button("Search Image", key="image_search"):
                if file is None:
                    st.warning("Please upload an image first.")
                else:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    try:    handle_image(tmp_path, file.name, mode)
                    finally:
                        try: os.unlink(tmp_path)
                        except: pass

    with tab2:
        q_sql = st.text_input("Ask database")
        if st.button("Query", key="sql_query"):
            if not q_sql.strip():       st.warning("Please enter a question.")
            elif not SQL_OK:            st.error(SQL_ERROR)
            elif not DB_PATH.exists():  st.error("Database not found.")
            else:                       handle_sql(q_sql)

if __name__ == "__main__":
    main()