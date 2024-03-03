import streamlit as st
from chat import chat
# import streamlit_debug
# streamlit_debug.set(flag=True, wait_for_client=True, host='localhost', port=8765)

def state_values_exists_eq(key, value):
    return key in st.session_state and st.session_state[key] == value

def login():
    if not state_values_exists_eq("survey_started", True):
        st.title("Dynamic Survey")
        st.session_state.email = st.text_input("Enter your email:")
        st.session_state.form_id = st.text_input("Enter form id:")

    if state_values_exists_eq("survey_started", True):
        chat()
    else:
        if st.button("Start Survey"):
            st.session_state.survey_started = True
            chat()

if __name__ == "__main__":
    login()