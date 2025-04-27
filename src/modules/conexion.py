# Conexión a MongoDB
import pymongo

def obtener_coleccion():
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["compras_internacionales"]
    return db["usuarios"]
