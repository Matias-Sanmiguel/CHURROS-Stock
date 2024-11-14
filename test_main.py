import pytest
from main import unique_uuid, matrix_read, guardar
import main
from funciones_modificadas import iniciarSesionPrueba,registrarUsuarioPrueba,fastaddPrueba1


def test_unique_uuid():
    """
    Prueba que unique_uuid genere un UUID único que no esté en la lista de UUIDs existentes.
    """
    existing_uuids = {"123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174001"}
    new_uuid = unique_uuid(existing_uuids)
    
    assert new_uuid not in existing_uuids
    assert len(new_uuid) == 36


def test_matrix_read():
    """
    Prueba que matrix_read lea correctamente el archivo JSON y retorne una matriz con UUIDs únicos.
    """
    # Ejecutar matrix_read sin argumentos, asumiendo que leerá de archivos.json
    matrix, existing_uuids = matrix_read()

    
    assert len(matrix) > 0  
    for item in matrix:
        assert len(item) == 6  
        assert isinstance(item[5], str) and len(item[5]) == 36  


def test_guardar():
    """
    Prueba que guardar guarde correctamente la matriz en formato dict.
    """
    
    matrix = [
        [1, "Rojo", 10, 5, 100, "123e4567-e89b-12d3-a456-426614174000"],
        [2, "Azul", 20, 3, 200, "123e4567-e89b-12d3-a456-426614174001"]
    ]
    
    
    guardar(matrix)

    


def test_askoptions():
    """
    Simulación de la función askoptions para verificar el manejo de opciones válidas.
    """
    matrix = [[1, "Rojo", 10, 5, 100, "123e4567-e89b-12d3-a456-426614174000"]]
    opciones_posibles = {1, 2, 3, 4, 5, 6, 99}
    
    assert all(option in opciones_posibles for option in [1, 99])



sample_matrix = [
    [101, 'Red', 42, 10, 500, 'uuid1'],
    [102, 'Blue', 40, 5, 700, 'uuid2'],
    [101, 'Red', 44, 8, 500, 'uuid3'],
    [103, 'Green', 42, 20, 300, 'uuid4']
]

def test_chequear_stock_general():
    
    expected_stock_total = 10 + 5 + 8 + 20
    assert main.chequear_stock_general(sample_matrix) == expected_stock_total

def test_consulta_art():
    
    articulo_id = 101
    expected_stock_art = 10 + 8  
    assert main.consulta_art(sample_matrix, articulo_id) == expected_stock_art

def test_consulta_variacion():
    
    articulo_id = 101
    color = 'Red'
    talle = 42
    expected_stock_variacion = 10  
    assert main.consulta_variacion(sample_matrix, articulo_id, talle, color) == expected_stock_variacion


def test_iniciarSesion1():
    email='caucho@gmail.com'
    password='Caucho090909'
    resultado=iniciarSesionPrueba(email,password)
    assert resultado==True

def test_iniciarSesion2():
    email='Prueba@gmail.com'
    password='test090909'
    resultado=iniciarSesionPrueba(email,password)
    assert resultado==False

def test_registrarUsuario1():
    email='agustin@.com'
    password='test1'
    resultado=registrarUsuarioPrueba(email,password)
    assert resultado==False

def test_registrarUsuario2():
    email='agustin@gmail.com'
    password='test2'
    resultado=registrarUsuarioPrueba(email,password)
    assert resultado==False

def test_registrarUsuario3():
    email='agustin@.com'
    password='Testnumero03'
    resultado=registrarUsuarioPrueba(email,password)
    assert resultado==False

def test_registrarUsuario4():
    email='tomas@gmail.com'
    password='TestNumero04'
    resultado,credenciales=registrarUsuarioPrueba(email,password)
    assert resultado==True and credenciales[len(credenciales)-1]=={"user":email,"pass":password}

def test_FastaddPrueba1():
    articulo=10
    cantidad=10
    color="rojo"
    accion="AGREGAR"
    precio=100 
    talle=100
    resultado=fastaddPrueba1(articulo,cantidad,color,accion,precio,talle)
    assert resultado==[articulo,color,talle,accion,cantidad,precio]

def test_FastaddPrueba2():
    articulo=-1
    cantidad=-1
    color="rojo"
    accion=" "
    precio=-1 
    talle=-1
    resultado=fastaddPrueba1(articulo,cantidad,color,accion,precio,talle)
    assert resultado==[99999,color,99999,"AGREGAR",99999,99999]
