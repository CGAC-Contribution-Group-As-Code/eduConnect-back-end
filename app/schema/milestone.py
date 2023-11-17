from datetime import datetime
from pydantic import BaseModel
from fastapi import UploadFile

class QuizBase(BaseModel):
    main_text:str
    answer:str
    write_time:datetime

class ContentBase(BaseModel):
    name:str
    size:int
    path:str
    quizs:list[QuizBase]|None=None

class MileStoneBase(BaseModel):
    _id: str    
    title: str
    desc:str
    last_modify: datetime
    contents:list[ContentBase]|None=None