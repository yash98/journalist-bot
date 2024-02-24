from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

model_name = "microsoft/phi-2"

pipe = pipeline(
    "text-generation",
    model=model_name,
    device=0,
    trust_remote_code=True,
)

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 150
    do_sample: bool = True
    temperature: float = 0.001
    top_k: int = 50
    top_p: float = 0.95

@app.post("/generate-response")
def generate_response_endpoint(prompt_request: PromptRequest):
    try:
        prompt = prompt_request.prompt
        max_new_tokens = prompt_request.max_new_tokens
        do_sample = prompt_request.do_sample
        temperature = prompt_request.temperature
        top_k = prompt_request.top_k
        top_p = prompt_request.top_p

        # Generate response using the model with custom parameters
        outputs = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=do_sample,
                       temperature=temperature, top_k=top_k, top_p=top_p)
        generated_text = outputs[0]["generated_text"]

        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
