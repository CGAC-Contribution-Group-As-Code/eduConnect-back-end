from pydantic import BaseModel

class CreateRoom(BaseModel):
    name: str
    desc: str
    teacher: str
    student: list

class CreateQuestion(BaseModel):
    room_id: str
    writer: str
    desc: str


class CreateAnswer(BaseModel):
    question_id: str
    ans_writer: str
    answer: str

