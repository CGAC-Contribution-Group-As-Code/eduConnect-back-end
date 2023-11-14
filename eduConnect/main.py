from typing import Union
from fastapi import FastAPI
import pymongo
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#CORS(https://www.jasonchoi.dev/posts/fastapi/cors-allow-setting)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:1000",
    "http://localhost:8080",
]

# 미들웨어 추가 -> CORS 해결위해 필요(https://ghost4551.tistory.com/46)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 스키마 내의 특정 테이블 조회
def read_db(name):
    conn = pymongo.MongoClient("mongodb://localhost:27017/")
    return conn['eduConnect'][name]


# 모든 유저 조회
@app.get("/all-user")
def read_all_user():
    conn = read_db("user")
    users = conn.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return user_list

# 모든 room 조회
@app.get("/all-room")
def read_all_user():
    conn = read_db("room")
    rooms = conn.find()
    room_list = []
    for room in rooms:
        room['_id'] = str(room['_id'])
        room_list.append(room)
    return room_list