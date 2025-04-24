# Proyecto: Análisis de Compras con MongoDB y Dot Notation

Este proyecto demuestra cómo trabajar con bases de datos MongoDB utilizando **dot notation** para acceder, consultar y modificar documentos con estructuras anidadas. Está dividido en módulos para facilitar el mantenimiento y la comprensión.

## 📁 Estructura del Proyecto

```
MongoDotNotationProject/
└── src/
    ├── main.py
    └── modules/
        ├── analysis.py
        ├── connection.py
        ├── indexing.py
        ├── load_data.py
        └── operations.py
└── data/
    ├── MOCK_DATA.json
```

## Requisitos

- Python 3.7+
- MongoDB (local o MongoDB Atlas)
- Paquetes Python:
  - `pymongo`
  - `bson`

Instalación rápida de dependencias:
```bash
pip install pymongo
```

## Ejecución

1. Asegúrate de tener MongoDB corriendo localmente o cambia la URI en `modules/connection.py` si usas Atlas.
2. Ejecuta el script principal:

```bash
python main.py
```

## 🔍 Qué hace el script

- Conecta con MongoDB.
- Limpia y carga datos JSON (convierte `$oid` y `$date`).
- Ejecuta operaciones como:
  - Buscar compras de proveedores por país.
  - Actualizar teléfonos.
  - Añadir nuevas compras.
  - Eliminar compras antiguas.
- Crea índices en campos anidados.
- Muestra análisis agregado del top 5 de países con más usuarios.

## 🧠 Aprendizajes clave

- Uso de `dot notation` en consultas y actualizaciones.
- Manipulación de documentos con arrays y subdocumentos.
- Modularización en Python para proyectos con MongoDB.

## 📄 Autores
- Nerea Jiménez Adorna
- Carlos García Ortiz

Proyecto desarrollado como parte de la asignatura complementos de bases de datos, en el tema Dot Notation en MongoDB.
