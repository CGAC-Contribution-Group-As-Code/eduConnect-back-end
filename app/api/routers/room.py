from app.crud.room import crud_room
from app.schema.room import CreateRoom
from fastapi import APIRouter
from app.crud.base import read_db


router = APIRouter(prefix="/room")

# 모든 room 조회
@router.get("/")
def read_all_room():
    return crud_room.read_all_room()

# room 생성
@router.post("/")
def create_room(info: CreateRoom):
    return crud_room.create_room(info)

# 해당 id의 room info 조회
@router.get("/{room_id}")
def read_room(room_id: str):
    return crud_room.read_room(room_id)

# 해당 id의 room의 질문리스트
@router.get("/{room_id}/questions")
def read_room(room_id: str):
    return crud_room.read_questions(room_id)