from pydantic import BaseModel

class CreateRoom(BaseModel):
    name: str
    desc: str
    teacher: str
    student: list