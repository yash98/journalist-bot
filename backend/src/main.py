from fastapi import FastAPI, HTTPException, Request, Body
from survey_bot_v1 import SurveyBotV1
from request import FormRequest, UserRequest
from model import FormModel, SurveyBotV1Model
from typing import List
from response import HistoryMessage, FollowUpResponse
import logging
import uuid
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

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

# Function to return Hash of form_id and email
def get_hash(email: str, form_id: uuid.UUID):
	return hash((email, form_id))

async def create_new_survey_bot(email: str, form_id: uuid.UUID, mongodb):
	created_form = await mongodb["forms"].find_one(
			{"_id": str(form_id)}
		)
	if created_form is not None:
		created_form = FormModel(**created_form)
		survey_bot = SurveyBotV1(created_form.questions)
		survey_bot_model = SurveyBotV1Model(hash_id=get_hash(email, form_id), SurveyBotV1=survey_bot)
		mongodb["survey_bot"].insert_one(jsonable_encoder(survey_bot_model))
		return survey_bot
	return None

@app.post("/user/get_next_question")
async def generate_follow_up(userRequest: UserRequest, request: Request):
	try:
		user_answer = userRequest.user_answer
		email = userRequest.email
		form_id = userRequest.form_id
		hash_id = get_hash(email, form_id)
		survey_bot_model = await request.app.mongodb["survey_bot"].find_one(
			{"_id": hash_id}
		)
		print(survey_bot_model)
		if survey_bot_model is None:
			raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
		survey_bot = SurveyBotV1(**survey_bot_model["SurveyBotV1"])
		(next_question, state) = survey_bot.get_next_question(user_answer)
		survey_bot_model["SurveyBotV1"] = survey_bot
		await request.app.mongodb["survey_bot"].insert_one(jsonable_encoder(survey_bot_model))
		return FollowUpResponse(next_question=next_question, status=state)
	except Exception as e:
		logging.exception("/user/get_next_question userRequest: " + str(userRequest) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/clear_history")
async def clear_history(email: str, form_id: uuid.UUID, request: Request):
	hash_id = get_hash(email, form_id)
	try:
		# delete document from survey_bot collection
		survey_bot_model = await request.app.mongodb["survey_bot"].find_one(
			{"_id": hash_id}
		)
		if survey_bot_model is not None:
			await request.app.mongodb["survey_bot"].delete_one(
				{"_id": hash_id}
			)
			return {"message": "History cleared successfully"}
		return {"message": "No history found for given email and form_id"}
	except Exception as e:
		logging.exception("/user/clear_history failed email: " + email + " form_id: " + str(form_id) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))

# Get API takes email and form_id as input and returns the survey_bot object from the survey_store
@app.get("/user/get_history")
async def get_history(email: str, form_id: uuid.UUID, request: Request) -> List[HistoryMessage]:
	hash_id = get_hash(email, form_id)
	try:
		survey_bot_model = await request.app.mongodb["survey_bot"].find_one(
			{"_id": hash_id}
		)
		print(survey_bot_model)
		if survey_bot_model is not None:
			survey_bot = SurveyBotV1(**survey_bot_model["SurveyBotV1"])
			return survey_bot.get_chat_history()
		else:
			survey_bot = await create_new_survey_bot(email, form_id, request.app.mongodb)
			if survey_bot:
				return survey_bot.get_chat_history()
			else:
				raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
	except Exception as e:
		logging.exception("/user/get_history failed email: " + email + " form_id: " + str(form_id) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))