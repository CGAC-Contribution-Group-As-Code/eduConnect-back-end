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
            "teacher": "CGAC",
            "member": info.student
        })
        return True
    
    def read_room(self, room_id):
        # room info
        conn = read_db("room")
        room = conn.find({ "_id": ObjectId(room_id)})
        room = list(room)[0]
        room['_id'] = str(room['_id'])
        
        # milestone = []
        # conn = read_db("milestone")
        # for value in room['milestone']:
        #     result = conn.find({ "_id":value})
        #     result = list(result)[0]
        #     print(result)


    
crud_room  = CrudRoom()