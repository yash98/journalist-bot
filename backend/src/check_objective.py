#!/usr/bin/env python
# coding: utf-8

import requests
import re

def generate_response(prompt, max_new_tokens=200):
    # Set the API endpoint URL
    api_url = "http://localhost:8000/generate_follow_up/"  # Update with your actual server URL

    # Prepare the request payload
    prompt_data = {"chat_content": prompt, "max_new_tokens" : max_new_tokens}

    # Send the POST request
    response = requests.post(api_url, json=prompt_data)

    if response.status_code == 200:
        # The request was successful
        generated_text = response.json()["generated_follow_up"]
        # print(f"Generated Text: {generated_text}")
        return generated_text
    else:
        # Something went wrong
        print(f"Error: {response.status_code}, {response.text}")
        return None

prompt_template = \
    """
    You are an expert in analysing survey questions & particpant's answer as per given chat history.
    
    Main question: {main_question}
    Objective: {objectives_left}
    
    Chat history:-
    {chat_history}
    
    Based on your analysis you can decide whether or not the particpant's answer meets the objective of the question asked.
    Answer "True" if it meets the objective and "False" if it does not. Only answer True or False and do not try to justify your answer.
    """

def objective_met_agent(chat_history, main_question, objectives_left):

    # fetch response from llm
    prompt = prompt_template.format(chat_history=chat_history, main_question=main_question, objectives_left=objectives_left)
    response = generate_response(prompt)

    # Use regular expressions to parse llm output
    end_of_turn_tags = re.findall(r'<start_of_turn>model(.*?)<eos>', response, re.DOTALL)
    parsed_response = end_of_turn_tags[0].strip().split('\n')[0]

    print("Parsed LLM response :", parsed_response)
    return parsed_response
