import requests

api_url = "http://127.0.0.1:8080/generate-response"

def generate_response(prompt, max_new_tokens=200):    
    # Prepare the request payload
    prompt_data = {"prompt": prompt, "max_new_tokens" : max_new_tokens}
    
    # Send the POST request
    response = requests.post(api_url, json=prompt_data)
    if response.status_code == 200:
        # The request was successful
        generated_text = response.json()["generated_text"]
        # print(f"Generated Text: {generated_text}")
        return generated_text
    else:
        # Something went wrong
        print(f"Error: {response.status_code}, {response.text}")
        return None

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
