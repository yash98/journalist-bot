from fastapi import FastAPI, HTTPException, Request, Body
from pydantic import BaseModel, Field
from survey_bot_v1 import SurveyBotV1
from request import Question
from typing import List, Optional
from response import HistoryMessage
import logging
import uuid
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient


MAX_UUID_RETRIES = 10

# Temporary persistence work around
survey_store = {}

# form_id -> fixed questions
fixed_questions_store = {}

app = FastAPI()

class FormRequest(BaseModel):
	form_id : str = Field(default_factory=uuid.uuid4, alias="_id")
	questions : List[Question]

	class Config:
		allow_population_by_field_name = True
		schema_extra = {
			"example": {
				"id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
				"questions": []
			}
		}


class UserRequest(BaseModel):
	email: str
	form_id: uuid.UUID
	user_answer: str

class FollowUpResponse(BaseModel):
	next_question: Optional[str]
	status: str

@app.on_event("startup")
async def startup_db_client():
	app.mongodb_client = AsyncIOMotorClient("localhost:27017")
	app.mongodb = app.mongodb_client["dynamic-survey"]


@app.on_event("shutdown")
async def shutdown_db_client():
	app.mongodb_client.close()

@app.post("/store_data/")
async def store_data(request: Request, formRequest: FormRequest = Body(...)):
	form_request = jsonable_encoder(formRequest)
	new_form = await request.app.mongodb["forms"].insert_one(form_request)
	created_form = await request.app.mongodb["forms"].find_one(
		{"_id": new_form.inserted_id}
	)
	
	print("value of created form : ", created_form)
	return {"form_id": created_form["_id"]}

def create_new_survey_bot(email: str, form_id: uuid.UUID):
	if form_id in fixed_questions_store:
		survey_bot = SurveyBotV1(fixed_questions_store[form_id])
		survey_store[(email, form_id)] = survey_bot
		return survey_bot
	return None

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
			raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
		(next_question, state) = survey_bot.get_next_question(user_answer)
		return FollowUpResponse(next_question=next_question, status=state)
	except Exception as e:
		logging.exception("/user/get_next_question userRequest: " + str(userRequest) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))

# Get API takes email and form_id as input and deletes the survey_bot object from the survey_store
@app.get("/user/clear_history")
async def clear_history(email: str, form_id: uuid.UUID):
	try:
		if (email, form_id) in survey_store:
			del survey_store[(email, form_id)]
			return {"message": "History cleared successfully"}
		return {"message": "No history found for given email and form_id"}
	except Exception as e:
		logging.exception("/user/clear_history failed email: " + email + " form_id: " + str(form_id) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))

# Get API takes email and form_id as input and returns the survey_bot object from the survey_store
@app.get("/user/get_history")
async def get_history(email: str, form_id: uuid.UUID) -> List[HistoryMessage]:
	try:
		if (email, form_id) in survey_store:
			return survey_store[(email, form_id)].get_chat_history()
		else:
			survey_bot = create_new_survey_bot(email, form_id)
			if survey_bot:
				return survey_bot.get_chat_history()
			else:
				raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
	except Exception as e:
		logging.exception("/user/get_history failed email: " + email + " form_id: " + str(form_id) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))