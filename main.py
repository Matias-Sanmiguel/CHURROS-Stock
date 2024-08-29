import pandas as pd


#Lee el csv por pandas y lo traduce a matrices
def matrix_read():
    df = pd.read_csv('prueba.csv')
    matrix = df.values
    print(matrix)
    return matrix


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
        return 0
    else:
        return 1, cumplidores
    
def final(agr):
    print("El articulo seleccionado es: ", matrix[cumplidores2])
    print("Cuantos artículos desea agregar?: ")
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
            esint = False
            first = False
            flag2, cumplidores2 = busqueda(info1, info2, info3, first, esint)
            if flag2 == 0:
                print("El talle de articulo seleccionado no existe")
                
        while agr == -1:
            agr = final(agr)
            if agr > 0:
                matrix = (matrix[3][cumplidores2] + agr)
            else:
                print("Ingrese un nro positivo")
        
            
                
        




matrix = matrix_read()
askoptions(matrix)
