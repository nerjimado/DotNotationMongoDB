from datetime import datetime

def buscar_proveedores_por_pais(collection, pais):
    print(f"\nUsuarios que han comprado algo de proveedores de {pais}:")
    for doc in collection.find({"shoppings.provider.country": pais}):
        print(f"{doc['first_name']} {doc['last_name']} - {doc['country']}")

def actualizar_telefono(collection, nombre, nuevo_telefono):
    result = collection.update_one(
        {"first_name": nombre},
        {"$set": {"contact.phone": nuevo_telefono}}
    )
    print(f"\n{result.modified_count} documento(s) actualizado(s) (teléfono cambiado).")

def agregar_compra(collection, nombre):
    nueva_compra = {
        "name": "Wireless Headphones",
        "price": 59.99,
        "date": datetime.utcnow(),
        "provider": {"name": "NewTech", "country": "Germany"}
    }
    collection.update_one(
        {"first_name": nombre},
        {"$push": {"shoppings": nueva_compra}}
    )
    print("\nNueva compra añadida.")

def eliminar_compras_antiguas(collection, year):
    fecha_corte = datetime(year, 1, 1)
    collection.update_many(
        {},
        {"$pull": {"shoppings": {"date": {"$lt": fecha_corte}}}}
    )
    print("\nCompras antiguas eliminadas.")
