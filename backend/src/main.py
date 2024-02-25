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

# form_id -> fixed questions
fixed_questions_store = {}

@app.post("/user/get_next_question")
async def generate_follow_up(userRequest: UserRequest):
	try:
		user_answer = userRequest.user_answer
		email = userRequest.email
		form_id = userRequest.form_id
		survey_bot = None
		if (email, form_id) in survey_store:
			survey_bot = survey_store[(email, form_id)]
		else:
			if form_id in fixed_questions_store:
				survey_bot = SurveyBotV1(fixed_questions_store[form_id])
				survey_store[(email, form_id)] = survey_bot
			else:
				raise HTTPException(status_code=404, detail="Form ID not found")
		next_question = survey_bot.get_next_question(user_answer)
		return {"next_question": next_question}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
