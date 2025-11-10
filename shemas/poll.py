from pydantic import BaseModel, ConfigDict
from typing import List

class OptionCreate(BaseModel):
    text: str
    
class Option(OptionCreate):
    id: int
    votes: int
    poll_id: int

    model_config = ConfigDict(from_attributes=True)
    
    
class PollCreate(BaseModel):
    question: str
    options: List[OptionCreate]
    

class Poll(BaseModel):
    id: int
    question: str
    options: List[Option] = []

    model_config = ConfigDict(from_attributes=True)
    
class VoteCreate(BaseModel):
    option_id: int
