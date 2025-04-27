# Proyecto: Análisis de Compras con MongoDB y Dot Notation

Este proyecto demuestra cómo trabajar con bases de datos MongoDB utilizando **dot notation** para acceder, consultar y modificar documentos con estructuras anidadas.

## 📁 Estructura del Proyecto

```
DotNotationMongoDB/
├app.py
└── src/
    ├── main.py
    └── modules/
        ├── agregaciones.py
        ├── analisis.py
        ├── carga_datos.py
        ├── conexion.py
        ├── indexacion.py
        ├── operaciones_actualizacion.py
        ├── operaciones_anidadas.py
        ├── operaciones_lectura.py
        └── utilidades.py
└── data/
    ├── MOCK_DATA.json
```

## Requisitos

- Python 3.7+
- MongoDB (local o MongoDB Atlas)
- Paquetes Python:
  - `pymongo`
  - `bson`
  - `flask`

Instalación rápida de dependencias:
```bash
pip install pymongo flask
```

## Ejecución

1. Asegúrate de tener MongoDB corriendo localmente o cambia la URI en `modules/connection.py` si usas Atlas.
2. Ejecuta el script principal:

```bash
python main.py
```
   O bien si quieres interactuar con la interfaz de usuario ejecuta:

```bash
python app.py
```

## 📄 Autores
- Nerea Jiménez Adorna
- Carlos García Ortiz

Proyecto desarrollado como parte de la asignatura complementos de bases de datos, en el tema Dot Notation en MongoDB.
