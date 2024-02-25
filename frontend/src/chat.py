import streamlit as st
import requests

backend_url = "http://127.0.0.1:8080/get_next_question"

SUCCESS="success"
API_FAILURE="api failure"

def generate_bot_response(prompt_input):
    response = requests.post(backend_url, payload={"email": st.session_state.email, "form_id": st.session_state.form_id, "user_answer": prompt_input})
    if response.status_code == 200:
        output = (response.json()["next_question"], SUCCESS)
    else:
        output = (None, API_FAILURE)
    return output

def chat():
    STARTING_MSG = "What topic would you describe today?"

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": STARTING_MSG}]

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
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)