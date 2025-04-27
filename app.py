from flask import Flask, request, render_template_string
from pymongo import MongoClient
from datetime import datetime
import html

from src.modules.conexion import obtener_coleccion
from src.modules.carga_datos import cargar_y_limpiar_datos
from src.modules.indexacion import crear_indices
from src.modules.analisis import mejores_5_paises, analisis_compras_por_categoria
from src.modules.agregaciones import crear_proveedores_ordenados
from src.modules.operaciones_lectura import (
    contar_compras_en_intervalo,
    listar_categorias_distintas,
    obtener_usuario_por_email,
    buscar_compras_por_email_y_pais,
    busqueda_texto_shoppings,
    buscar_usuarios_por_pais_y_categoria
)
from src.modules.operaciones_actualizacion import (
    actualizar_email_contacto,
    incrementar_precio_shopping,
)
from src.modules.operaciones_anidadas import (
    modificar_proveedor_compra,
    añadir_etiqueta_a_todas_compras,
    buscar_por_campo_anidado
)
from src.modules.utilidades import imprimir_documentos

app = Flask(__name__)

# Inicialización: conexión, carga de datos e índices
coleccion = obtener_coleccion()
cargar_y_limpiar_datos(coleccion, "data/MOCK_DATA.json")
crear_indices(coleccion)

# Helpers para formatear datos en tablas HTML
def dict_to_table(obj):
    if not obj:
        return '<p>No hay datos para mostrar.</p>'
    html_content = '<table class="table table-striped"><tbody>'
    for key, val in obj.items():
        html_content += (
            f"<tr><th>{html.escape(str(key))}</th>"
            f"<td>{html.escape(str(val))}</td></tr>"
        )
    html_content += '</tbody></table>'
    return html_content

def list_to_table(list_obj):
    if not list_obj:
        return '<p>No hay datos para mostrar.</p>'
    headers = list_obj[0].keys()
    html_content = '<table class="table table-bordered"><thead><tr>'
    for h in headers:
        html_content += f"<th>{html.escape(str(h))}</th>"
    html_content += '</tr></thead><tbody>'
    for item in list_obj:
        html_content += '<tr>'
        for h in headers:
            html_content += f"<td>{html.escape(str(item.get(h, '')))}</td>"
        html_content += '</tr>'
    html_content += '</tbody></table>'
    return html_content

# Plantilla base con estilos
layout = '''<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard de Compras</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { background-color: #ffe6f2; }
      .btn-custom-1 { background-color: #ff00ff; color: white; border-color: #ff00ff; }
      .btn-custom-2 { background-color: #800080; color: white; border-color: #800080; }
      .btn-custom-1:hover { background-color: #e600e6; border-color: #e600e6; }
      .btn-custom-2:hover { background-color: #660066; border-color: #660066; }
      nav a { margin-bottom: 0.5rem; }
      .content-block { background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    </style>
  </head>
  <body class="p-4">
    <div class="container">
      <h1 class="mb-4">Dashboard de Compras Internacionales</h1>
      <nav class="mb-4 d-flex flex-wrap">
        {% for name, endpoint in nav_items %}
          <a href="{{ endpoint }}" class="btn {{ 'btn-custom-1' if loop.index % 2 else 'btn-custom-2' }} me-2">{{ name }}</a>
        {% endfor %}
      </nav>
      <div class="content-block">{{ content | safe }}</div>
    </div>
  </body>
</html>'''

def render(content):
    nav_items = [
        ("Inicio", "/"),
        ("Top 5 Países", "/top5"),
        ("Análisis Categoría", "/analisis_categoria"),
        ("Proveedores Ordenados", "/proveedores"),
        ("Contar Intervalo", "/contar_intervalo"),
        ("Listar Categorías", "/lista_categorias"),
        ("Actualizar Email", "/actualizar_email"),
        ("Incrementar Precio", "/incrementar_precio"),
        ("Modificar Proveedor", "/modificar_proveedor"),
        ("Añadir Etiqueta", "/añadir_etiqueta"),
        ("Buscar Anidado", "/buscar_anidado"),
        ("Imprimir Docs", "/imprimir_doc"),
        ("Usuario por Email", "/usuario_email"),
        ("Compras Email+Pais", "/compras_email_pais"),
        ("Texto Shoppings", "/texto_shoppings"),
        ("Usuarios País+Categoría", "/usuarios_pais_categoria")
    ]
    return render_template_string(layout, content=content, nav_items=nav_items)

# Rutas
@app.route('/')
def home():
    return render('<p>Bienvenido al dashboard de Compras.</p>')

@app.route('/top5')
def top5_paises():
    docs = mejores_5_paises(coleccion)
    return render('<h2>Top 5 Países</h2>' + list_to_table(docs))

@app.route('/analisis_categoria')
def analisis_categoria():
    docs = analisis_compras_por_categoria(coleccion)
    return render('<h2>Análisis Categoría</h2>' + list_to_table(docs))

@app.route('/proveedores')
def proveedores():
    docs = crear_proveedores_ordenados(coleccion)
    return render('<h2>Proveedores Ordenados</h2>' + list_to_table(docs))

@app.route('/contar_intervalo', methods=['GET','POST'])
def contar_intervalo():
    form = (
      '<h2>Contar Compras en Intervalo</h2>'
      '<form method="post">'
      '<input type="date" name="inicio" class="form-control">'
      '<input type="date" name="fin" class="form-control mt-2">'
      '<button class="btn btn-custom-1 mt-2">Contar</button>'
      '</form>'
    )
    if request.method == 'POST':
        d1 = datetime.fromisoformat(request.form['inicio'])
        d2 = datetime.fromisoformat(request.form['fin'])
        count = contar_compras_en_intervalo(coleccion, d1, d2)
        return render(form + f"<p>Total de compras: {count}</p>")
    return render(form)

@app.route('/lista_categorias')
def lista_categorias():
    cats = listar_categorias_distintas(coleccion)
    docs = [{"category": c} for c in cats]
    return render('<h2>Categorías Distintas</h2>' + list_to_table(docs))

@app.route('/actualizar_email', methods=['GET','POST'])
def actualizar_email():
    form = (
      '<h2>Actualizar Email</h2>'
      '<form method="post">'
      '<input name="nombre" placeholder="Kerrie" class="form-control">'
      '<input name="email" placeholder="kerrie@ejemplo.com" class="form-control mt-2">'
      '<button class="btn btn-custom-2 mt-2">Actualizar</button>'
      '</form>'
    )
    if request.method == 'POST':
        mod = actualizar_email_contacto(
            coleccion,
            request.form['nombre'],
            request.form['email']
        )
        return render(form + f"<p>Documentos modificados: {mod}</p>")
    return render(form)

@app.route('/incrementar_precio', methods=['GET','POST'])
def incrementar_precio_route():
    form = (
      '<h2>Incrementar Precio de Shopping</h2>'
      '<form method="post">'
      '<input type="number" step="0.01" name="aumento" '
      'placeholder="Cantidad a incrementar" class="form-control">'
      '<button class="btn btn-custom-1 mt-2">Incrementar</button>'
      '</form>'
    )
    if request.method == 'POST':
        try:
            aumento = float(request.form['aumento'])
        except ValueError:
            return render(form + '<div class="alert alert-danger mt-2">Introduce un número válido.</div>')
        mod = incrementar_precio_shopping(coleccion, aumento)
        return render(form + f"<p class=\"mt-3\">Documentos modificados: {mod}</p>")
    return render(form)


@app.route('/modificar_proveedor', methods=['GET','POST'])
def modificar_proveedor_route():
    form = (
      '<h2>Modificar Proveedor</h2>'
      '<form method="post">'
      '<input name="usuario" placeholder="Delbert" class="form-control">'
      '<input name="indice" placeholder="0" class="form-control mt-2">'
      '<input name="proveedor" placeholder="TechCorp" class="form-control mt-2">'
      '<button class="btn btn-custom-1 mt-2">Modificar</button>'
      '</form>'
    )
    if request.method == 'POST':
        mod = modificar_proveedor_compra(
            coleccion,
            request.form['usuario'],
            int(request.form['indice']),
            request.form['proveedor']
        )
        return render(form + f"<p>Documentos modificados: {mod}</p>")
    return render(form)

@app.route('/añadir_etiqueta', methods=['GET','POST'])
def añadir_etiqueta_route():
    form = (
      '<h2>Añadir Etiqueta</h2>'
      '<form method="post">'
      '<input name="etiqueta" placeholder="destacado" class="form-control">'
      '<button class="btn btn-custom-1 mt-2">Añadir</button>'
      '</form>'
    )
    if request.method == 'POST':
        mod = añadir_etiqueta_a_todas_compras(
            coleccion,
            request.form['etiqueta']
        )
        return render(form + f"<p>Documentos modificados: {mod}</p>")
    return render(form)

@app.route('/buscar_anidado', methods=['GET','POST'])
def buscar_anidado_route():
    form = (
      '<h2>Buscar Anidado</h2>'
      '<form method="post">'
      '<input name="ruta" placeholder="shoppings.0.category" class="form-control">'
      '<input name="valor" placeholder="Clothing" class="form-control mt-2">'
      '<button class="btn btn-custom-2 mt-2">Buscar</button>'
      '</form>'
    )
    if request.method == 'POST':
        docs = buscar_por_campo_anidado(
            coleccion,
            request.form['ruta'],
            request.form['valor']
        )
        return render(form + list_to_table(docs))
    return render(form)

@app.route('/imprimir_doc', methods=['GET','POST'])
def imprimir_doc_route():
    form = (
      '<h2>Imprimir Documentos</h2>'
      '<form method="post">'
      '<input name="filtro" placeholder="{}" class="form-control">'
      '<input name="campos" placeholder="first_name,contact.email" class="form-control mt-2">'
      '<button class="btn btn-custom-1 mt-2">Imprimir</button>'
      '</form>'
    )
    if request.method == 'POST':
        filtro = eval(request.form['filtro'])
        campos = request.form['campos'].split(',')
        docs = imprimir_documentos(coleccion, filtro, campos)
        return render(form + list_to_table(docs))
    return render(form)

@app.route('/usuario_email', methods=['GET','POST'])
def usuario_email_route():
    form = (
      '<h2>Usuario por Email</h2>'
      '<form method="post">'
      '<input name="email" placeholder="hsauntb@who.int" class="form-control">'
      '<button class="btn btn-custom-1 mt-2">Buscar</button>'
      '</form>'
    )
    if request.method == 'POST':
        doc = obtener_usuario_por_email(coleccion, request.form['email'])
        return render(form + dict_to_table(doc))
    return render(form)

@app.route('/compras_email_pais', methods=['GET','POST'])
def compras_email_pais_route():
    form = (
      '<h2>Compras por Email y País</h2>'
      '<form method="post">'
      '<input name="email" placeholder="sbenallackf@wsj.com" class="form-control">'
      '<input name="pais" placeholder="Spain" class="form-control mt-2">'
      '<button class="btn btn-custom-2 mt-2">Buscar</button>'
      '</form>'
    )
    if request.method == 'POST':
        docs = buscar_compras_por_email_y_pais(
            coleccion,
            request.form['email'],
            request.form['pais']
        )
        return render(form + list_to_table(docs))
    return render(form)

@app.route('/texto_shoppings', methods=['GET','POST'])
def texto_shoppings_route():
    form = (
      '<h2>Búsqueda de Texto</h2>'
      '<form method="post">'
      '<input name="termino" placeholder="Electronics" class="form-control">'
      '<button class="btn btn-custom-1 mt-2">Buscar</button>'
      '</form>'
    )
    if request.method == 'POST':
        docs = busqueda_texto_shoppings(coleccion, request.form['termino'])
        return render(form + list_to_table(docs))
    return render(form)

@app.route('/usuarios_pais_categoria', methods=['GET','POST'])
def usuarios_pais_categoria_route():
    form = (
      '<h2>Usuarios por País y Categoría</h2>'
      '<form method="post">'
      '<input name="pais" placeholder="United States" class="form-control">'
      '<input name="categoria" placeholder="Clothing" class="form-control mt-2">'
      '<button class="btn btn-custom-2 mt-2">Buscar</button>'
      '</form>'
    )
    if request.method == 'POST':
        docs = buscar_usuarios_por_pais_y_categoria(
            coleccion,
            request.form['pais'],
            request.form['categoria']
        )
        return render(form + list_to_table(docs))
    return render(form)

if __name__ == '__main__':
    app.run(debug=True)
