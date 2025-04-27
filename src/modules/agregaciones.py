# Crea lista de proveedores ordenados por ventas

def crear_proveedores_ordenados(coleccion):
    pipeline = [
        {"$unwind": "$shoppings"},
        {"$group": {
            "_id": "$shoppings.provider.name",
            "total_ventas": {"$sum": 1},
            "paises": {"$addToSet": "$shoppings.provider.country"}
        }},
        {"$sort": {"total_ventas": -1}}
    ]
    return list(coleccion.aggregate(pipeline))
