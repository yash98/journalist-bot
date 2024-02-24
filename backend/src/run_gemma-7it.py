from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from pydantic import BaseModel


app = FastAPI()

quantization_config = BitsAndBytesConfig(load_in_4bit=True)
token = "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"
tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it", token=token)
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b-it", quantization_config=quantization_config, token=token)

default_prompt="""You are an expert interviewer, your job is to generate 1 followup question based interview till now and the objective of the main question not been met till now.
If the question can be made personalised based on user's characteristic do it. Do not generate answers. Be empathic to user. The following are details you will use
Main question: 
What do you believe are the reasons behind the high school dropout rates before 10th grade in India?
Objectives Left:
Get to the root cause of drop rate before 10th grade. Did the user give an example for the main question?
User's characteristic:
city is tier 2, education is postgraduate
Generate exactly one follow-up question comes from the assistant to be readily sent to user in a friendly tone. Once you have some context on all goals, close coversation by a thanking for their time."""

class PromptRequest(BaseModel):
    chat_content: str
    max_new_tokens: int = 150

@app.post("/generate_follow_up/")
async def generate_follow_up(promptRequest: PromptRequest):
    try:
        chat_content = promptRequest.chat_content
        max_new_tokens = promptRequest.max_new_tokens
        chat = [{"role": "user", "content": chat_content}]
        print(chat)
        prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        outputs = model.generate(input_ids=inputs.to(model.device), max_new_tokens=max_new_tokens)
        generated_response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        return {"generated_follow_up": generated_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
