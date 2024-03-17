from fastapi import FastAPI, HTTPException, Request, Body
from survey_bot_v1 import SurveyBotV1
from request import FormRequest, UserRequest
from model import FormModel
from typing import List
from response import HistoryMessage, FollowUpResponse
import logging
import uuid
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

survey_store = {}

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
	app.mongodb_client = AsyncIOMotorClient("localhost:27017",uuidRepresentation="standard")
	app.mongodb = app.mongodb_client["dynamic-survey"]


@app.on_event("shutdown")
async def shutdown_db_client():
	app.mongodb_client.close()

@app.post("/store_data/")
async def store_data(request: Request, formRequest: FormRequest = Body(...)):
	created_form = None
	if formRequest.form_id is not None:
		created_form = await request.app.mongodb["forms"].find_one(
			{"_id": str(formRequest.form_id)}
		)

		if created_form is None:
			raise HTTPException(status_code=404, detail="Form ID to be updated not found") 
		
		created_form["questions"] = formRequest.questions
		await request.app.mongodb["forms"].update_one(
			{"_id": formRequest.form_id}, {"$set": jsonable_encoder(created_form)}
		)
	else:
		form_model = FormModel(questions=formRequest.questions)
		new_form = await request.app.mongodb["forms"].insert_one(jsonable_encoder(form_model))
		created_form = await request.app.mongodb["forms"].find_one(
			{"_id": new_form.inserted_id}
		)
	
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