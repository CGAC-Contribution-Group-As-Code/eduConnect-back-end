from app.crud.base import read_db
from app.schema.milestone import *
from dotenv import load_dotenv
import os

load_dotenv(verbose=True,override=True)

def read_all():
    data=read_db("milestone")
    return data.find()

def create(milestone:MileStoneBase):
    db=read_db("milestone")
    id=db.insert_one(milestone.model_dump()).inserted_id
    if os.path.exists(os.path.join(os.getenv("MILESTONE_PATH"),id)):
        os.mkdir(os.path.join(os.getenv("MILESTONE_PATH"),id))