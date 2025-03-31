def siguiente(lista):
    return lista[0]
def mover(lista):
    lista = lista[1:]
    return lista[0]


def siguiente_token(lista, caracter):
    if siguiente(lista) == caracter:
        mover(lista)
        return True
    else:
        return False
            

def actual(lista):
    pass

def producto(lista):
    valor = actual(lista)
    if siguiente_token(lista, '*'):
        valor = valor* producto(lista)
    return valor
    
def expresion(lista):
    valor = producto(lista)
    valor = actual(lista)
    if siguiente_token(lista, '+'):
        valor =  valor + expresion(lista)

    return valor
