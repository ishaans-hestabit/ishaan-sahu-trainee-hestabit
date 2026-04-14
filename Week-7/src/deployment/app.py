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

try:
    from evaluation.confidence_guard import (
        check_text_confidence,
        check_image_confidence,
        check_hallucination,
    )
    GUARD_OK = True
except Exception as e:
    GUARD_OK = False

DB_PATH           = SRC_DIR / "data" / "enterprise.db"
CHAT_LOGS_FILE    = SRC_DIR / "CHAT-LOGS.json"
QUERY_MIN_LEN     = 3
QUERY_MAX_LEN     = 300
CONTEXT_MAX_CHARS = 6000
CHAT_LOG_MAX      = 100

st.set_page_config(page_title="Week-7 Dashboard")

def validate_query(q: str):
    if len(q) < QUERY_MIN_LEN:
        return f"Query is too short. Please type at least {QUERY_MIN_LEN} characters."
    if len(q) > QUERY_MAX_LEN:
        return f"Query is too long. Please keep it under {QUERY_MAX_LEN} characters."
    return None


def save_to_chat_log(entry):
    logs = []
    if CHAT_LOGS_FILE.exists():
        try:
            logs = json.loads(CHAT_LOGS_FILE.read_text())
        except Exception:
            pass
    entry["timestamp"] = datetime.now().isoformat()
    logs.append(entry)
    logs = logs[-CHAT_LOG_MAX:]
    CHAT_LOGS_FILE.write_text(json.dumps(logs, indent=2))


def build_context(results):
    parts = []
    total = 0
    for i, r in enumerate(results):
        doc   = r["doc"]
        src   = Path(doc.metadata.get("source", "unknown")).name
        pg    = doc.metadata.get("page", "?")
        text  = doc.page_content.strip()
        chunk = f"[Chunk {i+1}] {src} (p{pg})\n{text}"
        if total + len(chunk) > CONTEXT_MAX_CHARS:
            break
        parts.append(chunk)
        total += len(chunk)
    return "\n\n---\n\n".join(parts)


def get_history():
    return get_last_n_messages() if MEMORY_OK else []


def show_text_answer(question, text_results, mode):
    if not EVAL_OK:
        st.error(EVAL_ERROR)
        return

    if GUARD_OK:
        conf = check_text_confidence(text_results)
        if not conf["ok"]:
            st.warning(conf["message"])
            
            return

    if not text_results:
        st.info("No relevant text found.")
        return

    context = build_context(text_results)

    with st.spinner("Generating answer..."):
        answer = generate_answer(question, context, get_history())

    faith_score      = check_faithfulness(answer, context)
    hallucination_ok = True
    hall_message     = ""

    if GUARD_OK:
        hall             = check_hallucination(answer, context)
        hallucination_ok = hall["ok"]
        hall_message     = hall["message"]

    st.subheader("Answer")
    st.write(answer)

    col1, col2, col3 = st.columns(3)
    col1.metric("Faithfulness", f"{faith_score:.0%}")
    col2.metric("Chunks used",  len(text_results))
    if GUARD_OK:
        col3.metric("Confidence", str(check_text_confidence(text_results)["score"]))

    if GUARD_OK:
        if hallucination_ok:
            st.success(hall_message)
        else:
            st.warning(hall_message)


    if MEMORY_OK:
        save_message("user",      question)
        save_message("assistant", answer)

    save_to_chat_log({
        "mode":             mode,
        "question":         question,
        "answer":           answer,
        "faithfulness":     faith_score,
        "hallucination_ok": hallucination_ok,
    })


def show_images(results, question):
    st.subheader("Images")

    if GUARD_OK:
        conf = check_image_confidence(results)
        if not conf["ok"]:
            st.warning(conf["message"])
            return

    if not results:
        st.info("No images found.")
        return

    cols = st.columns(min(3, len(results)))
    for i, r in enumerate(results):
        with cols[i % len(cols)]:
            path = r.get("image_path", "")
            if path and os.path.exists(path):
                st.image(path)
            else:
                st.caption("Image file not found on disk.")
            st.caption(r.get("filename", "unknown"))
            st.caption(f"Similarity: {r.get('similarity', 0.0):.0%}")
            cap = r.get("caption", "")
            if cap:
                st.caption(cap[:120])

    save_to_chat_log({"mode": "image", "question": question, "count": len(results)})


def handle_text(question, mode):
    err = validate_query(question)
    if err:
        st.warning(err)
        return

    query = rewrite_query_with_history(question, get_history()) if EVAL_OK else question
    res   = retrieve_from_text(
        query,
        top_k_text   = 5 if "Text"   in mode else 0,
        top_k_images = 3 if "Images" in mode else 0,
    )
    if "Text"   in mode:
        show_text_answer(question, res.get("text_results", []), "text")
    if "Images" in mode:
        show_images(res.get("image_results", []), question)


def handle_image(path, name, mode):
    res = retrieve_from_image(path, top_k_text=5, top_k_images=3)
    if "Text"   in mode:
        show_text_answer(res.get("derived_query", name), res.get("text_results", []), "image_text")
    if "Images" in mode:
        show_images(res.get("image_results", []), name)


def handle_sql(question):
    err = validate_query(question)
    if err:
        st.warning(err)
        return

    res = sql_answer_question(question, str(DB_PATH))
    if not res["success"]:
        st.error(res["error"])
        return

    st.subheader("Generated SQL")
    st.code(res["sql"], language="sql")

    if res.get("rows"):
        import pandas as pd
        st.subheader("Results")
        st.dataframe(pd.DataFrame(res["rows"], columns=res["columns"]))

    st.subheader("Answer")
    st.write(res["answer"])


def main():
    st.title("Week-7 Dashboard")

    if not RETRIEVER_OK:
        st.error(f"Retriever failed to load: {RETRIEVER_ERROR}")

    tab1, tab2 = st.tabs(["Ask", "SQL"])

    with tab1:
        subtab1, subtab2 = st.tabs(["Text Query", "Image Upload"])

        with subtab1:
            q    = st.text_input("Ask something", max_chars=QUERY_MAX_LEN)
            mode = st.radio("Mode", ["Text only", "Images only", "Text + Images"], key="text_mode")
            if st.button("Search", key="text_search"):
                if q.strip():
                    handle_text(q.strip(), mode)
                else:
                    st.warning("Please enter a question.")

        with subtab2:
            file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp", "bmp"])
            mode = st.radio("Mode", ["Text only", "Images only", "Text + Images"], key="image_mode")
            if file:
                st.image(file, caption="Uploaded Image", width=250)
            if st.button("Search Image", key="image_search"):
                if file is None:
                    st.warning("Please upload an image first.")
                else:
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=Path(file.name).suffix
                    ) as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    try:
                        handle_image(tmp_path, file.name, mode)
                    finally:
                        try:
                            os.unlink(tmp_path)
                        except Exception:
                            pass

    with tab2:
        q_sql = st.text_input("Ask database", max_chars=QUERY_MAX_LEN)
        if st.button("Query", key="sql_query"):
            if not q_sql.strip():
                st.warning("Please enter a question.")
            elif not SQL_OK:
                st.error(SQL_ERROR)
            elif not DB_PATH.exists():
                st.error("Database not found.")
            else:
                handle_sql(q_sql.strip())


if __name__ == "__main__":
    main()