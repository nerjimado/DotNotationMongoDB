# Consultas de lectura avanzadas

def buscar_proveedores_por_pais(coleccion, pais):
    return list(coleccion.find({"shoppings.provider.country": pais}))

def obtener_documento_precio_mayor(coleccion, umbral):
    return coleccion.find_one({"shoppings.price": {"$gt": umbral}})

def contar_compras_en_intervalo(coleccion, fecha_inicio, fecha_fin):
    return coleccion.count_documents({
        "shoppings.date": {"$gte": fecha_inicio, "$lt": fecha_fin}
    })

def listar_categorias_distintas(coleccion):
    return coleccion.distinct("shoppings.category")

def obtener_usuario_por_email(coleccion, email):
    return coleccion.find_one({"contact.email": email})

def buscar_compras_por_email_y_pais(coleccion, email, pais):
    return list(coleccion.find({
        "contact.email": email,
        "shoppings.provider.country": pais
    }))

def busqueda_texto_shoppings(coleccion, termino):
    cursor = coleccion.find(
        {"$text": {"$search": termino}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])
    return list(cursor)

def buscar_usuarios_por_pais_y_categoria(coleccion, pais, categoria):
    return list(coleccion.find({
        "country": pais,
        "shoppings.category": categoria
    }))
