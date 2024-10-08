import streamlit as st
import requests
from constants import *
from utils import *

backend_url = "http://127.0.0.1:8080"

COMPLETION_STATUS="completed"

def state_values_exists_eq(key, value):
    return key in st.session_state and st.session_state[key] == value

def fill_survery():
    refresh_token_if_needed()
    st.title("Fill Survey")
    if not state_values_exists_eq("survey_started", True):
        st.session_state.form_id = st.text_input("Enter form id:")

    if state_values_exists_eq("survey_started", True):
        chat()
    else:
        if st.button("Start Survey"):
            st.session_state.survey_started = True
            chat()

def generate_bot_response(prompt_input):
    headers = {}
    if SESSION_TOKEN_KEY in st.session_state and SESSION_ID_TOKEN_KEY in st.session_state[SESSION_TOKEN_KEY]:
        headers[AUTH_HEADER_KEY] = st.session_state[SESSION_TOKEN_KEY][SESSION_ID_TOKEN_KEY]
    response = requests.post(backend_url+"/user/get_next_question", json={\
                            "form_id": st.session_state.form_id, "user_answer": prompt_input}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Oops! Something went wrong. Please try reloading the page")
        st.stop()
        return None

def get_chat_history():
    headers = {}
    if SESSION_TOKEN_KEY in st.session_state and SESSION_ID_TOKEN_KEY in st.session_state[SESSION_TOKEN_KEY]:
        headers[AUTH_HEADER_KEY] = st.session_state[SESSION_TOKEN_KEY][SESSION_ID_TOKEN_KEY]
    response = requests.get(\
        backend_url+"/user/get_history?"+"form_id="+str(st.session_state.form_id), \
            headers=headers)
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
        response = None
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_bot_response(prompt)
                if response["next_question"]:
                        st.write(response["next_question"])
        if response and response["status"] == COMPLETION_STATUS:
            st.stop()
        message = {"role": "assistant", "content": response["next_question"]}
        st.session_state.messages.append(message)


if __name__ == "__main__":
    fill_survery()