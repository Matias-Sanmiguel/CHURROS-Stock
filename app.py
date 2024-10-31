from flask import Flask, jsonify, request, render_template
import json
import uuid
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def unique_uuid(existing_uuids):
    new_uuid = str(uuid.uuid4())
    while new_uuid in existing_uuids:
        new_uuid = str(uuid.uuid4())
    return new_uuid

def convint(elec):
    try:
        eleccion = int(elec)
        return eleccion
    except ValueError:
        return -1

def matrix_read():
    with open('archivos.json', 'r') as file:
        data = json.load(file)
        existing_uuids = {item.get("UUID") for item in data if "UUID" in item}
        matrix = [[int(item['Articulo']), item['Color'], int(item['Size']), int(item['Quantity']), int(item['Price']), item.get("UUID", unique_uuid(existing_uuids))] for item in data]
        return matrix, existing_uuids

def guardar(matrix):
    data_nueva = [
        {"Articulo": item[0], "Color": item[1], "Size": item[2], "Quantity": item[3], "Price": item[4], "UUID": item[5]} 
        for item in matrix
    ]
    with open('archivos.json', 'w') as file:
        json.dump(data_nueva, file, indent=4)

@app.route('/matrix', methods=['GET'])
def get_matrix():
    matrix, _ = matrix_read()
    return jsonify(matrix)

@app.route('/matrix', methods=['POST'])
def add_or_remove_stock():
    data = request.json
    accion = data.get("accion")
    articulo = data.get("articulo")
    color = data.get("color")
    talle = data.get("talle")
    cantidad = data.get("cantidad")

    matrix, existing_uuids = matrix_read()
    articulo_existe = False

    for i, item in enumerate(matrix):
        if item[0] == articulo and item[1] == color and item[2] == talle:
            articulo_existe = True
            if accion == "AGREGAR":
                matrix[i][3] += cantidad
            elif accion == "ELIMINAR" and matrix[i][3] >= cantidad:
                matrix[i][3] -= cantidad
            guardar(matrix)
            return jsonify({"message": f"Stock actualizado. Nueva cantidad: {matrix[i][3]}"})

    if not articulo_existe and accion == "AGREGAR":
        nuevo_item = [articulo, color, talle, cantidad, data.get("precio"), unique_uuid(existing_uuids)]
        matrix.append(nuevo_item)
        guardar(matrix)
        return jsonify({"message": "Nuevo artículo agregado", "item": nuevo_item})

    return jsonify({"error": "Artículo no encontrado"}), 404

@app.route('/matrix', methods=['DELETE'])
def delete_stock():
    data = request.json
    articulo = data.get("articulo")
    color = data.get("color")
    talle = data.get("talle")
    cantidad = data.get("cantidad")

    matrix, _ = matrix_read()
    articulo_existe = False

    for i, item in enumerate(matrix):
        if item[0] == articulo and item[1] == color and item[2] == talle:
            articulo_existe = True
            if matrix[i][3] >= cantidad:
                matrix[i][3] -= cantidad
                if matrix[i][3] == 0:
                    matrix.pop(i)
                    guardar(matrix)
                    return jsonify({"message": f"Artículo {articulo} eliminado del stock"})
                guardar(matrix)
                return jsonify({"message": f"Stock actualizado. Nueva cantidad: {matrix[i][3]}"})
            else:
                return jsonify({"error": f"No se puede eliminar {cantidad} unidades; solo hay {matrix[i][3]} en stock"}), 400

    if not articulo_existe:
        return jsonify({"error": "Artículo no encontrado"}), 404


def cargar_usuarios():
    with open('credenciales.json', 'r') as arch:
        datos = json.load(arch)
    return datos if isinstance(datos, list) else []

def guardar_credenciales(credenciales):
    with open('credenciales.json', 'w') as arch:
        json.dump(credenciales, arch)

@app.route('/stock/total', methods=['GET'])
def get_total_stock():
    matrix, _ = matrix_read()
    stock_total = sum(item[3] for item in matrix)
    return jsonify({"stock_total": stock_total})

@app.route('/stock/articulo/<int:articulo>', methods=['GET'])
def get_stock_articulo(articulo):
    matrix, _ = matrix_read()
    stock_art = sum(item[3] for item in matrix if item[0] == articulo)
    if stock_art > 0:
        return jsonify({"stock_articulo": stock_art})
    return jsonify({"error": f"Artículo '{articulo}' no encontrado"}), 404

@app.route('/stock/especifico', methods=['GET'])
def get_stock_especifico():
    articulo = request.args.get('articulo', type=int)
    talle = request.args.get('talle', type=int)
    color = request.args.get('color')

    matrix, _ = matrix_read()
    for item in matrix:
        if item[0] == articulo and item[1] == color and item[2] == talle:
            return jsonify({"stock_especifico": item[3]})
    return jsonify({"error": "Artículo o variación no encontrado"}), 404

@app.route('/matrix/slice', methods=['GET'])
def get_matrix_slice():
    matrix, _ = matrix_read()
    sliced_matrix = [item[:5] for item in matrix]
    return jsonify(sliced_matrix)

@app.route('/usuario/registrar', methods=['POST'])
def registrar_usuario():
    data = request.json
    email = data.get("email")
    contraseña = data.get("contraseña")

    credenciales = cargar_usuarios()
    credenciales.append({"user": email, "pass": contraseña})
    guardar_credenciales(credenciales)
    return jsonify({"message": "Registro exitoso"})

@app.route('/usuario/login', methods=['POST'])
def iniciar_sesion():
    data = request.json
    email = data.get("email")
    contraseña = data.get("contraseña")

    credenciales = cargar_usuarios()
    for credencial in credenciales:
        if credencial['user'] == email and credencial['pass'] == contraseña:
            return jsonify({"message": "Inicio de sesión exitoso"})
    return jsonify({"error": "Correo electrónico o contraseña no válidos"}), 401

if __name__ == '__main__':
    app.run(debug=True)
