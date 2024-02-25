from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from survey_bot_v1 import SurveyBotV1

app = FastAPI()

class UserRequest(BaseModel):
	email: str
	form_id: int
	user_answer: str

# Temporary persistence work around
survey_store = {}

@app.post("/get_next_question/")
async def generate_follow_up(userRequest: UserRequest):
	try:
		user_answer = userRequest.user_answer
		email = userRequest.email
		form_id = userRequest.form_id
		survey_bot = None
		if (email, form_id) in survey_store:
			survey_bot = survey_store[(email, form_id)]
		else:
			survey_bot = SurveyBotV1()
		next_question = survey_bot.get_next_question(user_answer)
		return {"next_question": next_question}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
