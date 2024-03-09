from pydantic import BaseModel
from typing import List

class QuestionConfig(BaseModel):
	followup_depth: int
	criteria: List[str]

class Question(BaseModel):
	question: str
	question_config: QuestionConfig