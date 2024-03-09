import streamlit as st
import requests

backend_url = "http://127.0.0.1:8080"

COMPLETION_STATUS="completed"

def generate_bot_response(prompt_input):
    response = requests.post(backend_url+"/user/get_next_question", json={"email": st.session_state.email, "form_id": st.session_state.form_id, "user_answer": prompt_input})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Oops! Something went wrong. Please try reloading the page")
        st.stop()
        return None

def get_chat_history():
    response = requests.get(backend_url+"/user/get_history?email="+st.session_state.email+"&form_id="+str(st.session_state.form_id))
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Oops! Something went wrong. Please try reloading the page")
        st.stop()
        return []

def chat():
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = get_chat_history()

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input("Write here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_bot_response(prompt)
                placeholder = st.empty()
                if response["next_question"]:
                        placeholder.markdown(response["next_question"])
                if response["status"] == COMPLETION_STATUS:
                    st.stop()
        message = {"role": "assistant", "content": response["next_question"]}
        st.session_state.messages.append(message)