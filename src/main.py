from modules.connection import get_collection
from modules.load_data import load_and_clean_data
from modules.operations import *
from modules.indexing import create_indexes
from modules.analysis import top_5_paises

# 1. Conectar y obtener colección
collection = get_collection()

# 2. Cargar e insertar datos
load_and_clean_data(collection, "data/MOCK_DATA.json")

# 3. Consultas y operaciones básicas
buscar_proveedores_por_pais(collection, "Spain")
actualizar_telefono(collection, "Kerrie", "999-999-9999")
agregar_compra(collection, "Kerrie")
eliminar_compras_antiguas(collection, 2022)

# 4. Crear índices
create_indexes(collection)

# 5. Análisis
top_5_paises(collection)

print("\nScript finalizado.")