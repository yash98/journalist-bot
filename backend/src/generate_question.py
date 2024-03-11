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
    You are an expert interviewer, your job is to generate 1 followup question based interview till now and the objective of the main question not been met till now.
    Do not generate answers. Be empathic to user. 
    
    The following are details you will use
    
    Main question: {main_question}
    Objectives left: {objectives_left}
    
    Chat history:-
    {chat_history}
    
    Generate exactly one follow-up question comes from the assistant to be readily sent to user in a friendly tone.
    Do not generate the questions that's already present in the chat history, however you can use different words in case of any ties
    """

def question_generation_agent(chat_history, main_question, objectives_left, user_charecteristics="calm and patient"):

    # fetch llm response
    prompt = prompt_template.format(chat_history=chat_history, main_question=main_question, objectives_left=objectives_left)
    print("Prompt for Question generation: ", prompt)
    response =  generate_response(prompt)

    # Use regular expressions to parse the llm output
    end_of_turn_tags = re.findall(r'<start_of_turn>model(.*?)<eos>', response, re.DOTALL)
    parsed_response = end_of_turn_tags[0].strip().strip('"').strip("'")

    print("Parsed LLM response :", parsed_response)
    return parsed_response
