#!/usr/bin/env python
# coding: utf-8

import requests
import re


THRESH = 0.7

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
You are an expert in rating surveys by single number, tracking the progress of conversation, questions & particpant's answer in the current context.
Users answer vaguely at times. You can detect when the user has fulfilled your motivation for your question and when not. You dont know how to write english, just numbers.

Question: {main_question}
Objective of the question: {objectives_left}

Chat history:-
{chat_history}

Based on your expert understanding you must give a number only on the conversation on how well the particpant's answer has met the objective of the question.
Answer 1.0 when the conversation completely fullfils the objective, 0.5 if it partially fullfils the objective and 0.0 if it does not fullfill the motivation of the question. \
Never ever not justify your answer. 
Give number between 0.0 to 1.0. Values could be 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 
    """

def objective_met_agent(chat_history, main_question, objectives_left):

    # fetch response from llm
    prompt = prompt_template.format(chat_history=chat_history, main_question=main_question, objectives_left=objectives_left)
    print("Objective Met Agent prompt: \n", prompt)
    response = generate_response(prompt)

    # Use regular expressions to parse llm output
    end_of_turn_tags = re.findall(r'<start_of_turn>model(.*?)<eos>', response, re.DOTALL)
    # parsed_response = end_of_turn_tags[0].strip().split('\n')[0]
    print("Objective Met Agent LLM response: \n", response)
    parsed_response = find_occurrences(response)
    print(parsed_response)
    return parsed_response >= THRESH


def find_occurrences(input_string):
    pattern = r'\b(?:0\.[1-9]|[1-9]\.[0-9]|1\.0)\b'
    occurrences = re.findall(pattern, input_string)
    if len(occurrences)>0:
        return float(occurrences[-1])
    return 0.0
