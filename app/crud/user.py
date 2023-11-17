from bson import ObjectId
from fastapi import UploadFile
from fastapi.responses import FileResponse
from app.crud.base import read_db
from app.schema.milestone import *

def read_user(user_id:str):
    temp = read_db("user").find_one({"_id":ObjectId(user_id)})
    temp['_id']=str(temp['_id'])
    return temp

