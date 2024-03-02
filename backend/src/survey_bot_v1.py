from pydantic import BaseModel
from typing import List, Dict, Union, Tuple
from check_objective import objective_met_agent
from generate_question import question_generation_agent
from request import Question
from response import HistoryMessage

import concurrent.futures

PARALLEL_WORKERS = 4
parallel_objective_met_agent_executor = concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_WORKERS)

class SurveyBotV1(BaseModel):
	question_generation_agent = question_generation_agent
	objective_met_agent = objective_met_agent
	user_characteristics: Dict[str, Union[str, int, float, bool, None]] = {}
	# List of tuples of main question index, main question or followup question, user answer
	chat_history: List[Tuple[int, str, str]] = []
	# List of tuples of question and its left criteria
	fixed_questions: List[Tuple[Question, List[str]]] = []
	current_question_index: int = 0
	current_question_followup_depth: int = 0

	def append_question_to_chat_history(self, question: str):
		self.chat_history.append((self.current_question_index, question, None))

	def __init__(self, questions):
		super().__init__()
		self.fixed_questions = [(question, question.question_config.criteria) for question in questions]
		next_question = self.fixed_questions[self.current_question_index][0].question
		self.append_question_to_chat_history(next_question)

	def parallel_objective_met_agent(self):
		futures = [parallel_objective_met_agent_executor.submit(objective_met_agent, \
			self.transform_chat_history(self.chat_history), self.fixed_questions[self.current_question_index][0].question, criteria) \
			for criteria in self.fixed_questions[self.current_question_index][1]]
		results = [future.result() for future in concurrent.futures.as_completed(futures)]
		objective_left_list = [criteria for criteria, result in zip(self.fixed_questions[self.current_question_index][1], results) if not result]
		return objective_left_list
	
	def transform_chat_history(self, chat_history: List[Tuple[int, str, str]], question_prefix="Interviewer: ", answer_prefix="Participant: ") -> str:
		chat_history_str = ""
		for chat in chat_history:
			question = chat[1]
			answer = chat[2]

			if question is not None and len(question) > 0:
				chat_history_str += question_prefix + question + "\n"

			if answer is not None and len(answer) > 0:
				chat_history_str += answer_prefix + answer + "\n"
		return chat_history_str

	def get_next_question(self, user_answer: str):
		if len(self.chat_history) == 0:
			next_question = self.fixed_questions[self.current_question_index][0]
			self.append_question_to_chat_history(next_question)
			return next_question

		# Add answer to chat history
		last_tuple = self.chat_history[-1]
		self.chat_history[-1] = (self.current_question_index, last_tuple[1], user_answer)

		objective_remaining_list = self.parallel_objective_met_agent()
		self.fixed_questions[self.current_question_index] = (self.fixed_questions[self.current_question_index][0], objective_remaining_list)

		if len(objective_remaining_list) == 0 or self.current_question_followup_depth >= self.fixed_questions[self.current_question_index][0].question_config.followup_depth:
			self.current_question_index += 1
			self.current_question_follow_up_depth = 0
			if len(self.fixed_questions) > self.current_question_index:
				next_question = self.fixed_questions[self.current_question_index][0].question
				self.append_question_to_chat_history(next_question)
				return next_question
			else:
				return None
		
		current_question_follow_up_depth += 1
		next_question = self.question_generation_agent(self.transform_chat_history(self.chat_history), self.fixed_questions[self.current_question_index][0].question, \
			self.fixed_questions[self.current_question_index][1], self.user_charecteristics)
		self.append_question_to_chat_history(next_question)
		return next_question
	
	def get_chat_history(self) -> List[HistoryMessage]:
		history = []
		for chat in self.chat_history:
			question = chat[1]
			answer = chat[2]

			if question is not None and len(question) > 0:
				history.append(HistoryMessage(role="assistant", content=question))

			if answer is not None and len(answer) > 0:
				history.append(HistoryMessage(role="user", content=question))
		return history

	