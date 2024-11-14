from main import cargar_usuarios,convint
def iniciarSesionPrueba(email,contraseña):
    credenciales = cargar_usuarios()
    
    for credencial in credenciales:
        if credencial['user'] == email and credencial['pass'] == contraseña:
            return True
    else:
        return False

def registrarUsuarioPrueba(email,contraseña):
    
    verificarArroba = lambda correo: correo.find('@') == correo.rfind('@') and '@' in correo
    verificarAlfanum = lambda correo: correo[:correo.find('@')].isalnum()
    verificarFinal = lambda correo: correo.endswith('.com')
    verificarDominio = lambda correo: len(correo[correo.find('@')+1:].rstrip('.com')) > 0

    validarMail = lambda correo: (verificarArroba(correo) and
                                verificarAlfanum(correo) and
                                verificarFinal(correo) and
                                verificarDominio(correo))

    # Contraseña

    verificarLetrasNumeros = lambda contra: contra.isalnum()
    verificarCantLetras = lambda contra: len(contra) >= 8
    verificarMayus = lambda contra: any(c.isupper() for c in contra)
    verificarLetras = lambda contra: any(c.isalpha() for c in contra)
    verificarNum = lambda contra: any(c.isdigit() for c in contra)

    validarContraseña = lambda contraseña: (verificarLetrasNumeros(contraseña) and
                                            verificarCantLetras(contraseña) and
                                            verificarMayus(contraseña) and
                                            verificarLetras(contraseña) and
                                            verificarNum(contraseña))
    

    credenciales = cargar_usuarios()
    
    if validarMail(email)==False or validarContraseña(contraseña)==False:
        return False
         
    credenciales.append({"user": email, "pass": contraseña})

    return True,credenciales

def fastaddPrueba1(articulo, cantidad, color, accion, precio, talle):
    linea = []

    # Agregar 'articulo' a la lista
    if articulo == -1:
        articulo_pre = 99999
        articulo = convint(articulo_pre)
    linea.append(articulo)

    # Agregar 'color' a la lista
    linea.append(color)

    # Agregar 'talle' a la lista
    if talle == -1:
        talle_pre = 99999
        talle = convint(talle_pre)
    linea.append(talle)

    # Asegurar 'accion' válida y agregar a la lista
    if accion not in ["AGREGAR", "ELIMINAR"]:
        accion = "AGREGAR"
    linea.append(accion)

    # Asegurar 'cantidad' válida y agregar a la lista
    if cantidad == -1:
        cantidad_pre = 99999
        cantidad = convint(cantidad_pre)
    linea.append(cantidad)

    # Asegurar 'precio' válido y agregar a la lista
    if precio == -1:
        precio_pre = 99999
        precio = convint(precio_pre)
    linea.append(precio)

    return linea

    