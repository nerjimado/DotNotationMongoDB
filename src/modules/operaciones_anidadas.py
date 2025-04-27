# Operaciones dot notation

def modificar_proveedor_compra(coleccion, nombre_usuario, indice, nuevo_proveedor):
    ruta = f"shoppings.{indice}.provider.name"
    result = coleccion.update_one(
        {"first_name": nombre_usuario},
        {"$set": {ruta: nuevo_proveedor}}
    )
    return result.modified_count

def añadir_etiqueta_a_todas_compras(coleccion, etiqueta):
    result = coleccion.update_many(
        {},
        {"$push": {"shoppings.$[].tags": etiqueta}}
    )
    return result.modified_count

def buscar_por_campo_anidado(coleccion, ruta_dot, valor):
    return list(coleccion.find({ruta_dot: valor}))
