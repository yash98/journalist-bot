from pydantic import BaseModel
from typing import List, Optional
import uuid

class QuestionConfig(BaseModel):
	followup_depth: int
	criteria: List[str]

class Question(BaseModel):
	question: str
	question_config: QuestionConfig

class FormRequest(BaseModel):
	form_id : Optional[uuid.UUID]
	questions : List[Question]

class UserRequest(BaseModel):
	email: str
	form_id: uuid.UUID
	user_answer: str
