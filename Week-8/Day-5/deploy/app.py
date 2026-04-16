import streamlit as st
import requests
from config import MAX_NEW_TOKENS, TEMPERATURE, TOP_P, TOP_K

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Local LLM")
st.title("Local LLM — Week 8 Capstone")

st.sidebar.header("Generation Settings")
temperature = st.sidebar.slider("Temperature", 0.1, 1.5, TEMPERATURE, 0.1)
top_p       = st.sidebar.slider("Top-P",       0.1, 1.0, TOP_P,       0.05)
top_k       = st.sidebar.slider("Top-K",       1,   100, TOP_K,       1)
max_tokens  = st.sidebar.slider("Max Tokens",  50,  500, MAX_NEW_TOKENS, 50)

if "messages" not in st.session_state:
    st.session_state.messages = []

keywords = ["def ", "return ", "function", "SELECT", "<!DOCTYPE", "{", "=>"]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and any(w in msg["content"] for w in keywords):
            st.code(msg["content"])
        else:
            st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

   
    history = []
    msgs = st.session_state.messages 
    for i in range(0, len(msgs) - 1, 2):
        if i + 1 < len(msgs):
            history.append({
                "user": msgs[i]["content"],
                "assistant": msgs[i + 1]["content"]
            })

    # call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/chat", json={
                "message": user_input,
                "history": history,
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            })
            data = res.json()
            response = data["response"]
            elapsed = data["latency_sec"]
            req_id  = data["request_id"]

        if any(w in response for w in keywords):
            st.code(response)
        else:
            st.write(response)
        st.caption(f"⏱ {elapsed}s | request_id: {req_id}")

    st.session_state.messages.append({"role": "assistant", "content": response})