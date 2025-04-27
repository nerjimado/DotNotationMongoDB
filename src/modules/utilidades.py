# Utilidades

def imprimir_documentos(coleccion, filtro=None, campos=None):
    filtro = filtro or {}
    proyeccion = {campo: 1 for campo in campos} if campos else None
    return list(coleccion.find(filtro, proyeccion))
