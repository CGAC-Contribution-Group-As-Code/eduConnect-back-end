from bson import ObjectId
from app.schema.user import Feedback, Login
from fastapi import APIRouter
from app.crud.base import read_db
from app.crud.user import *

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

@router.post("/login")
def login(info: Login):
    conn = read_db("user")
    user = conn.find({ "user_id":info.id, "pw": info.pw } )
    user = list(user)
    return {
        '_id': str(user[0]['_id']),
        'user_id': user[0]['user_id'],
        'role': user[0]['role']
    }

@router.get("/feedback")
def read_user_info(room_id:str=None):
    return_user_list=[]
    if room_id:
        conn = read_db("room")
        users = conn.find_one({"_id":ObjectId(room_id)})['member']
        for i in users:
            temp=read_user(i['_id'])
            if temp['role']==0:
                return_user_list.append(temp)
    return return_user_list

@router.post("/feedback")
def read_user_info(user_id:str,feedback:Feedback):
    collection=read_db("user")
    query = {"_id":ObjectId(user_id)}
    document=collection.find_one(query)
    if document:
        if 'feedback' in document:  # 만약 리스트 필드가 이미 존재한다면
            document['feedback'].append(feedback.model_dump())
        else:
            document['feedback']=[feedback.model_dump()]

        # 업데이트된 문서 저장
        collection.update_one(query, {'$set': document})
        print("값을 성공적으로 추가했습니다.")
    else:
        print("문서를 찾을 수 없습니다.")