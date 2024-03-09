import streamlit as st
import requests

BACKEND_URL = "http://localhost:8080"

USER_INPUT_KEY = "user_inputs"

QUESTION_KEY = "question"
OBJECTIVE_KEY = "objective"
FOLLOWUP_DEPTH_KEY = "followup_depth"

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

"""
curl -X POST -H "Content-Type: application/json" \
    -d '{"form_id":1001, "questions":[{"question":"How would you rate the availability and affordability of healthcare services in your rural area?","question_config":{"followup_depth":1,"criteria":["The answer should have a perception healthcare availability in rural areas"]}},{"question":"Have you experienced any difficulties in accessing healthcare facilities due to distance or transportation issues?","question_config":{"followup_depth":3,"criteria":["To evaluate the impact of distance and transportation on healthcare access in rural areas","To identify areas where transportation infrastructure or services need improvement to enhance healthcare accessibility"]}},{"question":"How satisfied are you with the quality of healthcare services, including the availability of medical professionals and equipment, in your rural area?","question_config":{"followup_depth":3,"criteria":["To gauge satisfaction levels with the quality of healthcare services, identifying areas for improvement","To assess the availability of medical professionals and equipment, highlighting any deficiencies in healthcare infrastructure"]}}]}' \
    http://localhost:8080/store_data/
"""
def make_submit_survey_call():
    # check if empty string in question or objective and exclude from new json payload object it before sending
    questions_list = [] 
    for input_data in st.session_state[USER_INPUT_KEY]:
        question_data = {}
        if input_data[QUESTION_KEY] == "":
            continue

        question_data["question"] = input_data[QUESTION_KEY]
        question_data["question_config"] = {}

        for objective in input_data[OBJECTIVE_KEY]:
            if objective != "":
                if "criteria" not in question_data["question_config"]:
                    question_data["question_config"]["criteria"] = []
                question_data["question_config"]["criteria"].append(objective)

        questions_list.append(question_data)

    data = {
        "form_id": None,
        "questions": questions_list
    }
    response = requests.post(BACKEND_URL+"/store_data/", json=data)
    return response

def survey_creator():
    if USER_INPUT_KEY not in st.session_state:
        st.session_state[USER_INPUT_KEY] = []
        add_empty_question()

    update_user_input_based_on_session_keys()
    display_survey()

    if st.button("Submit Survey"):
        update_user_input_based_on_session_keys()
        st.write(st.session_state[USER_INPUT_KEY])

survey_creator()