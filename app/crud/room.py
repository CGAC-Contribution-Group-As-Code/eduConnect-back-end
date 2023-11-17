import json
from app.core.chatgpt import ask_ai
from app.crud.base import read_db
from bson.objectid import ObjectId
from datetime import datetime

class CrudRoom():
    def read_all_room(self):
        conn = read_db("room")
        rooms = conn.find()
        room_list = []
        for room in rooms:
            room_list.append({
                "_id":  str(room['_id']),
                "name": room['name'],
                "teacher": room['teacher'],
                "member": len(room['member'])
            })
        return room_list
    
    def create_room(self, info):
        conn = read_db("room")
        conn.insert_one({
            "name": info.name,
            "desc": info.desc,
            "teacher": info.teacher,
            "member": info.student,
            "milestone": [],
            "question": []
        })
        return True
    
    def read_room(self, room_id):
        # room info
        conn = read_db("room")
        room = conn.find({ "_id": ObjectId(room_id)})
        room = list(room)[0]
        room['_id'] = str(room['_id'])

    def read_questions(self, room_id):
        conn = read_db("room")
        room = conn.find({ "_id": ObjectId(room_id)})
        room = list(room)[0]

        conn = read_db("Question")
        question = []
        for i in room['question']:
            result = conn.find({ "_id": i})
            result = list(result)
            answer = list(result[0]['answer'] )
            question.append({
                '_id': str(result[0]['_id']),
                'writer': result[0]['writer'],
                'time': result[0]['time'],
                'desc': result[0]['desc'],
                'answer': answer[::-1]
            })
        return question[::-1]

    def create_questions(self, info):
        conn = read_db("Question")
        id = conn.insert_one({
            "writer": info.writer,
            "desc": info.desc,
            "time": datetime.now(),
            "answer": []
        }).inserted_id

        conn = read_db("room")
        conn.update_one({"_id": ObjectId(info.room_id)}, 
            {"$push": {"question": id}})
        return True

    def create_answer(self, info):
        print(info)
        conn = read_db("Question")
        conn.update_one({"_id": ObjectId(info.question_id)}, 
            {"$push": {"answer": {
                "ans_time": datetime.now(),
                "ans_writer": info.ans_writer,
                "answer": info.answer
            }}})
        return True

    def create_aianswer(self,q_id:str,question:str):
        conn = read_db("Question")
        conn.update_one({"_id": ObjectId(q_id)}, 
            {"$push": {"answer": {
                "ans_time": datetime.now(),
                "ans_writer": "AI",
                "answer": self.create_aians(question)
            }}})
        return True
    
    def create_aians(self,question:str):
        answer_prompt='''
    %s

    주어진 질문에 대한 자세한 답변을 반드시 형식에 맞게 대답해주세요.
    '''%(question)
        answer_template = '''
    당신은 선생님입니다.
    당신은 주어진 질문에 대한 답변을 다음과 같은 형식으로 제공합니다.
    {
        "answer": "<답변>"
    }
    '''
        result=ask_ai(answer_prompt,answer_template)
        json_result=json.loads(result)
        return json_result["answer"]

crud_room  = CrudRoom()