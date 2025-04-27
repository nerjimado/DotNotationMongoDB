# Análisis de datos con agregaciones

def mejores_5_paises(coleccion):
    pipeline = [
        {"$group": {"_id": "$country", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5}
    ]
    return list(coleccion.aggregate(pipeline))

def analisis_compras_por_categoria(coleccion):
    pipeline = [
        {"$unwind": "$shoppings"},
        {"$group": {"_id": "$shoppings.category", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]
    return list(coleccion.aggregate(pipeline))
