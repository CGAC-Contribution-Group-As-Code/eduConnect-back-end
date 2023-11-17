from bson import ObjectId
from fastapi import UploadFile
from fastapi.responses import FileResponse
from app.crud.base import read_db
from app.schema.milestone import *
from dotenv import load_dotenv
import uuid
import os
from app.core.chatgpt import *
import fitz
import json

load_dotenv(verbose=True,override=True)

def create(milestone:MileStoneBase,room_id:str):
    milestone.last_modify=datetime.now()
    milestone_id=read_db("milestone").insert_one(milestone.model_dump()).inserted_id

    collection=read_db("room")
    query = {"_id":ObjectId(room_id)}
    document=collection.find_one(query)
    if document:
        new_value = milestone_id
        if 'milestone' in document:  # 만약 리스트 필드가 이미 존재한다면
            document['milestone'].append(new_value)
        else:  # 리스트 필드가 없다면 새로 생성하여 값을 추가합니다.
            document['milestone'] = [new_value]

        # 업데이트된 문서 저장
        collection.update_one(query, {'$set': document})
        print("값을 성공적으로 추가했습니다.")
    else:
        print("문서를 찾을 수 없습니다.")

def read_all(room_id:str):
    room_col=read_db("room")
    milestone_list=room_col.find_one({"_id":ObjectId(room_id)})
    if (milestone_list):
        print(list(read_db("milestone").find({"_id":{"$in":milestone_list["milestone"]}})))
        return list(read_db("milestone").find({"_id":{"$in":milestone_list["milestone"]}}))
    else:
        return []
    
def read(mileston_id:str):
    col=read_db("milestone")
    milestone=col.find_one({"_id":ObjectId(mileston_id)})
    print(milestone)
    return milestone

def create_content(milestone_id:str, file:UploadFile):
    if not os.path.exists(os.path.join(os.getenv("MILESTONE_PATH"),milestone_id)):
        os.mkdir(os.path.join(os.getenv("MILESTONE_PATH"),milestone_id))

    path=f'{milestone_id}/{uuid.uuid4()}'
    with open(os.path.join(os.getenv("MILESTONE_PATH"),path),"wb+") as new_file:
        new_file.write(file.file.read())
    collection=read_db("milestone")
    query = {"_id":ObjectId(milestone_id)}
    document=collection.find_one(query)
    if document:
        new_value = ContentBase(name=file.filename,size=file.size,path=path)
        if 'contents' in document:  # 만약 리스트 필드가 이미 존재한다면
            document['contents'].append(new_value.model_dump())

        # 업데이트된 문서 저장
        collection.update_one(query, {'$set': document})
        print("값을 성공적으로 추가했습니다.")
    else:
        print("문서를 찾을 수 없습니다.")

def read_contents(mileston_id:str):
    col=read_db("milestone")
    milestone=col.find_one({"_id":ObjectId(mileston_id)})
    return milestone["contents"]

def read_content(milestone_id:str,content_id:str):
    return FileResponse(os.path.join(os.getenv("MILESTONE_PATH"),milestone_id,content_id), media_type="application/pdf")

def save_quiz(milestone_id:str, content_id:str,quizs:list[QuizBase]):
    collection=read_db("milestone")
    query = {"_id":ObjectId(milestone_id)}
    document=collection.find_one(query)
    new_round={
        "r_id": {
            "$oid": ObjectId()
          },
        "quiz":[]
    }
    for i in quizs:
        new_round["quiz"].append(i.model_dump())
    if document:
        for content in document["contents"]:
            if content['path'].split('/')[-1]==content_id:
                content["roundes"].append(new_round)
                break
        print(document)
        collection.update_one(query, {'$set': document})
        print("값을 성공적으로 추가했습니다.")
    else:
        print("문서를 찾을 수 없습니다.")

def create_quiz(type:str,milestone_id:str, content_id:str):
    task_type=""
    if type=="1":
        task_type="계산"
    elif type=="0":
        task_type="객관식"
    subjective_prompt='''
%s

주어진 정보를 고려해서 %s 문제를 1개 만들어주세요
'''%(extract_pdf(milestone_id,content_id),task_type)
    subjective_template = '''
당신은 %s에 대해서 잘 알고 있는 선생님입니다.
당신은 주어진 내용에 관한 문제를 만들고, 문제에 관한 정보를 다음과 같은 형식으로 제공합니다.
객관식 문제일 경우 "option" 도 제공합니다.
{
    "title": "<문제 제목>",
    "desc": "<문제 설명>",
    "option":[
        "<보기1>",
        "<보기2>",
        "<보기3>",
        "<보기4>",
    ]
    "answer":"<문제 정답>"
}
'''%("물리")
    result=ask_ai(subjective_prompt,subjective_template)
    json_result=json.loads(result)
    json_result['type']=type
    return json_result

def extract_pdf(milestone_id:str, content_id:str):
    path = os.path.join(os.getenv("MILESTONE_PATH"),milestone_id,content_id)
    doc = fitz.open(path)
    text_list=""
    for page in doc:
        text = page.get_text()
        text_list+=text+"\n"
    return text_list