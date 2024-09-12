matrix = [[2000, 'AZU', 90, 3, 1000],
 [2000, 'AZU', 95, 4, 1000],
 [2001, 'ROJ', 90, 2, 3000],
 [2001, 'NEG', 90, 1, 1500],
 [3000, 'ROJ', 90, 1, 2000],
 [3001, 'ROJ', 90, 1, 7000]]

def ag_el_a(matrix):
    flag = 0
    opciones_posibles=[1, 2, 99]
    while flag != 1:
        print("""
              
              AGREGAR articulos: 1
              ELIMINAR articulos: 2
              Salir: 99
              """)
        print("Elija una opción: ")
        eleccion_pre_int = input()
        eleccion = convint(eleccion_pre_int)
        
        flag = checker_opt(eleccion, opciones_posibles)
    
    if eleccion==1:
        flag=-1
        cantidadart_pre= int(input("ingrese la cantidad de articulos que desea ingresar: "))
        flag=convint(cantidadart_pre)
        if flag==-1:
            print("ingrese un numero entero")
        else:
            cantidadart=int(cantidadart_pre)
            for fila in range(0, cantidadart):
                art=[]
                flag=-1
                while flag==-1:
                    articulo_pre = int(input("Ingrese el numero de articulo que desea ingresar: "))
                    flag=convint(articulo_pre)
                    if flag==-1:
                        print("ingrese un numero entero")
                    else:
                        articulo=int(articulo_pre)
                        for i in range(fila):
                            if articulo==matrix[i][0]:
                                print(fila)
                                print("ingrese los datos del articulo", i+1)
                                col=input("Ingrese el color que quiere ingresar: ")
                                flag=-1
                                while flag==-1:
                                    tal_pre=int(input("Ingrese el numero de talle que desea ingresar: "))
                                    flag=convint(tal_pre)
                                    if flag==-1:
                                        print("ingrese un numero entero")
                                    else:
                                        tal=int(tal_pre)
                                        pre=matrix[i][4]
                                        art.append(articulo)
                                        art.append(col)
                                        art.append(tal)
                                        stock=0
                                        art.append(stock)
                                        art.append(pre)
                                        matrix.append(art)
                        else:
                            print("No existe ese numero de articulo en el inventario")
                            flag=-1
                            while flag==-1:
                                narticulo_pre=int(input("Ingrese el numero del nuevo articulo: "))
                                flag=convint(narticulo_pre)
                                if flag==-1:
                                    print("ingrese un numero entero")
                                else:
                                    narticulo=int(narticulo_pre)
                                    print("Ingrese los datos del articulo", i+1)
                                    col=input("Ingrese el color que quiere ingresar: ")
                                    flag=-1
                                    while flag==-1:
                                        tal_pre=int(input("Ingrese el numero de talle que desea ingresar: "))
                                        flag=convint(tal_pre)
                                        if flag==-1:
                                            print("ingrese un numero entero")
                                        else:
                                            tal=int(tal_pre)
                                            flag=-1
                                            while flag==-1:
                                                pre_pre=int(input("Ingrese el precio del articulo nuevo: "))
                                                flag=convint(pre_pre)
                                                if flag==-1:
                                                    print("ingrese un numero entero")
                                                else:
                                                    pre=int(pre_pre)
                                                    art.append(narticulo)
                                                    art.append(col)
                                                    art.append(tal)
                                                    stock=0
                                                    art.append(stock)
                                                    art.append(pre)
                                                    matrix.append(art)

        for i in range(0,cantidadart):
            print("datos del articulo: ",i+1)
            print("numero de articulo: ",art[i][0],"color: ",art[i][1],"talle: ",art[i][2])
    elif eleccion==2:
        print(matrix)
        flag=-1
        while flag==-1:
            cantidadart_pre= int(input("ingrese la cantidad de articulos que desea eliminar: "))
            flag=convint(cantidadart_pre)
            if flag==-1:
                print("ingrese un numero entero")
            else:
                cantidadart=int(cantidadart_pre)
                for fila in range(0, cantidadart):
                    flag=-1
                    while flag==-1:
                        articulo_pre = int(input("Ingrese el numero de articulo que desea eliminar: "))
                        flag=convint(articulo_pre)
                        if flag==-1:
                            print("ingrese un numero entero ")
                        else:
                            articulo=int(articulo_pre)
                            for i in range(fila):
                                if articulo==matrix[i][0]:
                                    print(fila)
                                    print("ingrese los datos del articulo", i+1)
                                    col=input("Ingrese el color que quiere eliminar: ")
                                    flag=-1
                                    while flag==-1:
                                        tal_pre=int(input("Ingrese el numero de talle que desea eliminar: "))
                                        flag=convint(tal_pre)
                                        if flag==-1:
                                            print("ingrese un numero entero ")
                                        else:
                                            tal=int(tal_pre)
                                            if col==matrix[i][1] and tal==matrix[i][2]:
                                                matrix.pop(fila)
            
if eleccion == 99:
    print("""Gracias por usar nuestro software
        Saliendo...""")