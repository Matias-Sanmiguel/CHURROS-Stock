def consultaprodd(matrix, producto):
    for fila in matrix:
        if fila[0] == producto and fila[2] == "Producto":
            print(f"El stock actual del producto '{producto}' es: {fila[1]}")
            return fila[1]
    print(f"El producto {producto}' no fue encontrado en el stock")
    return None