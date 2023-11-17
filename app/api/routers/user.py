from fastapi import APIRouter
from app.crud.base import read_db

router = APIRouter(prefix="/user")

# 모든 유저 조회
@router.get("/")
def read_all_user():
    conn = read_db("user")
    users = conn.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return user_list