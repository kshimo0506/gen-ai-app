import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets.GoogleAPI.google_api_key)

model = genai.GenerativeModel("gemini-pro")

if "chat" not in st.session_state:
    st.session_state["chat"] = model.start_chat(history=[])

def communicate():
    chat = st.session_state["chat"]
    chat.send_message(st.session_state["user_input"])
    st.session_state["chat"] = chat
    st.session_state["user_input"] = ""

st.title("Gen-AI-Chatbot")
st.write("生成AIを使ったチャットボットです。")

if st.session_state["chat"]:
    chat = st.session_state["chat"]

    for message in chat.history:
        if message.role == "user":
            speaker = "🙂"
        if message.role == "model":
            speaker="🤖"
        st.write(speaker + ": " + message.parts[0].text)

st.text_area("メッセージを入力してください。", key="user_input", placeholder="ここにメッセージを入力してください")
st.button("送信", key="submit", on_click=communicate)