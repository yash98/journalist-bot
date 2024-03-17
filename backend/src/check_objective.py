import requests
import re
import traceback

completions_url = "http://localhost:8000/v1/chat/completions"
THRESH = 0.8

def generate_response(prompt, temperature, max_tokens):
    message_data = {
        "model": "TechxGenus/gemma-7b-it-GPTQ",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        # Request for chat completions
        completions_response = requests.post(
            completions_url,
            json=message_data,
            headers={"Content-Type": "application/json"}
        )
        # {'id': 'cmpl-8e05afc0c9704f4eaffd586d311d255f',
        # 'object': 'chat.completion',
        # 'created': 163914,
        # 'model': 'TechxGenus/gemma-7b-it-GPTQ',
        # 'choices': [{'index': 0,
        # 'message': {'role': 'assistant',
        #     'content': "Hi! 👋\n\nIt's nice to hear from you. What would you like to talk about today?"},
        # 'logprobs': None,
        # 'finish_reason': 'stop'}],
        # 'usage': {'prompt_tokens': 10, 'total_tokens': 33, 'completion_tokens': 23}}
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return ""

    if completions_response.status_code != 200:
        print(f"Error: {completions_response.status_code}, {completions_response.text}")
        return ""

    return completions_response.json()["choices"][0]["message"]["content"]

prompt_template = \
    """
You are an expert in understanding and rating interviews based on whether a question's objective is met.
---
Question: {main_question}
Objective of the question: {objectives_left}
---
Conversation:
{chat_history}
---
Based on your understanding of the conversation you must give a rating between 0.0 to 1.0 based on how well the conversation has met the objective of the question.
It can be ambiguous at times whether the objective is met or not, use logic about conversation to determine if the objective is met. 
You can be nit picky in determining whether the Interviewee has fulfilled the objective for the interviewer question or not.
Answer 1.0 when the conversation completely fulfills the objective, and 0.0 if it does not fulfill the objective of the question at all.
Otherwise answer a rating in between 0.0 to 1.0 if the conversation partially fulfills the objective, closer to 0.25 if conversation could meet the objective of the question better and closer to 0.75 if it almost fullfils the objective. 
Just give the Rating between 0.0 to 1.0. Do not say anything else.
    """

def objective_met_agent(chat_history, main_question, objectives_left):

    # fetch response from llm
    prompt = prompt_template.format(chat_history=chat_history, main_question=main_question, objectives_left=objectives_left)
    # print("***"+prompt+"***")
    response = generate_response(prompt, temperature=0, max_tokens=4)
    print(response)
    parsed_response = find_occurrences(response)
    print(parsed_response)
    return float(parsed_response) > THRESH


def find_occurrences(input_string):
    pattern = r'\b[0-1]\.[0-9]+'
    occurrences = re.findall(pattern, input_string)
    if len(occurrences)>0:
        return occurrences[-1]
    return 0.0
