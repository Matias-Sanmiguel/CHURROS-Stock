def chequear_stock_general(matrix):
    """Calcula el stock total sumando el stock de todos los productos y sus variaciones."""
    stock_total = 0
    for fila in matrix:
        stock_total += fila[1]  # Se asume que la columna 1 es la cantidad de stock
    print(f"El stock total de todos los artículos es: {stock_total}")
    return stock_total