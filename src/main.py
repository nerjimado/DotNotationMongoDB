# Archivo principal
from modules.conexion import obtener_coleccion
from modules.carga_datos import cargar_y_limpiar_datos
from modules.indexacion import crear_indices, crear_indice_compuesto
from modules.analisis import mejores_5_paises
from modules.operaciones_lectura import *
from modules.operaciones_actualizacion import *
from modules.operaciones_anidadas import *
from datetime import datetime

def main():
    coleccion = obtener_coleccion()
    cargar_y_limpiar_datos(coleccion, "data/MOCK_DATA.json")
    crear_indices(coleccion)
    mejores_5_paises(coleccion)
    buscar_proveedores_por_pais(coleccion, "Germany")
    obtener_documento_precio_mayor(coleccion, 100)
    contar_compras_en_intervalo(coleccion, datetime(2024,5,5), datetime(2025,1,1))
    listar_categorias_distintas(coleccion)
    actualizar_email_contacto(coleccion, "Kerrie", "kerrie@ejemplo.com")
    incrementar_precio_shopping(coleccion, 10, "mastercard")
    modificar_proveedor_compra(coleccion, "Delbert", 0, "TechCorp")
    añadir_etiqueta_a_todas_compras(coleccion, "destacado")
    buscar_por_campo_anidado(coleccion, "shoppings.0.category", "Clothing")
    crear_indice_compuesto(coleccion, ["country", "shoppings.category"])

if __name__ == "__main__":
    main()
