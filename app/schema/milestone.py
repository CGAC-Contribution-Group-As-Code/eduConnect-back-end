from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

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
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    desc:str
    last_modify: datetime|None=None
    contents:list[ContentBase]|None=None