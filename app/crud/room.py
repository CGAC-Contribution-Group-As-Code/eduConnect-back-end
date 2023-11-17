from app.crud.base import read_db
from bson.objectid import ObjectId

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
            question.append({
                'writer': result[0]['writer'],
                'time': result[0]['time'],
                'title': result[0]['title'],
                'desc': result[0]['desc'],
                'answer': result[0]['answer'] 
            })
        print(question)
        return question

    
crud_room  = CrudRoom()