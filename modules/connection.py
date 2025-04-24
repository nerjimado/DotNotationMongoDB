import pymongo

def get_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["compras_internacionales"]
    return db["usuarios"]
