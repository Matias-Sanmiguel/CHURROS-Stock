import pandas as pd


#Lee el csv por pandas y lo traduce a matrices
def matrix_read():
    df = pd.read_csv('prueba.csv')
    matrix = df.values
    print(matrix)
    return matrix

def askoptions(matrix):
    flag = 0
    opciones_posibles=[1, 2, 3, 4, 5, 99]
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
        agregar_stock(matrix)
    if eleccion == 3:
        stock = chequear_stock_general(matrix)
        print(matrix)
        print("El stock total es de: ", stock)
    if eleccion == 4:
        stock_art()
    if eleccion == 5:
        stock_esp()


        
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

def sumres(matrix,cumplidores2, value, sign, agr):
    if sign == "ELIMINAR":
        if agr <= value:
            matrix = (matrix[3][cumplidores2[0]] - agr)
            return -1, matrix
        else:
            print("Ingrese un numero menor o igual al stock el articulo seleccionado")
            return 0, 0
    else:
        if agr > 0:
            matrix = (matrix[3][cumplidores2[0]] + agr)
            return -1, matrix
        else:
            print("Ingrese un numero mayor a 0")
            return 0, 0

def busqueda(info1, info2, info3, first, esint):
    print(info1)
    if first == True:
        print(info2)
    else:
        for i in range(len(info2)):
            num = info2[i]
            print(matrix[num])
    data_pre = input()
    if esint == True:
        data = convint(data_pre)
    else:
        data = data_pre
    cumplidores = []
    for i in range(len(matrix)):
        if data == matrix[i][int(info3)]:
            cumplidores.append(i)
    if len(cumplidores) == 0:
        print("Ese nro de artículo no existe")
        return 0, 0
    else:
        return 1, cumplidores

def agregar_stock(matrix):
    flag = 0
    opciones_posibles=[1, 2, 99]
    while flag != 1:
        print("""
              Agregar stock: 1
              Eliminar stock: 2
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
        flag = 0
        flag1 = 0
        flag2 = 0
        agr = -1
        
        while flag == 0:
            print("Agregar stock") 
            info1 = "Elija un articulo al que quiera agregar el stock:"
            info2 = matrix
            info3 = 0
            first = True
            esint = True
            flag, cumplidores = busqueda(info1, info2, info3, first, esint)
            if flag == 0:
                print("El nro de articulo seleccionado no existe")
        
        while flag1 == 0:
            info1 = "Elija un color de articulo al que quiera agregar el stock:"
            info2 = cumplidores
            info3 = 1
            esint = False
            first = False
            flag1, cumplidores1 = busqueda(info1, info2, info3, first, esint)
            if flag1 == 0:
                print("El color de articulo seleccionado no existe")
            
        while flag2 == 0:
            info1 = "Elija el talle de articulo al que quiera agregar el stock:"
            info2 = cumplidores1
            info3 = 2
            esint = True
            first = False
            flag2, cumplidores2 = busqueda(info1, info2, info3, first, esint)
            if flag2 == 0:
                print("El talle de articulo seleccionado no existe")
                
        while agr == -1:
            flag = 0
            info = "AGREGAR"
            agr = final(agr, cumplidores2, info)
            value = matrix[3][cumplidores2[0]]
            while flag != -1:
                flag, matrix = sumres(matrix,cumplidores2, value, info, agr)
            print("Nueva matriz: ")
            print(matrix)
            
            
    if eleccion == 2:
        flag = 0
        flag1 = 0
        flag2 = 0
        agr = -1
    
        while flag == 0:
            print("Eliminar stock") 
            info1 = "Elija un articulo al que quiera eliminar el stock:"
            info2 = matrix
            info3 = 0
            first = True
            esint = True
            flag, cumplidores = busqueda(info1, info2, info3, first, esint)
            if flag == 0:
                print("El nro de articulo seleccionado no existe")

        while flag1 == 0:
            info1 = "Elija un color de articulo al que quiera eliminar el stock:"
            info2 = cumplidores
            info3 = 1
            esint = False
            first = False
            flag1, cumplidores1 = busqueda(info1, info2, info3, first, esint)
            if flag1 == 0:
                print("El color de articulo seleccionado no existe")

        while flag2 == 0:
            info1 = "Elija el talle de articulo al que quiera eliminar al stock:"
            info2 = cumplidores1
            info3 = 2
            esint = True
            first = False
            flag2, cumplidores2 = busqueda(info1, info2, info3, first, esint)
            if flag2 == 0:
                print("El talle de articulo seleccionado no existe")

        while agr == -1:
            flag = 0
            info = "ELIMINAR"
            agr = final(agr, cumplidores2, info)
            value = matrix[3][cumplidores2[0]]
            while flag != -1:
                flag, matrix = sumres(matrix,cumplidores2, value, info, agr)
            print("Nueva matriz: ")
            print(matrix)
            
    
def final(agr, cumplidores2, info):
    print("El articulo seleccionado es: ", matrix[cumplidores2])
    print("Cuantos artículos desea", info, ":")
    pre_agr = input()
    agr = convint(pre_agr)
    return agr
    
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
                    opciones_posibles = [1, 99]
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
                    opciones_posibles = [1, 99]
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
    askoptions(matrix)


if __name__ == '__main__':
    matrix = matrix_read()
    main1(matrix)

