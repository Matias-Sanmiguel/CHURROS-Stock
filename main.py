import numpy as np
import json
import uuid
from fpdf import FPDF

def unique_uuid(existing_uuids):
    new_uuid = str(uuid.uuid4())
    while new_uuid in existing_uuids:
        new_uuid = str(uuid.uuid4())
    return new_uuid

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

def askoptions(matrix):
    flag = 0
    opciones_posibles={1, 2, 3, 4, 5, 6, 7, 99}
    while flag != 1:
        print("""
              
              AGREGAR / ELIMINAR stock: 1
              AGREGAR / ELIMINAR articulos: 2
              CONSULTAR stock total: 3
              CONSULTAR stock de un ART: 4
              CONSULTAR stock específico: 5 
              Ver matriz sin UUID : 6
              Generar reporte : 7
              Salir: 99
              
              """)
        print("Elija una opción: ")
        eleccion_pre_int = input()
        eleccion = convint(eleccion_pre_int)
        
        flag = checker_opt(eleccion, opciones_posibles)
        
        
    if eleccion == 99:
        print("""Gracias por usar nuestro software
              Saliendo...""")
        
    if eleccion == 1:
        # agregar_stock(matrix)
        fastadd(matrix)
        askoptions(matrix)
        
    if eleccion == 2:
        ag_el_a(matrix)
        askoptions(matrix)
        
    if eleccion == 3:
        stock = chequear_stock_general(matrix)
        print(matrix)
        print("El stock total es de: ", stock)
        askoptions(matrix)
        
    if eleccion == 4:
        stock_art()
        askoptions(matrix)
        
    if eleccion == 5:
        stock_esp()
        askoptions(matrix)

    if eleccion == 6:
        matiz_slice(matrix)
        askoptions(matrix)

    if eleccion == 7:
        generar_reporte_json("archivos.json")
        askoptions(matrix)

def fastadd(matrix):
    print("Matriz actual:")
    print(matrix)
    print("A continuación deberá ingresar el número de artículo para agregar o eliminar stock.")
    
    articulo, cantidad, precio, talle = -1, -1, -1, -1
    linea = []


    while articulo == -1:
        articulo_pre = input("Ingrese un artículo: ")
        articulo = convint(articulo_pre)
    linea.append(articulo)
    
    color = input("Ingrese un color: ")
    linea.append(color)

    while talle == -1:
        talle_pre = input("Ingrese un talle: ")
        talle = convint(talle_pre)
    linea.append(talle)

    accion = ""
    while accion not in ["AGREGAR", "ELIMINAR"]:
        accion = input("¿Desea AGREGAR o ELIMINAR stock?: ").upper()

    while cantidad == -1:
        cantidad_pre = input(f"Ingrese una cantidad para {accion}: ")
        cantidad = convint(cantidad_pre)

    articulo_existe = False
    for i in range(len(matrix)):
        if matrix[i][0] == articulo and matrix[i][1] == color and matrix[i][2] == talle:
            articulo_existe = True

            if accion == "AGREGAR":
                matrix[i][3] = int(matrix[i][3]) + cantidad  # stock tiene que ser un numero
                print(f"Stock actualizado para el artículo {articulo} con color {color} y talle {talle}. Nueva cantidad: {matrix[i][3]}")
                guardar(matrix)
                askoptions(matrix)

            elif accion == "ELIMINAR":
                if int(matrix[i][3]) >= cantidad:
                    matrix[i][3] = int(matrix[i][3]) - cantidad
                    print(f"Stock actualizado para el artículo {articulo} con color {color} y talle {talle}. Nueva cantidad: {matrix[i][3]}")
                    guardar(matrix)
                    askoptions(matrix)
                else:
                    print(f"Error: No se puede eliminar {cantidad} unidades. Solo hay {matrix[i][3]} en stock.")
            break

    if not articulo_existe and accion == "AGREGAR":
        while precio == -1:
            precio_pre = input("Ingrese un precio para el nuevo artículo: ")
            precio = convint(precio_pre)
        linea.append(cantidad)
        linea.append(precio)
        
        uuidN = unique_uuid(existing_uuids)
         
        linea.append(uuidN)

        linea = np.expand_dims(linea, axis=0)
        
        matrix = np.append(matrix, linea, axis=0)  
        print(f"Nuevo artículo agregado: {linea}")
        guardar(matrix)
        askoptions(matrix)

    elif not articulo_existe and accion == "ELIMINAR":
        print("Error: No se puede eliminar stock de un artículo que no existe.")
    

from fpdf import FPDF
import json

def consulta_art(matrix, articulo):
    stock_art = 0
    for fila in matrix:
        if fila[0] == articulo:
            stock_art += fila[3]
    if stock_art > 0:
        return f"Consulta de stock para '{articulo}': {stock_art}"
    else: 
        return f"El artículo '{articulo}' no fue encontrado en el stock."  

def chequear_stock_general(matrix):
    stock_total = sum(fila[3] for fila in matrix)
    return f"El stock total de todos los artículos es: {stock_total}"  

def consulta_variacion(matrix, articulo, talle, color):
    for fila in matrix:
        if fila[0] == articulo and fila[2] == talle and fila[1] == color:
            print(f"El stock actual de la variación '{articulo} - Talle: {talle} - Color: {color}' es: {fila[3]}")
            return fila[3]
    print(f"La variación '{articulo} - Talle: {talle} - Color: {color}' no fue encontrada en el stock.")
    return None



class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Reporte de Stock", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

import json
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Reporte de Inventario", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def generar_reporte_json(nombre_archivo_json):
    try:
        with open(nombre_archivo_json, "r") as archivo:
            data = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return

    pdf = PDF()
    pdf.add_page()

    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 10, "Artículo", 1, 0, "C", 1)
    pdf.cell(40, 10, "Color", 1, 0, "C", 1)
    pdf.cell(40, 10, "Talle", 1, 0, "C", 1)
    pdf.cell(40, 10, "Cantidad", 1, 0, "C", 1)
    pdf.cell(40, 10, "Precio", 1, 1, "C", 1)

    pdf.set_font("Arial", "", 10)
    for item in data:
        pdf.cell(40, 10, str(item.get("Articulo", "")), 1)
        pdf.cell(40, 10, str(item.get("Color", "")), 1)
        pdf.cell(40, 10, str(item.get("Size", "")), 1)
        pdf.cell(40, 10, str(item.get("Quantity", "")), 1)
        pdf.cell(40, 10, str(item.get("Price", "")), 1)
        pdf.ln()

    nombre_reporte = "reporte_inventario.pdf"
    pdf.output(nombre_reporte)
    print(f"Reporte guardado como '{nombre_reporte}'.")


        
def checker_opt(elc, lista):
    if elc in lista:
        return 1
    else:
        print("Por favor, elija una opción disponible")
        return 0

def convint(elec):
    try:
        eleccion = int(elec)
        return eleccion
    except ValueError:
        print("Valor Inválido")
        return -1


    
def consulta_art(matrix, articulo):
    stock_art = 0
    for fila in matrix:
        if fila[0] == articulo:
            stock_art += fila[3]
    if stock_art > 0:
        return stock_art
    else: 
        print(f"El artículo '{articulo}' no fue encontrado en el stock.")
        return None

def chequear_stock_general(matrix):
    """Calcula el stock total sumando el stock de todos los productos y sus variaciones."""
    stock_total = 0
    for fila in matrix:
        stock_total += fila[3]  
    print(f"El stock total de todos los artículos es: {stock_total}")
    return stock_total

def consulta_variacion(matrix, articulo, talle, color):
 
    for fila in matrix:
        if fila[0] == articulo and fila[2] == talle and fila[1] == color:
            print(f"El stock actual de la variación '{articulo} - Talle: {talle} - Color: {color}' es: {fila[3]}")
            return fila[3]
    print(f"La variación '{articulo} - Talle: {talle} - Color: {color}' no fue encontrada en el stock.")
    return None

def matiz_slice(matrix):
    for fila in matrix:
        if not isinstance(fila, list):
            print(f"Error: La fila {fila} es de tipo {type(fila)} en lugar de 'list'.")
    
    matrix = [list(fila) if isinstance(fila, set) else fila for fila in matrix]

    return [fila[:5] for fila in matrix]



def stock_art():
    eleccion = -1
    empezado = False

    while eleccion != 99:
        if empezado:
            opciones_posibles = {1, 99}
            print("""
                Seguir : 1
                Salir: 99
            """)
            eleccion_pre = input("Elija una opción: ")
            eleccion = convint(eleccion_pre)
            
            if checker_opt(eleccion, opciones_posibles) == -1:
                print("Opcion no válida. Intente nuevamente.")
                continue 
        else:
            art = -1
            while art == -1 or art == 99:
                art_pre = input("Ingrese un artículo: ")
                art = convint(art_pre)
                
                if art == 99:
                    askoptions(matrix)
                    return 
                
                stock = consulta_art(matrix, art)
                if stock is not None:
                    print(f"El stock del artículo {art} es: {stock}")
                    empezado = True
                    break  
                else:
                    print(f"Artículo {art} no encontrado. Intente nuevamente.")

        
        
def stock_esp():
    eleccion = -1
    empezado = False
    flag = 0
    while eleccion == -1:
        if empezado == True:
                while flag != -1:    
                    opciones_posibles = {1, 99}
                    print("""
                        Seguir : 1
                        Salir: 99""")
                    eleccion_pre = input("Elija una opción: ")
                    eleccion= convint(eleccion_pre)
                    flag = checker_opt(eleccion, opciones_posibles)
        
        else:      
            if eleccion != 99:
                art, col, talle  = -1, -1, -1
                while art == -1:
                    print("Ingrese un artículo: ")
                    art_pre = input()
                    art = convint(art_pre)
                while col == -1:
                    print("Ingrese un color: ")
                    col = input()
                    
                while talle == -1:
                    print("Ingrese un talle: ")
                    talle_pre = input()
                    talle = convint(talle_pre)    
                    stock = consulta_variacion(matrix, art, talle, col)
                    print("El stock del articulo ",art, col, talle," es: ", stock)
                    empezado = True



# Correo


# Inicio de sesion
def registrarUsuario():
    
    verificarArroba = lambda correo: correo.find('@') == correo.rfind('@') and '@' in correo
    verificarAlfanum = lambda correo: correo[:correo.find('@')].isalnum()
    verificarFinal = lambda correo: correo.endswith('.com')
    verificarDominio = lambda correo: len(correo[correo.find('@')+1:].rstrip('.com')) > 0

    validarMail = lambda correo: (verificarArroba(correo) and
                                verificarAlfanum(correo) and
                                verificarFinal(correo) and
                                verificarDominio(correo))

    # Contraseña

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
    
    
    
    credenciales = cargar_usuarios()
    print("Antes de registrar su correo, por favor asegúrese de que cumple con los siguientes requisitos:")
    print("1. Debe contener una sola '@'.")
    print("2. Debe terminar en '.com'.")
    print("3. La parte local (antes de '@') debe ser alfanumérica.")
    print("4. Debe contener un dominio después de '@'.")
    
    email = input("Ingrese tu email: ").strip()
    
    
    while not validarMail(email):
        print("El email ingresado no es valido")
        email = input("Ingrese otro email: ").strip()
        
        
    for credencial in credenciales:
        if credencial["user"] == email and credencial ["pass"] == contraseña:
            print("Inicio de sesión exitoso")
            askoptions(matrix)
            return
        print("Correo electrónico o contraseña no válido")
            
    
    print("Antes de ingresar su contraseña, por favor asegúrese de que cumple con los siguientes requisitos:")
    print("1. No debe contener caracteres especiales.")
    print("2. Debe contener, al menos, un numero.")
    print("3. Debe contener, al menos, una letra minuscula.")
    print("4. Debe contener, al menos, una letra mayuscula.")
    print("5. Debe contener, como minimo, 8 caracteres.")

    contraseña = input("Ingrese su contraseña: ").strip()
    
    while not validarContraseña(contraseña):
        print("La contraseña ingresada no es valida")
        contraseña = input("Ingrese otra contraseña: ").strip()
        
    
    credenciales.append({"user": email, "pass": contraseña})
    guardar_credenciales(credenciales)
    print("Registro exitoso")
    
def iniciarSesion():
    email = input("Ingrese tu email: ").strip()
    contraseña = input("Ingrese su contraseña: ").strip()
    credenciales = cargar_usuarios()
    
    for credencial in credenciales:
        if credencial['user'] == email and credencial['pass'] == contraseña:
            print("Inicio de sesión exitoso")
            askoptions(matrix)
    else:
        print("Correo electronico o contraseña no valido")

def menu():
    while True:
        print("\nOpciones:")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        eleccion = -1
        while eleccion == -1:
            eleccion_pre = input("Seleccione una opcion (1/2/3): ")
            eleccion = convint(eleccion_pre)
        
        if eleccion == 1:
            registrarUsuario()
        elif eleccion == 2:
            iniciarSesion()
            
        elif eleccion == 3:
            print("Saliendo..")
            break
        else:
            print("Opcion no valida, por favor selecciona 1, 2 o 3")




import numpy as np

def ag_el_a(matrix):
    opciones_posibles = {1, 2, 99}
    
    while True:
        print("""
              AGREGAR artículos: 1
              ELIMINAR artículos: 2
              Salir: 99
              """)
        eleccion_pre = input("Elija una opción: ")
        eleccion = convint(eleccion_pre)
        
        if checker_opt(eleccion, opciones_posibles) == -1:
            print("Opción no válida. Intente nuevamente.")
            continue

        if eleccion == 1: 
            cantidadart_pre = input("Ingrese la cantidad de artículos que desea ingresar: ")
            cantidadart = convint(cantidadart_pre)
            
            if cantidadart == -1:
                print("Ingrese un número entero válido.")
                continue
            
            
            existing_uuids = set(row[0] for row in matrix)
            
            for _ in range(cantidadart):
                while True:
                    articulo_pre = input("Ingrese el número de artículo: ")
                    articulo = convint(articulo_pre)
                    if articulo == -1:
                        print("Número de artículo no válido. Intente nuevamente.")
                    else:
                        break

                if any(row[1] == articulo for row in matrix):  # Asumiendo que el UUID es el primer elemento
                    print("El artículo ya existe en el inventario.")
                    continue
                
                col = input("Ingrese el color: ")
                
                while True:
                    tal_pre = input("Ingrese el número de talle: ")
                    tal = convint(tal_pre)
                    if tal == -1:
                        print("Número de talle no válido. Intente nuevamente.")
                    else:
                        break

                while True:
                    pre_pre = input("Ingrese el precio del artículo: ")
                    pre = convint(pre_pre)
                    if pre == -1:
                        print("Precio no válido. Ingrese un número entero.")
                    else:
                        break
                
                stock = 0
                nuevo_uuid = unique_uuid(existing_uuids)
                art = [articulo, col, tal, stock, pre, nuevo_uuid ]
                
                
                matrix = np.append(matrix, [art], axis=0)
                guardar(matrix)
                print(f"Artículo {articulo} agregado exitosamente.")
                
        elif eleccion == 2:
            cantidadart_pre = input("Ingrese la cantidad de artículos que desea eliminar: ")
            cantidadart = convint(cantidadart_pre)
            
            if cantidadart == -1:
                print("Ingrese un número entero válido.")
                continue

            for _ in range(cantidadart):
                while True:
                    articulo_pre = input("Ingrese el número de artículo que desea eliminar: ")
                    articulo = convint(articulo_pre)
                    if articulo == -1:
                        print("Número de artículo no válido. Intente nuevamente.")
                    else:
                        break
                
                for i, row in enumerate(matrix):
                    if row[1] == articulo:
                        col = input("Ingrese el color: ")
                        
                        while True:
                            tal_pre = input("Ingrese el número de talle: ")
                            tal = convint(tal_pre)
                            if tal == -1:
                                print("Número de talle no válido. Intente nuevamente.")
                            else:
                                break
                        
                        if col == row[2] and tal == row[3]:
                            matrix = np.delete(matrix, i, axis=0)
                            print(f"Artículo {articulo} eliminado exitosamente.")
                            guardar(matrix)
                            break
                else:
                    print("Artículo no encontrado en el inventario.")
        
        elif eleccion == 99:
            print("Gracias por usar nuestro software. Saliendo...")
            break

    return matrix


def cargar_usuarios():
    with open('credenciales.json', 'r') as arch: ## el r es para que pueda sobreescribir
        datos = json.load(arch)

    if isinstance(datos, list):
        return datos


def guardar_credenciales(credenciales):
    with open('credenciales.json', 'w') as arch: ## el w es para que pueda sobreescribir
        json.dump(credenciales, arch)

def main1(matrix):
    print(

"""
+==========================================================+
| ██████╗██╗  ██╗██╗   ██╗██████╗ ██████╗  ██████╗ ███████╗|
|██╔════╝██║  ██║██║   ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝|
|██║     ███████║██║   ██║██████╔╝██████╔╝██║   ██║███████╗|
|██║     ██╔══██║██║   ██║██╔══██╗██╔══██╗██║   ██║╚════██║|
|╚██████╗██║  ██║╚██████╔╝██║  ██║██║  ██║╚██████╔╝███████║|
| ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝|
+==========================================================+
"""
)
    menu()


if __name__ == '__main__':
    matrix, existing_uuids = matrix_read()
    main1(matrix)


