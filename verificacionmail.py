def verificarArroba(correo):
    x = correo.find('@')  # find busca la primera aparicion de la cadena de texto en el string
    y = correo.rfind('@') # rfind busca la ultima aparicion de la cadena de texto en el string
    if '@' in correo and x == y:
        return True
    else:
        return False

def verificarAlfanum(correo):
    posicion = correo.find('@')   
    aux = correo[:posicion]  # Evalua todo el correo hasta la arroba, sin incluirla
    if aux.isalnum():  # Verifica que todos los caracteres sean numeros o letras
        return True
    else:
        return False

def verificarFinal(correo):
    aux = correo[len(correo)-7:]  # Verifica solo los ultimos 7, que serian .com.ar
    if aux == '.com.ar':          # Si no es .com.ar, daria error
        return True
    else:
        return False

def verificarDominio(correo):
    aux = correo.rstrip('.com.ar')  # Saca el .com.ar para poder verificar que entre el @ y el .com.ar 
    posicion = correo.find('@')     # haya algo, que no sea vacio
    dominio = aux[posicion+1:]
    if len(dominio) > 0:
        return True
    else:
        return False

def obtenerDominio(correo):
    pos = correo.find('@')
    dominio_ = correo[pos+1:len(correo)-7]  # Devuelve el str de lo que hay entre @ y .com.ar
    return dominio_

correo = input('Ingrese correo electronico  ')
listaDominios = []
while len(correo) > 0:
    valido = True
    while valido:
        arroba = verificarArroba(correo)
        if not arroba:
            valido = False
            break
        alfanumerico = verificarAlfanum(correo)
        if not alfanumerico:
            valido = False
            break
        final = verificarFinal(correo)
        if not final:
            valido = False
            break
        dominio = verificarDominio(correo)
        if not dominio:
            valido = False
            break
        break
    if valido:
        print('valido')
        break
    if not valido:
        print('Correo no valido')
        correo = input('Ingrese otro correo electronico  ')