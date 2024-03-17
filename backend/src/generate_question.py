import requests
import re
import traceback

completions_url = "http://localhost:8000/v1/chat/completions"

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
    print("Prompt for Question generation: \n", prompt)
    response =  generate_response(prompt, temperature=0, max_tokens=150)

    # Use regular expressions to parse the llm output
    # end_of_turn_tags = re.findall(r'<start_of_turn>model(.*?)<eos>', response, re.DOTALL)
    # parsed_response = end_of_turn_tags[0].strip().strip('"').strip("'")
    parsed_response = response.strip().strip('"').strip("'")

    print("Parsed LLM response for Question generation: \n", parsed_response)
    return parsed_response
