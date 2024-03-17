from pydantic import BaseModel
from typing import Optional

class HistoryMessage(BaseModel):
    role: str
    content: str

class FollowUpResponse(BaseModel):
	next_question: Optional[str]
	status: str