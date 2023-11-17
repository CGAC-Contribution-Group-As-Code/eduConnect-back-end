from pydantic import BaseModel

class Login(BaseModel):
    id: str
    pw: str

class Feedback(BaseModel):
    round_id:str
    milestone_id:str
    content_id:str
    round_id:str
    feedback:str
    is_ai:bool=False
