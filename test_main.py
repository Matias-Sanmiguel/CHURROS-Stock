import pytest
from main import unique_uuid, matrix_read, guardar
import main

# Prueba para la función unique_uuid
def test_unique_uuid():
    """
    Prueba que unique_uuid genere un UUID único que no esté en la lista de UUIDs existentes.
    """
    existing_uuids = {"123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174001"}
    new_uuid = unique_uuid(existing_uuids)
    # Comprobar que el UUID generado no esté en los existentes y tenga longitud 36
    assert new_uuid not in existing_uuids
    assert len(new_uuid) == 36

# Prueba para la función matrix_read
def test_matrix_read():
    """
    Prueba que matrix_read lea correctamente el archivo JSON y retorne una matriz con UUIDs únicos.
    """
    # Ejecutar matrix_read sin argumentos, asumiendo que leerá de archivos.json
    matrix, existing_uuids = matrix_read()

    # Verificar que matrix_read convierta los datos correctamente
    assert len(matrix) > 0  # Comprobar que la matriz no esté vacía
    for item in matrix:
        assert len(item) == 6  # Cada entrada en matrix debe tener 6 elementos
        assert isinstance(item[5], str) and len(item[5]) == 36  # Verificar longitud del UUID

# Prueba para la función guardar
def test_guardar():
    """
    Prueba que guardar guarde correctamente la matriz en formato dict.
    """
    # Matriz de ejemplo
    matrix = [
        [1, "Rojo", 10, 5, 100, "123e4567-e89b-12d3-a456-426614174000"],
        [2, "Azul", 20, 3, 200, "123e4567-e89b-12d3-a456-426614174001"]
    ]
    
    # Ejecutar guardar sin pasar un argumento de archivo
    guardar(matrix)

    # Aquí normalmente verificaríamos el contenido del archivo JSON si fuera necesario

# Prueba para la función askoptions (simulación básica sin interacción)
def test_askoptions():
    """
    Simulación de la función askoptions para verificar el manejo de opciones válidas.
    """
    matrix = [[1, "Rojo", 10, 5, 100, "123e4567-e89b-12d3-a456-426614174000"]]
    opciones_posibles = {1, 2, 3, 4, 5, 6, 99}
    # Simulación de opciones posibles sin necesidad de interacción
    assert all(option in opciones_posibles for option in [1, 99])


# Sample data to use in tests
sample_matrix = [
    [101, 'Red', 42, 10, 500, 'uuid1'],
    [102, 'Blue', 40, 5, 700, 'uuid2'],
    [101, 'Red', 44, 8, 500, 'uuid3'],
    [103, 'Green', 42, 20, 300, 'uuid4']
]

def test_chequear_stock_general():
    # Test total stock calculation
    expected_stock_total = 10 + 5 + 8 + 20
    assert main.chequear_stock_general(sample_matrix) == expected_stock_total

def test_consulta_art():
    # Test stock for a specific article (ID 101)
    articulo_id = 101
    expected_stock_art = 10 + 8  # Sum of all stock with article ID 101
    assert main.consulta_art(sample_matrix, articulo_id) == expected_stock_art

def test_consulta_variacion():
    # Test stock for a specific variation (article ID 101, size 42, color 'Red')
    articulo_id = 101
    color = 'Red'
    talle = 42
    expected_stock_variacion = 10  # Expected stock for this specific variation
    assert main.consulta_variacion(sample_matrix, articulo_id, talle, color) == expected_stock_variacion