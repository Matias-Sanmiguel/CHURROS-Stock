import pandas as pd


#Lee el csv por pandas y lo traduce a matrices
def matrix_read():
    df = pd.read_csv('prueba.csv')
    matrix = df.values
    print(matrix)
    return matrix

def sumres(matrix,cumplidores2, value, sign, agr, stock_column=3):
    if not cumplidores2 or stock_column >= len(matrix[0]):
        print("Error: Índice de stock inválido o lista de cumplidores vacía.")
        return 0, matrix
    
    current_stock = matrix[cumplidores2[0]][stock_column]  # Valor actual del stock
    
    if sign == "ELIMINAR":
        if agr <= current_stock:
            # Eliminar stock
            matrix[cumplidores2[0]][stock_column] -= agr
            return -1, matrix
        else:
            print("Ingrese un número menor o igual al stock del artículo seleccionado.")
            return 0, matrix
    else:
        if agr > 0:
            # Agregar stock
            matrix[cumplidores2[0]][stock_column] += agr
            return -1, matrix
        else:
            print("Ingrese un número mayor a 0.")
            return 0, matrix


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
    
### despues agregar una opcion para poder salir de una
def askoptions(matrix):
    flag = 0
    opciones_posibles=[1, 2, 3, 99]
    while flag != 1:
        print("""
              
              AGREGAR / ELIMINAR stock: 1
              AGREGAR / ELIMINAR articulos: 2
              CONSULTAR stock: 3 
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


def busqueda(info1, info2, info3, first, esint):
    print(info1)  # Muestra la información de entrada
    if first:
        # Si es la primera búsqueda, imprime toda la matriz o las opciones iniciales
        print(info2)
    else:
        # Si no es la primera búsqueda, imprime solo las filas relevantes de info2
        for i in info2:
            print(matrix[i])
    
    # Pide al usuario un input para buscar
    data_pre = input("Ingrese el valor a buscar: ")
    
    # Convierte el input dependiendo de si se espera un entero o no
    data = convint(data_pre) if esint else str(data_pre)
    
    cumplidores = []  # Lista de índices que cumplen con la búsqueda
    
    if not first:
        # Si no es la primera búsqueda, busca entre los índices proporcionados en info2
        for i in info2:
            if data == matrix[i][int(info3)]:
                cumplidores.append(i)
                print(f"Cumplidor encontrado en índice {i}: {matrix[i]}")
    else:
        # Si es la primera búsqueda, busca en toda la matriz
        for i in range(len(matrix)):
            if data == matrix[i][int(info3)]:
                cumplidores.append(i)
                print(f"Cumplidor encontrado en índice {i}: {matrix[i]}")
    
    # Verifica si se encontraron elementos que cumplen con la búsqueda
    if len(cumplidores) == 0:
        print("No se encontraron elementos que cumplan con la búsqueda.")
        return 0, 0
    else:
        return 1, cumplidores

            
    
def final(agr, cumplidores2, info):
    print("El articulo seleccionado es: ", matrix[cumplidores2])
    print("Cuantos artículos desea", info, ":")
    pre_agr = input()
    agr = convint(pre_agr)
    return agr
    
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
                flag, matrix = sumres(matrix, cumplidores2, value, info, agr)
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
            print(cumplidores)
            if flag == 0:
                print("El nro de articulo seleccionado no existe")

        while flag1 == 0:
            info1 = "Elija un color de articulo al que quiera eliminar el stock:"
            info2 = cumplidores
            info3 = 1
            esint = False
            first = False
            flag1, cumplidores1 = busqueda(info1, info2, info3, first, esint)
            print(cumplidores1)
            if flag1 == 0:
                print("El color de articulo seleccionado no existe")

        while flag2 == 0:
            info1 = "Elija el talle de articulo al que quiera eliminar al stock:"
            info2 = cumplidores1
            info3 = 2
            esint = True
            first = False
            flag2, cumplidores2 = busqueda(info1, info2, info3, first, esint)
            print(cumplidores2)
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
            

matrix = matrix_read()
askoptions(matrix)
