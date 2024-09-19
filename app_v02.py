import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets.GoogleAPI.google_api_key)

model = genai.GenerativeModel("gemini-pro")

if "chat" not in st.session_state:
    st.session_state["chat"] = model.start_chat(history=[])

def communicate():
    try:
        chat = st.session_state["chat"]
        pre_prompt = ""

        pre_prompt_custom_role = ""
        pre_prompt_custom_target = ""
        pre_prompt_custom_condition = ""
        
        if st.session_state["custom_role"] != "":
            pre_prompt_custom_role = st.session_state["custom_role"] + "の役割で、"
        else:
            pre_prompt_custom_role = ""

        if st.session_state["custom_target"] != "":
            pre_prompt_custom_target = st.session_state["custom_target"] + "向けに、"
        else:
            pre_prompt_custom_target = ""

        if st.session_state["custom_condition"] != "":
            pre_prompt_custom_condition = st.session_state["custom_condition"] + "の条件で、"
        else:
            pre_prompt_custom_condition = ""

        if pre_prompt_custom_role == "" and pre_prompt_custom_target == "" and pre_prompt_custom_condition == "":
            pre_prompt = ""
        else:
            pre_prompt = pre_prompt_custom_role + pre_prompt_custom_target + pre_prompt_custom_condition + "次の質問に答えてください。\n"

        prompt = pre_prompt + st.session_state["user_input"]
        chat.send_message(prompt)
        st.session_state["chat"] = chat
        st.session_state["user_input"] = ""

    except Exception as e:
        st.error(f"エラーが発生しました： {e}")

st.title("Gen-AI-Chatbot")
st.write("生成AIを使ったチャットボットです。")

delimiter = "次の質問に答えてください。\n"

if st.session_state["chat"]:
    chat = st.session_state["chat"]

    for message in chat.history:
        message_text = ""
        if message.role == "user":
            speaker = "🙂"
            index = message.parts[0].text.find(delimiter)
            if index != -1:
                message_text = message.parts[0].text[index + len(delimiter):]
            else:
                message_text = message.parts[0].text
            print(message_text)
        if message.role == "model":
            speaker = "🤖"
            message_text = message.parts[0].text
        print(message_text)
        st.write(speaker + ": " + message_text)

st.text_area("メッセージを入力してください。", key="user_input", placeholder="ここにメッセージを入力してください")
st.button("送信", key="submit", on_click=communicate)
st.write("")
st.write("入力オプション(任意入力)")
st.text_input("どのような役割で回答してほしいですか？", key="custom_role", placeholder="例: 親切なアシスタント")
st.text_input("どのような人向けに回答してほしいですか？", key="custom_target", placeholder="例: 小学生向け")
st.text_input("どのような条件で回答してほしいですか？", key="custom_condition", placeholder="例: 300文字以内で")
