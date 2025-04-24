import json
from bson import ObjectId
from datetime import datetime

def clean_document(doc):
    if '_id' in doc and '$oid' in doc['_id']:
        doc['_id'] = ObjectId(doc['_id']['$oid'])
    if 'shoppings' in doc:
        for shopping in doc['shoppings']:
            if 'date' in shopping and '$date' in shopping['date']:
                shopping['date'] = datetime.fromisoformat(shopping['date']['$date'].replace('Z', '+00:00'))
    return doc

def load_and_clean_data(collection, filepath):
    if collection.count_documents({}) == 0:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        data_cleaned = [clean_document(d) for d in data]
        collection.insert_many(data_cleaned)
        print("Datos insertados correctamente.")
