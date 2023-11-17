from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class QuizBase(BaseModel):
    title: str
    desc: str
    type: str
    etc: list | None = []
    answer: str

class RoundBase(BaseModel):
    r_id: Optional[PyObjectId] = Field(alias="_id", default=None)
    quiz:list[QuizBase]|None=[]

class ContentBase(BaseModel):
    name:str
    size:int
    path:str
    roundes: list[RoundBase]|None = []


class MileStoneBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    desc:str
    last_modify: datetime|None=None
    contents:list[ContentBase]|None=[]

class ReadMileStoneBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    desc:str
    last_modify: datetime|None=None