def consulta_variacion(matrix, articulo, talle, color):
    """
    Consulta el stock de una variación específica de un artículo, basada en el talle y el color.
    :param matrix: Matriz de datos con artículos, talles, colores y su stock.
    :param articulo: Nombre del artículo.
    :param talle: Talle de la variación del artículo.
    :param color: Color de la variación del artículo.
    :return: Stock de la variación o None si no se encuentra.
    """
    for fila in matrix:
        if fila[0] == articulo and fila[2] == talle and fila[3] == color:
            print(f"El stock actual de la variación '{articulo} - Talle: {talle} - Color: {color}' es: {fila[1]}")
            return fila[1]
    print(f"La variación '{articulo} - Talle: {talle} - Color: {color}' no fue encontrada en el stock.")
    return None