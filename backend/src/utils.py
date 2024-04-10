import requests
import traceback
from config_loader import app_config

def generate_response(prompt, temperature, max_tokens):
    message_data = {
        "model": app_config["llm-server"]["model"],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        # Request for chat completions
        completions_response = requests.post(
            app_config["llm-server"]["url"]+app_config["llm-server"]["endpoint"],
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

def initialize_pydantic_from_dict(model_cls, data_dict):
    """
    Initialize a Pydantic object from a dictionary, sending missing fields as None.

    Args:
        model_cls (type): Pydantic model class.
        data_dict (dict): Dictionary containing data for the model.

    Returns:
        model_cls: Initialized Pydantic object.
    """
    # Get all fields from the Pydantic model class
    fields = model_cls.__fields__
    print(fields)

    # Prepare kwargs for initializing the Pydantic object
    kwargs = {field: data_dict.get(field) for field in fields}

    # Initialize the Pydantic object
    return model_cls(**kwargs)
