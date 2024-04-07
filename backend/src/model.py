from request import Question
from survey_bot_v1 import SurveyBotV1
from pydantic import BaseModel, Field
from typing import List
import uuid

class SurveyBotV1Model(BaseModel):
	hash_id : int = Field(alias="_id")
	SurveyBotV1 : SurveyBotV1

	class Config:
		populate_by_name = True
		json_schema_extra =             {
                "example": {
                    "hash_id": "8362034428305540585",
                    "SurveyBotV1": {
                        "user_characteristics": {},
                        "chat_history": [
                            [
                                0,
                                "How would you rate the availability and affordability of healthcare services in your rural area?"
                            ]
                        ],
                        "fixed_questions": [
                            [
                                {
                                    "question": "How would you rate the availability and affordability of healthcare services in your rural area?",
                                    "question_config": {
                                        "followup_depth": 10,
                                        "criteria": [
                                            "The answer should have a perception healthcare availability in rural areas"
                                        ]
                                    }
                                },
                                [
                                    "The answer should have a perception healthcare availability in rural areas"
                                ]
                            ],
                            [
                                {
                                    "question": "Have you experienced any difficulties in accessing healthcare facilities due to distance or transportation issues?",
                                    "question_config": {
                                        "followup_depth": 3,
                                        "criteria": [
                                            "To evaluate the impact of distance and transportation on healthcare access in rural areas",
                                            "To identify areas where transportation infrastructure or services need improvement to enhance healthcare accessibility"
                                        ]
                                    }
                                },
                                [
                                    "To evaluate the impact of distance and transportation on healthcare access in rural areas",
                                    "To identify areas where transportation infrastructure or services need improvement to enhance healthcare accessibility"
                                ]
                            ],
                            [
                                {
                                    "question": "How satisfied are you with the quality of healthcare services, including the availability of medical professionals and equipment, in your rural area?",
                                    "question_config": {
                                        "followup_depth": 3,
                                        "criteria": [
                                            "To gauge satisfaction levels with the quality of healthcare services, identifying areas for improvement",
                                            "To assess the availability of medical professionals and equipment, highlighting any deficiencies in healthcare infrastructure"
                                        ]
                                    }
                                },
                                [
                                    "To gauge satisfaction levels with the quality of healthcare services, identifying areas for improvement",
                                    "To assess the availability of medical professionals and equipment, highlighting any deficiencies in healthcare infrastructure"
                                ]
                            ]
                        ],
                        "current_question_index": 0,
                        "current_question_followup_depth": 0,
                        "state": "in progress"
                    }
                }
            }
			

class FormModel(BaseModel):
    
	form_id : str = Field(default_factory=uuid.uuid4, alias="_id")
	questions : List[Question]

	class Config:
		populate_by_name = True
		json_schema_extra = {
			"example": {
				"form_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
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
		
class UserModel(BaseModel):
	email : str =  Field(alias="_id")
	filled_surveys : List[uuid.uuid4] = Field(default_factory=list)
	created_surveys : List[uuid.uuid4] = Field(default_factory=list)

	class Config:
		populate_by_name = True
		json_schema_extra = {
			"example": {
				"email": "abc@gmail.com",
				"filled_surveys": ["00010203-0405-0607-0809-0a0b0c0d0e0f", "510aeb2b-59af-4716-bbea-6198a423ea92"],
				"created_surveys": ["00010203-0405-0607-0809-0a0b0c0d0e0f"]
            }
		}