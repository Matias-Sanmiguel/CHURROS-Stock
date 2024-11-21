from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import json
import uuid
import numpy as np

app = Flask(__name__)
app.secret_key = 'super_secret_key'



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
        matrix = np.array([[int(item['Articulo']), item['Color'], int(item['Size']), int(item['Quantity']), int(item['Price']), item.get("UUID", unique_uuid(existing_uuids))] for item in data], dtype=object)
        return matrix, existing_uuids

def guardar(matrix):
    data_nueva = [
        {"Articulo": int(item[0]), "Color": item[1], "Size": int(item[2]), "Quantity": int(item[3]), "Price": int(item[4]), "UUID": item[5]}
        for item in matrix
    ]
    with open('archivos.json', 'w') as file:
        json.dump(data_nueva, file, indent=4)

@app.route('/fastadd', methods=['POST'])
def fastadd():
    data = request.json
    articulo = convint(data.get("articulo", -1))
    color = data.get("color")
    talle = convint(data.get("talle", -1))
    accion = data.get("accion", "").upper()
    cantidad = convint(data.get("cantidad", -1))
    precio = convint(data.get("precio", -1)) if accion == "AGREGAR" else None

    if articulo == -1 or talle == -1 or cantidad == -1 or not color or accion not in ["AGREGAR", "ELIMINAR"]:
        return jsonify({"error": "Datos inválidos o incompletos"}), 400

    matrix, existing_uuids = matrix_read()
    articulo_existe = False

    for i in range(matrix.shape[0]):
        if matrix[i, 0] == articulo and matrix[i, 1] == color and matrix[i, 2] == talle:
            articulo_existe = True
            if accion == "AGREGAR":
                matrix[i, 3] += cantidad
                guardar(matrix)
                return jsonify({"message": f"Stock actualizado para el artículo {articulo}. Nueva cantidad: {matrix[i, 3]}"}), 200
            elif accion == "ELIMINAR":
                if matrix[i, 3] >= cantidad:
                    matrix[i, 3] -= cantidad
                    if matrix[i, 3] == 0:
                        matrix = np.delete(matrix, i, axis=0)
                        guardar(matrix)
                        return jsonify({"message": f"Artículo {articulo} eliminado del stock"}), 200
                    guardar(matrix)
                    return jsonify({"message": f"Stock actualizado para el artículo {articulo}. Nueva cantidad: {matrix[i, 3]}"}), 200
                else:
                    return jsonify({"error": f"No se puede eliminar {cantidad} unidades. Solo hay {matrix[i, 3]} en stock"}), 400

    if not articulo_existe and accion == "AGREGAR":
        if precio == -1:
            return jsonify({"error": "Necesitas agregar un precio"}), 400
        nuevo_item = np.array([[articulo, color, talle, cantidad, precio, unique_uuid(existing_uuids)]], dtype=object)
        matrix = np.append(matrix, nuevo_item, axis=0)
        guardar(matrix)
        return jsonify({"message": f"Nuevo artículo agregado: {nuevo_item.tolist()}"}), 201

    if not articulo_existe and accion == "ELIMINAR":
        return jsonify({"error": "No se puede eliminar stock de un artículo no existente"}), 404



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

def cargar_usuarios():
    try:
        with open('credenciales.json', 'r') as archivo:
            usuarios = json.load(archivo)
        print("Usuarios cargados:", usuarios)
        return usuarios if isinstance(usuarios, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error al cargar usuarios:", e) 
        return []

def guardar_usuarios(credenciales):
    with open('credenciales.json', 'w') as archivo:
        json.dump(credenciales, archivo, indent=4)

@app.route('/')
def index():
    if 'user' in session:
        return f'Bienvenido, {session["user"]}! <a href="/logout">Cerrar sesión</a>'
    return render_template('index.html')

@app.route('/stock.html')
def stock():
    return render_template('stock.html')


@app.route('/usuario/registrar', methods=['POST'])
def registrar_usuario():

    verificarArroba = lambda correo: correo.find('@') == correo.rfind('@') and '@' in correo
    verificarAlfanum = lambda correo: correo[:correo.find('@')].isalnum()
    verificarFinal = lambda correo: correo.endswith('.com')
    verificarDominio = lambda correo: len(correo[correo.find('@')+1:].rstrip('.com')) > 0

    validarMail = lambda correo: (verificarArroba(correo) and
                                verificarAlfanum(correo) and
                                verificarFinal(correo) and
                                verificarDominio(correo))

    verificarLetrasNumeros = lambda contra: contra.isalnum()
    verificarCantLetras = lambda contra: len(contra) >= 8
    verificarMayus = lambda contra: any(c.isupper() for c in contra)
    verificarLetras = lambda contra: any(c.isalpha() for c in contra)
    verificarNum = lambda contra: any(c.isdigit() for c in contra)

    validarContraseña = lambda contraseña: (verificarLetrasNumeros(contraseña) and
                                            verificarCantLetras(contraseña) and
                                            verificarMayus(contraseña) and
                                            verificarLetras(contraseña) and
                                            verificarNum(contraseña))
                                            
    data = request.json
    email = data.get("user")
    contraseña = data.get("pass")

    if not validarMail(email):
        return jsonify({"error": "El correo electrónico no es válido."}), 400

    if not validarContraseña(contraseña):
        return jsonify({"error": "La contraseña no cumple con los requisitos: alfanumérica, mínimo 8 caracteres, al menos una mayúscula, un número y una letra."}), 400

    usuarios = cargar_usuarios()

    if any(u["user"] == email for u in usuarios):
        return jsonify({"error": "El correo electrónico ya está registrado."}), 400

    usuarios.append({"user": email, "pass": contraseña})
    guardar_usuarios(usuarios)

    return jsonify({"message": "Registro exitoso"}), 200


@app.route('/usuario/login', methods=['POST'])
def iniciar_sesion():
    data = request.json
    print("Datos recibidos:", data)
    email = data.get("user")
    contraseña = data.get("pass")

    usuarios = cargar_usuarios()
    print("Verificando usuarios...") 

    for usuario in usuarios:
        print(f"Comparando con: {usuario}")
        if usuario['user'] == email and usuario['pass'] == contraseña:
            session['user'] = email
            return jsonify({"redirect": "/stock.html"}), 200

    return jsonify({"error": "Correo electrónico o contraseña no válidos"}), 401


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
