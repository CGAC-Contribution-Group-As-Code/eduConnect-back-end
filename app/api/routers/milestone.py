from fastapi import APIRouter,Depends
from app.crud.milestone import *
from app.schema.milestone import *

router = APIRouter(prefix="/milestone")

@router.get("/",response_model=list[MileStoneBase],response_model_exclude=["files"])
def read_all_milestone(room_id:str):
    return read_all(room_id)

@router.post("/")
def create_milestone(info : MileStoneBase):
    create(info)

@router.post("/{milestone_id}/content")
def create_cont(milestone_id:str, file:UploadFile):
    create_content(milestone_id,file)