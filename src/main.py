# Archivo principal
from modules.conexion import obtener_coleccion
from modules.carga_datos import cargar_y_limpiar_datos
from modules.indexacion import *
from modules.analisis import *
from modules.operaciones_lectura import *
from modules.operaciones_actualizacion import *
from modules.operaciones_anidadas import *
from datetime import datetime
from pprint import pprint


def main():
    coleccion = obtener_coleccion()
    cargar_y_limpiar_datos(coleccion, "data/MOCK_DATA.json")
    crear_indices(coleccion)
    paises = mejores_5_paises(coleccion)
    categorias = analisis_compras_por_categoria(coleccion)
    print("Top 5 países:")
    pprint(paises)
    print("\nCompras por categoría:")
    pprint(categorias)
    precio = obtener_documento_precio_mayor(coleccion, 100)
    print("\nDocumento de precio mayor que:")
    pprint(precio)
    conteo_compras = contar_compras_en_intervalo(coleccion, datetime(2024,5,5), datetime(2025,1,1))
    print("\nCompras en un intervalo dado:")
    pprint(conteo_compras)
    listado_cat = listar_categorias_distintas(coleccion)
    print("\nListado de categorías:")
    pprint(listado_cat)
    actualizar_email_contacto(coleccion, "Kerrie", "kerrie@ejemplo.com")
    incrementar_precio_shopping(coleccion, 10, "mastercard")
    modificar_proveedor_compra(coleccion, "Delbert", 0, "TechCorp")
    añadir_etiqueta_a_todas_compras(coleccion, "destacado")
    busqueda = buscar_por_campo_anidado(coleccion, "shoppings.0.provider.name", "Centimia")
    print("\nBúsqueda:")
    pprint(busqueda)
    crear_indice_compuesto(coleccion, ["country", "shoppings.category"])
    

if __name__ == "__main__":
    main()
