import streamlit as st

USER_INPUT_KEY = "user_inputs"

QUESTION_KEY = "question"
OBJECTIVE_KEY = "objective"

def add_empty_question():
    st.session_state[USER_INPUT_KEY].append({QUESTION_KEY: "", OBJECTIVE_KEY: [""]})

def add_empty_objective(id_q):
    st.session_state[USER_INPUT_KEY][id_q][OBJECTIVE_KEY].append("")

def display_survey():
    for id_q, input_data in enumerate(st.session_state[USER_INPUT_KEY], start=0):
        saved_question = input_data[QUESTION_KEY]
        saved_objective = input_data[OBJECTIVE_KEY]
        question = st.text_area(f"Enter the question {id_q+1}:", key=f"q_{id_q}")
        for id_o, obj in enumerate(saved_objective, start=0):
            objective = st.text_area(f"Enter question {id_q+1} objective {id_o+1}:", key=f"o_{id_q}_{id_o}")
        if st.button("Add Objective", key=f"aob_{id_q}"):
            add_empty_objective(id_q)
            st.rerun()
    if st.button("Add Question"):
        add_empty_question()
        st.rerun()

def update_user_input_based_on_session_keys():
    for key in st.session_state.keys():
        if key.startswith("q_"):
            id_q = int(key.split("_")[1])
            st.session_state[USER_INPUT_KEY][id_q][QUESTION_KEY] = st.session_state[key]
        elif key.startswith("o_"):
            id_q = int(key.split("_")[1])
            id_o = int(key.split("_")[2])
            st.session_state[USER_INPUT_KEY][id_q][OBJECTIVE_KEY][id_o] = st.session_state[key]

def survey():
    # Initialize an empty list to store user inputs
    if USER_INPUT_KEY not in st.session_state:
        st.session_state[USER_INPUT_KEY] = []
        add_empty_question()

    update_user_input_based_on_session_keys()
    display_survey()

    if st.button("Submit Survey"):
        update_user_input_based_on_session_keys()
        st.write(st.session_state[USER_INPUT_KEY])

survey()