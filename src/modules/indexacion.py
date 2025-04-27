# Creación de índices

def crear_indices(coleccion):
    coleccion.create_index("contact.email")
    coleccion.create_index("shoppings.provider.country")
    coleccion.create_index([("contact.email", 1), ("shoppings.provider.country", 1)], name="indice_compuesto_email_proveedor")
    coleccion.create_index([("shoppings.category", 1)], name="indice_categoria")
    coleccion.create_index([("shoppings.provider.name", "text"), ("shoppings.category", "text")], name="indice_texto_shoppings")
    print("Índices creados: contact.email, shoppings.provider.country, compuesto y de texto.")

def crear_indice_compuesto(coleccion, campos):
    indice = [(campo, 1) for campo in campos]
    coleccion.create_index(indice)
    print(f"\nÍndice compuesto creado para campos: {campos}")