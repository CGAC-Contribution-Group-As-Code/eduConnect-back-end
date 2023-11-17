import pymongo

def read_db(name):
    '''
    db내의 특정 콜렉션
    '''
    conn = pymongo.MongoClient("mongodb://localhost:27017/")
    return conn['eduConnect'][name]