from fastapi import APIRouter,Depends
from app.crud.milestone import *
from app.schema.milestone import *

router = APIRouter(prefix="/milestone")

@router.get("/",response_model=list[MileStoneBase],response_model_exclude=["files"])
def read_all_milestone():
    return read_all()

@router.post("/")
def create_milestone(info : MileStoneBase):
    create(info)