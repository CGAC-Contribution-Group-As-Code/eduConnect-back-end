from fastapi import APIRouter,Depends
from app.crud.milestone import *
from app.schema.milestone import *

router = APIRouter(prefix="/milestone",tags=["milestone"])

@router.post("/")
def create_milestone(room_id:str,info : MileStoneBase):
    create(info,room_id)

@router.get("/",response_model=list[MileStoneBase])
def read_all_milestone(room_id:str):
    print("ㅇㅇㅇ")
    return read_all(room_id)

@router.get("/{milestone_id}",response_model=MileStoneBase,response_model_exclude=["contents"])
def read_milestone(milestone_id:str):
    print("ㅋㅋㅋ")
    return read(milestone_id)

@router.post("/{milestone_id}/content")
def create_cont(milestone_id:str, file:UploadFile):
    create_content(milestone_id,file)

@router.get("/{milestone_id}/content",response_model=list[ContentBase])
def read_cont(milestone_id:str):
    return read_contents(milestone_id)

@router.get("/{milestone_id}/content/{content_id}")
def read_cont(milestone_id:str,content_id:str):
    return read_content(milestone_id,content_id)