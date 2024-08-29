def consulta(matrix, articulo):
    for fila in matrix:
        if fila[0] == articulo:
            print(f"El stock actual de '{articulo}' es: {fila[1]}")
            return fila[1]
    print(f"El artículo '{articulo}' no fue encontrado en el stock.")
    return None