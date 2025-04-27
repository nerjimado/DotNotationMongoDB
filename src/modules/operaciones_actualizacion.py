# Actualizaciones avanzadas

def actualizar_email_contacto(coleccion, nombre, nuevo_email):
    result = coleccion.update_one(
        {"first_name": nombre},
        {"$set": {"contact.email": nuevo_email}}
    )
    return result.modified_count

def incrementar_precio_shopping(coleccion, aumento=10, tarjeta ="mastercard"):
    result = coleccion.update_many(
        {"creditcards.0": tarjeta},
        {"$inc": {"shoppings.0.price": aumento}}
    )
    return result.modified_count
