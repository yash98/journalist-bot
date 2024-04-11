from pydantic import BaseModel
from typing import List, Dict, Union, Tuple
from check_objective import objective_met_agent as objective_met_agent
from generate_question import question_generation_agent as question_generation_agent
from request import Question
from response import HistoryMessage
import time

from utils import generate_response as call_llm_fn

import concurrent.futures

PARALLEL_WORKERS = 4
parallel_objective_met_agent_executor = concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_WORKERS)
COMPLETION_MESSAGE = "You have completed the survey. Thank you for your time!"
COMPLETED_STATUS = "completed"
IN_PROGRESS_STATUS = "in progress"

class SurveyBotV1(BaseModel):
	# List of tuples of main question index, main question or followup question, user answer
	chat_history: List[Tuple[int, str, str]] = []
	# List of tuples of question and its left criteria
	fixed_questions: List[Tuple[Question, List[str]]] = []
	current_question_index: int = 0
	current_question_followup_depth: int = 0
	state: str = IN_PROGRESS_STATUS

	def append_question_to_chat_history(self, question: str):
		self.chat_history.append((self.current_question_index, question, ""))

	def init_with_questions(self, questions):
		self.fixed_questions = [(question, question.question_config.criteria) for question in questions]
		next_question = self.fixed_questions[self.current_question_index][0].question
		self.append_question_to_chat_history(next_question)
		return self
	
	def __init__(self, **kwargs):
		# print(kwargs)
		# print type of each key in kwargs
		# for key, value in kwargs.items():
		# 	print(key, type(value))
		super().__init__(**kwargs)

	def parallel_objective_met_agent(self):
		start_time = time.time()
		last_question_chat_history = self.transform_chat_history(self.get_last_question_chat_history(self.chat_history))
		futures = [parallel_objective_met_agent_executor.submit(objective_met_agent, \
			call_llm_fn, last_question_chat_history, self.fixed_questions[self.current_question_index][0].question, criteria) \
			for criteria in self.fixed_questions[self.current_question_index][1]]
		results = [future.result() for future in concurrent.futures.as_completed(futures)]
		objective_left_list = [criteria for criteria, result in zip(self.fixed_questions[self.current_question_index][1], results) if not result]
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(f"parallel_objective_met_agent time taken: {elapsed_time} seconds")
		return objective_left_list
	
	def transform_chat_history(self, chat_history: List[Tuple[int, str, str]], question_prefix="Interviewer: ", answer_prefix="Interviewee: ") -> str:
		chat_history_str = ""
		for chat in chat_history:
			question = chat[1]
			answer = chat[2]

			if question is not None and len(question) > 0:
				chat_history_str += question_prefix + question + "\n"

			if answer is not None and len(answer) > 0:
				chat_history_str += answer_prefix + answer + "\n"
		return chat_history_str

	def get_last_question_chat_history(self, chat_history: List[Tuple[int, str, str]]) -> List[Tuple[int, str, str]]:
		chat_list = []
		for chat in chat_history:
			if chat[0] == self.current_question_index:
				chat_list.append(chat)
		return chat_list

	def get_next_question(self, user_answer: str):
		if (self.state == COMPLETED_STATUS):
			return (None, self.state)

		if len(self.chat_history) == 0:
			next_question = self.fixed_questions[self.current_question_index][0]
			self.append_question_to_chat_history(next_question)
			return (next_question, self.state)

		# Add answer to chat history
		last_tuple = self.chat_history[-1]
		self.chat_history[-1] = (last_tuple[0], last_tuple[1], user_answer)

		objective_remaining_list = self.fixed_questions[self.current_question_index][1]
		if self.current_question_followup_depth < self.fixed_questions[self.current_question_index][0].question_config.followup_depth:
			objective_remaining_list = self.parallel_objective_met_agent()
			self.fixed_questions[self.current_question_index] = (self.fixed_questions[self.current_question_index][0], objective_remaining_list)

		if len(objective_remaining_list) == 0 or self.current_question_followup_depth >= self.fixed_questions[self.current_question_index][0].question_config.followup_depth:
			self.current_question_index += 1
			self.current_question_followup_depth = 0
			if len(self.fixed_questions) > self.current_question_index:
				next_question = self.fixed_questions[self.current_question_index][0].question
				self.append_question_to_chat_history(next_question)
				return (next_question, self.state)
			else:
				self.state = COMPLETED_STATUS
				self.append_question_to_chat_history(COMPLETION_MESSAGE)
				return (COMPLETION_MESSAGE, self.state)
		
		self.current_question_followup_depth += 1
		start_time = time.time()
		# TODO user characteristic is not used and tested, so just passing empty dict. It's a hacky interim solution
		next_question = question_generation_agent(call_llm_fn, self.transform_chat_history(self.get_last_question_chat_history(self.chat_history)), self.fixed_questions[self.current_question_index][0].question, \
			self.fixed_questions[self.current_question_index][1], {})
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(f"question_generation_agent time taken: {elapsed_time} seconds")
		self.append_question_to_chat_history(next_question)
		return (next_question, self.state)
	
	def get_chat_history(self) -> List[HistoryMessage]:
		history = []
		for chat in self.chat_history:
			question = chat[1]
			answer = chat[2]

			if question is not None and len(question) > 0:
				history.append(HistoryMessage(role="assistant", content=question))

			if answer is not None and len(answer) > 0:
				history.append(HistoryMessage(role="user", content=answer))
		return history

	