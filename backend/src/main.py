from fastapi import FastAPI, HTTPException, Request, Body
from survey_bot_v1 import SurveyBotV1
from request import FormRequest, UserRequest
from model import *
from typing import List
from response import HistoryMessage, FollowUpResponse
import logging
import uuid
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from google.oauth2 import id_token
from google.auth.transport import requests
from constants import *
from config_loader import *

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
	authorization_token = request.headers.get(AUTH_HEADER_KEY)
	id_info = None
	try:
		id_info = id_token.verify_oauth2_token(authorization_token, requests.Request(), GOOGLE_OATH_CLIENT_ID)
	except Exception as e:
		logging.exception("Failed with auth error: " + str(e))
		raise HTTPException(status_code=401, detail="Invalid token")
	# print("id_info: ", id_info)
	email = id_info["email"]

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

		created_user = await request.app.mongodb["users"].find_one(
			{"_id": email}
		)
		if created_user is None:
			users_model = UserModel(_id=email, created_surveys=[uuid.UUID(new_form.inserted_id),])
			await request.app.mongodb["users"].insert_one(jsonable_encoder(users_model))
		else:
			created_user["created_surveys"].append(uuid.UUID(new_form.inserted_id))
			await request.app.mongodb["users"].update_one(
				{"_id": email}, {"$set": jsonable_encoder(created_user)}
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
		survey_bot = SurveyBotV1().init_with_questions(created_form.questions)
		survey_bot_model = SurveyBotV1Model(hash_id=get_hash(email, form_id), SurveyBotV1=survey_bot)
		mongodb["survey_bot"].insert_one(jsonable_encoder(survey_bot_model))
		return survey_bot
	return None

@app.post("/user/get_next_question")
async def generate_follow_up(userRequest: UserRequest, request: Request):
	authorization_token = request.headers.get(AUTH_HEADER_KEY)
	id_info = None
	try:
		id_info = id_token.verify_oauth2_token(authorization_token, requests.Request(), GOOGLE_OATH_CLIENT_ID)
	except Exception as e:
		logging.exception("Failed with auth error: " + str(e))
		raise HTTPException(status_code=401, detail="Invalid token")
	# print("id_info: ", id_info)
	email = id_info["email"]

	try:
		user_answer = userRequest.user_answer
		form_id = userRequest.form_id
		hash_id = get_hash(email, form_id)
		print("hash_id: ", hash_id)
		survey_bot_model = await request.app.mongodb["survey_bot"].find_one(
			{"_id": hash_id}
		)
		print("survey_bot_model: ", survey_bot_model)
		if survey_bot_model is None:
			raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
		survey_bot = SurveyBotV1(**survey_bot_model["SurveyBotV1"])
		(next_question, state) = survey_bot.get_next_question(user_answer)
		survey_bot_model["SurveyBotV1"] = survey_bot
		print(survey_bot)
		await request.app.mongodb["survey_bot"].update_one(
			{"_id": hash_id}, {"$set": jsonable_encoder(survey_bot_model)}
		)
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
async def get_history(form_id: uuid.UUID, request: Request) -> List[HistoryMessage]:
	authorization_token = request.headers.get(AUTH_HEADER_KEY)
	id_info = None
	try:
		id_info = id_token.verify_oauth2_token(authorization_token, requests.Request(), GOOGLE_OATH_CLIENT_ID)
	except Exception as e:
		logging.exception("Failed with auth error: " + str(e))
		raise HTTPException(status_code=401, detail="Invalid token")
	# print("id_info: ", id_info)
	email = id_info["email"]

	hash_id = get_hash(email, form_id)
	print("hash_id: ", hash_id)
	try:
		survey_bot_model = await request.app.mongodb["survey_bot"].find_one(
			{"_id": hash_id}
		)
		print("survey_bot_model: ", survey_bot_model)
		survey_bot = None
		if survey_bot_model is not None:
			survey_bot = SurveyBotV1(**survey_bot_model["SurveyBotV1"])
		else:
			survey_bot = await create_new_survey_bot(email, form_id, request.app.mongodb)
		
		if not survey_bot:
			raise HTTPException(status_code=404, detail="Survey bot for Email, Form ID pair not found")
			
		created_user = await request.app.mongodb["users"].find_one(
				{"_id": email}
			)
		if created_user is None:
			users_model = UserModel(_id=email, filled_surveys=[form_id])
			await request.app.mongodb["users"].insert_one(jsonable_encoder(users_model))
		else:
			created_user["created_surveys"].append(form_id)
			await request.app.mongodb["users"].update_one(
				{"_id": email}, {"$set": jsonable_encoder(created_user)}
			)
		
		return survey_bot.get_chat_history()
	except Exception as e:
		logging.exception("/user/get_history failed email: " + email + " form_id: " + str(form_id) + " error: " + str(e))
		raise HTTPException(status_code=500, detail=str(e))