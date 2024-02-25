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