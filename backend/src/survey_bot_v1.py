from pydantic import BaseModel
from typing import List, Dict, Union, Tuple

class QuestionConfig(BaseModel):
	followup_depth: int
	criteria: List[str]

class Question(BaseModel):
	question: str
	question_config: QuestionConfig

class SurveyBotV1(BaseModel):
	question_generation_agent = question_generation_agent
	objective_met_agent = objective_met_agent
	user_characteristics: Dict[str, Union[str, int, float, bool, None]] = {}
	chat_history: List[List[Tuple[int, str, str]]] = []
	fixed_questions: List[Tuple[Question, List[str]]] = []
	current_question_index: int = 0
	current_question_followup_depth: int = 0

	def get_next_question(user_answer: str):
		objective_remaining_list = question_generation_agent(chat_history, \
		fixed_questions[current_question_index].question, fixed_questions[current_question_index][1])
		if len(objective_remaining_list) == 0 or current_question_followup_depth >= fixed_questions[current_question_index][0].question_config.followup_depth:
			current_question_index += 1
			current_question_follow_up_depth = 0
			if len(fixed_questions) > current_question_index:
				return fixed_questions[current_question_index]
			else:
				None
		
		current_question_follow_up_depth += 1
		return question_generation_agent(chat_history, fixed_questions[current_question_index][0].question, \
			fixed_questions[current_question_index][1], user_charecteristics)
	