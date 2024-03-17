
from request import Question
from pydantic import BaseModel, Field
from typing import List
import uuid

class FormModel(BaseModel):
    
	form_id : str = Field(default_factory=uuid.uuid4, alias="_id")
	questions : List[Question]

	class Config:
		populate_by_name = True
		json_schema_extra = {
			"example": {
				"id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
				"questions": [
			{
				"question": 'How would you rate the availability and affordability of healthcare services in your rural area?',
				"question_config": {
				"followup_depth": 1,
				"criteria": [
					'The answer should have a perception healthcare availability in rural areas'
				]
				}
			},
			{
				"question": 'Have you experienced any difficulties in accessing healthcare facilities due to distance or transportation issues?',
				"question_config": {
				"followup_depth": 3,
				"criteria": [
					'To evaluate the impact of distance and transportation on healthcare access in rural areas',
					'To identify areas where transportation infrastructure or services need improvement to enhance healthcare accessibility'
				]
				}
			}
			]
			}
		}