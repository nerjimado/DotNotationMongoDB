# Carga y limpieza de datos
import json
from bson import ObjectId
from datetime import datetime

def limpiar_documento(doc):
    if '_id' in doc and '$oid' in doc['_id']:
        doc['_id'] = ObjectId(doc['_id']['$oid'])
    if 'shoppings' in doc:
        for compra in doc['shoppings']:
            if 'date' in compra and '$date' in compra['date']:
                compra['date'] = datetime.fromisoformat(compra['date']['$date'].replace('Z', '+00:00'))
    return doc

def cargar_y_limpiar_datos(coleccion, ruta_archivo):
    if coleccion.count_documents({}) == 0:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        datos_limpiados = [limpiar_documento(d) for d in datos]
        coleccion.insert_many(datos_limpiados)
        print("Datos insertados correctamente en la colección.")
