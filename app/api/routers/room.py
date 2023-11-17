from fastapi import APIRouter
from app.crud.base import read_db

router = APIRouter(prefix="/room")

# 모든 room 조회
@router.get("/")
def read_all_user():
    conn = read_db("room")
    rooms = conn.find()
    room_list = []
    for room in rooms:
        room['_id'] = str(room['_id'])
        room_list.append(room)
    return room_list