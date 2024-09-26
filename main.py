import pandas as pd
import numpy as np
import json


#Lee el csv por pandas y lo traduce a matrices
def matrix_read():
    df = pd.read_csv('prueba.csv')
    matrix = df.values
    print(matrix)
    return matrix

def guardar(matriz):
    csv = 'prueba.csv'
    df = pd.DataFrame(matriz)
    df.to_csv(csv, index=False, header=False)

def askoptions(matrix):
    flag = 0
    opciones_posibles={1, 2, 3, 4, 5, 99}
    while flag != 1:
        print("""
              
              AGREGAR / ELIMINAR stock: 1
              AGREGAR / ELIMINAR articulos: 2
              CONSULTAR stock total: 3
              CONSULTAR stock de un ART: 4
              CONSULTAR stock específico: 5 
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
        
    if eleccion == 2:
        ag_el_a(matrix)
        
    if eleccion == 3:
        stock = chequear_stock_general(matrix)
        print(matrix)
        print("El stock total es de: ", stock)
        
    if eleccion == 4:
        stock_art()
        
    if eleccion == 5:
        stock_esp()

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
                matrix[i][3] += cantidad
                print(f"Stock actualizado para el artículo {articulo} con color {color} y talle {talle}. Nueva cantidad: {matrix[i][3]}")
                guardar(matrix)
                askoptions(matrix)
            
            elif accion == "ELIMINAR":
                if matrix[i][3] >= cantidad:
                    
                    matrix[i][3] -= cantidad
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
        linea.append(precio)
        matrix.append(linea)  
        print(f"Nuevo artículo agregado: {linea}")
        guardar(matrix)
        askoptions(matrix)
    
    elif not articulo_existe and accion == "ELIMINAR":
        print("Error: No se puede eliminar stock de un artículo que no existe.")
    



        
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

# def sumres(matrix, cumplidores2, value, sign, agr):
#     fila_articulo = cumplidores2[0]
    
#     if sign == "ELIMINAR":
#         if agr <= value:
#             matrix[fila_articulo][3] -= agr  # Restar stock
#             return -1, matrix
#         else:
#             print("Ingrese un número menor o igual al stock del artículo seleccionado")
#             return 0, matrix
#     else:  # AGREGAR
#         if agr > 0:
#             matrix[fila_articulo][3] += agr  # Sumar stock
#             return -1, matrix
#         else:
#             print("Ingrese un número mayor a 0")
#             return 0, matrix


# def busqueda(info1, info2, info3, first, esint):
#     print(info1)
#     if first == True:
#         print(info2)
#     else:
#         for i in range(len(info2)):
#             num = info2[i]
#             print(matrix[num])
#     data_pre = input()
#     if esint == True:
#         data = convint(data_pre)
#     else:
#         data = data_pre
#     cumplidores = []
#     for i in range(len(matrix)):
#         if data == matrix[i][int(info3)]:
#             cumplidores.append(i)
#     if len(cumplidores) == 0:
#         print("Ese nro de artículo no existe")
#         return 0, 0
#     else:
#         return 1, cumplidores

# def agregar_stock(matrix):
#     flag = 0
#     opciones_posibles = [1, 2, 99]
    
#     while flag != 1:
#         print("""
#               Agregar stock: 1
#               Eliminar stock: 2
#               Salir: 99
#               """)
#         print("Elija una opción: ")
#         eleccion_pre_int = input()
#         eleccion = convint(eleccion_pre_int)
        
#         flag = checker_opt(eleccion, opciones_posibles)
        
#     if eleccion == 99:
#         print("Gracias por usar nuestro software. Saliendo...")
#         return
    
#     # Elección de agregar o eliminar stock
#     if eleccion in [1, 2]:
#         operacion = "AGREGAR" if eleccion == 1 else "ELIMINAR"
        
#         # Selección del artículo
#         flag = 0
#         while flag == 0:
#             print(f"{operacion} stock")
#             info1 = "Elija un artículo al que quiera agregar/eliminar el stock:"
#             info2 = matrix
#             info3 = 0  # El campo de ID de artículo
#             first = True
#             esint = True
#             flag, cumplidores = busqueda(info1, info2, info3, first, esint)
#             if flag == 0:
#                 print("El número de artículo seleccionado no existe.")
        
#         # Selección del color
#         flag1 = 0
#         while flag1 == 0:
#             info1 = "Elija un color de artículo:"
#             info2 = cumplidores
#             info3 = 1  # El campo de color
#             esint = False
#             first = False
#             flag1, cumplidores1 = busqueda(info1, info2, info3, first, esint)
#             if flag1 == 0:
#                 print("El color de artículo seleccionado no existe.")
        
#         # Selección del talle
#         flag2 = 0
#         while flag2 == 0:
#             info1 = "Elija el talle del artículo:"
#             info2 = cumplidores1
#             info3 = 2  # El campo de talle
#             esint = True
#             first = False
#             flag2, cumplidores2 = busqueda(info1, info2, info3, first, esint)
#             if flag2 == 0:
#                 print("El talle de artículo seleccionado no existe.")
        
#         # Solicitar la cantidad a agregar/eliminar
#         agr = -1
#         while agr == -1:
#             agr = final(agr, cumplidores2, operacion)
#             value = matrix[cumplidores2[0]][3]  # Acceder al stock del artículo seleccionado
            
#             # Realizar la operación de sumar o restar stock
#             flag, matrix = sumres(matrix, cumplidores2, value, operacion, agr)
        
#         print("Nueva matriz: ")
#         print(matrix)
            
    
# def final(agr, cumplidores2, info):
#     print("El articulo seleccionado es: ", matrix[cumplidores2])
#     print("Cuantos artículos desea", info, ":")
#     pre_agr = input()
#     agr = convint(pre_agr)
#     return agr
    
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


def stock_art():
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
                art = -1
                while art == -1:
                    print("Ingrese un artículo: ")
                    art_pre = input()
                    art = convint(art_pre)
                    stock = consulta_art(matrix, art)
                    print("El stock del articulo ",art," es: ", stock)
                    empezado = True
        
        
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
# Inicio de sesion
def registrarUsuario():
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
        if credencial["user"] == email:
            print("El correo ya está registrado")
            return
    
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




def ag_el_a(matrix):
    flag = 0
    opciones_posibles = {1, 2, 99}
    
    while flag != 1:
        print("""
              AGREGAR artículos: 1
              ELIMINAR artículos: 2
              Salir: 99
              """)
        print("Elija una opción: ")
        eleccion_pre_int = input()
        eleccion = convint(eleccion_pre_int)
        
        flag = checker_opt(eleccion, opciones_posibles)
    
    if eleccion == 1:
        cantidadart_pre = input("Ingrese la cantidad de artículos que desea ingresar: ")
        cantidadart = convint(cantidadart_pre)
        
        if cantidadart == -1:
            print("Ingrese un número entero válido")
        else:
            for fila in range(cantidadart):
                art = []
                
                while True:
                    articulo_pre = input("Ingrese el número de artículo: ")
                    articulo = convint(articulo_pre)
                    if articulo == -1:
                        print("Ingrese un número entero válido")
                    else:
                        break
                
                exists = any(row[0] == articulo for row in matrix)
                if exists:
                    print("El artículo ya existe en el inventario")
                else:
                    col = input("Ingrese el color: ")
                    while True:
                        tal_pre = input("Ingrese el número de talle: ")
                        tal = convint(tal_pre)
                        if tal == -1:
                            print("Ingrese un número entero válido")
                        else:
                            break
                    
                    while True:
                        pre_pre = input("Ingrese el precio del artículo: ")
                        pre = convint(pre_pre)
                        if pre == -1:
                            print("Ingrese un número entero válido")
                        else:
                            break
                    
                    stock = 0  
                    art = [articulo, col, tal, stock, pre]
                    matrix = np.append(matrix, [art], axis=0)
                    guardar(matrix)
                    askoptions(matrix)
    
    elif eleccion == 2:
        print(matrix)
        
        cantidadart_pre = input("Ingrese la cantidad de artículos que desea eliminar: ")
        cantidadart = convint(cantidadart_pre)
        
        if cantidadart == -1:
            print("Ingrese un número entero válido")
        else:
            for _ in range(cantidadart):
                while True:
                    articulo_pre = input("Ingrese el número de artículo que desea eliminar: ")
                    articulo = convint(articulo_pre)
                    if articulo == -1:
                        print("Ingrese un número entero válido")
                    else:
                        break
                
                for i, row in enumerate(matrix): 
                    if row[0] == articulo:
                        col = input("Ingrese el color: ")
                        while True:
                            tal_pre = input("Ingrese el número de talle: ")
                            tal = convint(tal_pre)
                            if tal == -1:
                                print("Ingrese un número entero válido")
                            else:
                                break
                        
                        if col == row[1] and tal == row[2]:
                            matrix = np.delete(matrix, i, axis=0)
                            print(f"Artículo {articulo} eliminado")
                            guardar(matrix)
                            askoptions(matrix)
                            break
                else:
                    print("El artículo no se encontró.")
    
    if eleccion == 99:
        print("Gracias por usar nuestro software. Saliendo...")

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
    matrix = matrix_read()
    main1(matrix)


