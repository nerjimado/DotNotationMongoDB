import pymongo
import json
from datetime import datetime
from bson import ObjectId

# Función para limpiar cada documento
def clean_document(doc):
    # Convertir _id
    if '_id' in doc and '$oid' in doc['_id']:
        doc['_id'] = ObjectId(doc['_id']['$oid'])
    
    # Convertir fechas en las compras
    if 'shoppings' in doc:
        for shopping in doc['shoppings']:
            if 'date' in shopping and '$date' in shopping['date']:
                shopping['date'] = datetime.fromisoformat(shopping['date']['$date'].replace('Z', '+00:00'))

    return doc


# 1. Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Cambia la URL si usas Atlas

# 2. Crear base de datos y colección
db = client["compras_internacionales"]
collection = db["usuarios"]

# 3. Cargar el dataset
with open("MOCK_DATA.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 4. Insertar documentos (si la colección está vacía)
if collection.count_documents({}) == 0:
    # Aplicar limpieza a todo
    data_cleaned = [clean_document(d) for d in data]
    collection.insert_many(data)
    print("Datos insertados correctamente.")

# 5. Consultas usando dot notation
print("\nUsuarios que han comprado algo de proveedores de Spain:")
for doc in collection.find({"shoppings.provider.country": "Spain"}):
    print(f"{doc['first_name']} {doc['last_name']} - {doc['country']}")

# 6. Actualizar un número de teléfono (ejemplo)
result = collection.update_one(
    {"first_name": "Kerrie"},
    {"$set": {"contact.phone": "136-467-5547"}}
)
print(f"\n{result.modified_count} documento(s) actualizado(s) (teléfono cambiado).")

# 7. Agregar una nueva compra a un usuario
nueva_compra = {
    "name": "Wireless Headphones",
    "price": 59.99,
    "date": datetime.now(),
    "provider": {"name": "NewTech", "country": "Germany"}
}
collection.update_one(
    {"first_name": "Kerrie"},  # Cambia por un nombre real
    {"$push": {"shoppings": nueva_compra}}
)
print("\nNueva compra añadida.")

# 8. Eliminar compras antes de 2022
fecha_corte = datetime(2022, 1, 1)
collection.update_many(
    {},
    {"$pull": {"shoppings": {"date": {"$lt": fecha_corte}}}}
)
print("\nCompras antiguas eliminadas.")

# 9. Crear índices para optimizar consultas en campos anidados
collection.create_index("contact.email")
collection.create_index("shoppings.provider.country")
print("\nÍndices creados en contact.email y shoppings.provider.country.")

# 10. Ejemplo de análisis: Top 5 países con más usuarios
pipeline = [
    {"$group": {"_id": "$country", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}},
    {"$limit": 5}
]
print("\nTop 5 países con más usuarios:")
for doc in collection.aggregate(pipeline):
    print(f"{doc['_id']}: {doc['total']} usuarios")

print("\nScript finalizado.")
