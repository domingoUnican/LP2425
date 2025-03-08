from dataclasses import dataclass, field
from typing import List
from enum import Enum
from collections import defaultdict

# --------------------------------- TOKENS ---------------------------------------------


class TokenType(Enum):
    """
    Enumeración que contiene los distintos tipos de tokens que el lexer puede reconocer.
    Para crear un nuevo tipo de token hay que ponerlo aqui.
    """

    # One character literals
    TComment = "//"
    TCommentLine = "/*"
    TLeftParen = "("
    TRightParen = ")"
    TLeftBrace = "{"
    TRightBrace = "}"
    TComma = ","
    TDot = "."
    TMinus = "-"
    TPlus = "+"
    TSemiColon = ";"
    TStar = "*"
    TSlash = "/"
    TBang = "!"
    TEqual = "="
    TLess = "<"
    TGreater = ">"
    TLine = "\n"
    TSpace = " "

    # Two character literals
    TBangEqual = "!="
    TEqualEqual = "=="
    TLessEqual = "<="
    TGreaterEqual = ">="

    # Literals
    THalfString = "_Unfinised String"
    TUnfinishedFloat = "_UnfinishedFloat"
    TString = '"text"'
    TNumber = "_Number"
    TFloat = "_Float"
    TIdentifier = "_Identificador"

    # Keywords
    TAnd = "and"
    TClass = "class"
    TElse = "else"
    TFalse = "false"
    TFor = "for"
    TFun = "fun"
    TIf = "if"
    TNil = "nil"
    TOr = "or"
    TPrint = "print"
    TReturn = "return"
    TSuper = "super"
    TThis = "this"
    TNot = "not"
    TTrue = "true"
    TVar = "var"
    TWhile = "while"
    TNothing = None  # No token


# ---------------------------------------------------------------------------------------------

# ------------------------------------ LITERALES ----------------------------------------------


class TypesLiteral(Enum):
    """
    Enumeración que contiene los distintos tipos de literales que el lexer puede reconocer
    en el imput.
    Para crear un nuevo tipo de literal hay que ponerlo aqui.
    Si no esta aqui saldra error en el input.
    """

    TyNothing = None
    TyNumber = "number"
    TyChar = "char"
    TyLine = "\n"
    TySpace = " "
    TyLeftParen = "("
    TyRightParen = ")"
    TyLeftBrace = "{"
    TyRightBrace = "}"
    TyComma = ","
    TyDot = "."
    TyMinus = "-"
    TyPlus = "+"
    TySemiColon = ";"
    TyStar = "*"
    TySlash = "/"
    TyBang = "!"
    TyEqual = "="
    TyLess = "<"
    TyGreater = ">"

    # Two character literals
    TyQuote = '"'


# --------------------------------------------------------------------------------------------

# Esto es por si queremos quitar TokenType.TAnd a todos los tokens
# globals().update(TokenType.__members__)
# Esto es por si queremos quitar TypesLiteral a todos los tokens
# globals().update(TypesLiteral.__members__)

# ------------------------------------- CLASE TOKEN ------------------------------------------


@dataclass
class Token:
    """
    Clase que representa un token en el proceso de análisis léxico.

    Esta clase almacena la información de un token, incluyendo
    su tipo, su valor y la línea en la que aparece.
    """

    lineno: int = (
        0  # Número de línea en la que se encuentra el token dentro del código introducido.
    )
    value: str = (
        ""  # Valor del token, por ejemplo, una palabra clave ('if'), un número ('123'), un símbolo ('(').
    )
    tipo: TokenType = (
        TokenType.TNothing
    )  # Tipo de token según la enumeración TokenType.

    def __post_init__(self):
        """
        Método especial que se ejecuta automáticamente después de la inicialización de la instancia.

        Intenta asignar el tipo de token basándose en su valor. Si el valor del token coincide con
        una entrada en la enumeración TokenType, se asigna el tipo correspondiente. Si no coincide,
        se mantiene el tipo predeterminado TokenType.TNothing.
        """
        try:
            # como no queremos distincion en float y number, lo pasamos a number
            if self.tipo == TokenType.TFloat:
                self.tipo = TokenType.TNumber
            else:
                self.tipo = TokenType(
                    self.value
                )  # Se intenta convertir el valor en un tipo de token definido en TokenType.
        except:
            pass  # Si el valor no corresponde a ningún tipo de token en TokenType, no se modifica el tipo del token.


# --------------------------------------------------------------------------------------------

# ---------------------------------DFA como diccionario --------------------------------------

# Definimos un diccionario llamado 'dfa' que representa el autómata finito determinista (DFA)
# usado para el proceso de tokenización.
#
# El DFA mapea un estado actual (TokenType) y un tipo de carácter (TypesLiteral)
# a un nuevo estado. Si no hay una transición definida, se devuelve 'None' como valor predeterminado.
dfa = defaultdict(lambda: None)

# ahora hay que rellenar todas las transiciones posibles en el autómata.

# Transiciones desde TNothing
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNothing, TypesLiteral.TySlash)] = TokenType.TSlash
dfa[(TokenType.TNothing, TypesLiteral.TyLeftParen)] = TokenType.TLeftParen
dfa[(TokenType.TNothing, TypesLiteral.TyRightParen)] = TokenType.TRightParen
dfa[(TokenType.TNothing, TypesLiteral.TyLeftBrace)] = TokenType.TLeftBrace
dfa[(TokenType.TNothing, TypesLiteral.TyRightBrace)] = TokenType.TRightBrace
dfa[(TokenType.TNothing, TypesLiteral.TyComma)] = TokenType.TComma
dfa[(TokenType.TNothing, TypesLiteral.TyDot)] = TokenType.TDot
dfa[(TokenType.TNothing, TypesLiteral.TyMinus)] = TokenType.TMinus
dfa[(TokenType.TNothing, TypesLiteral.TyPlus)] = TokenType.TPlus
dfa[(TokenType.TNothing, TypesLiteral.TySemiColon)] = TokenType.TSemiColon
dfa[(TokenType.TNothing, TypesLiteral.TyStar)] = TokenType.TStar
dfa[(TokenType.TNothing, TypesLiteral.TyBang)] = TokenType.TBang
dfa[(TokenType.TNothing, TypesLiteral.TyEqual)] = TokenType.TEqual
dfa[(TokenType.TNothing, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TNothing, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TNothing, TypesLiteral.TyLess)] = TokenType.TLess
dfa[(TokenType.TNothing, TypesLiteral.TyGreater)] = TokenType.TGreater
dfa[(TokenType.TNothing, TypesLiteral.TyLine)] = TokenType.TLine
dfa[(TokenType.TNothing, TypesLiteral.TyQuote)] = TokenType.THalfString

# Transiciones dentro del mismo estado
dfa[(TokenType.TNumber, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.TNumber
dfa[(TokenType.TSpace, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TIdentifier, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TIdentifier, TypesLiteral.TyNumber)] = TokenType.TIdentifier

# Dos caracteres seguidos que generan nuevos tokens
dfa[(TokenType.TBang, TypesLiteral.TyEqual)] = TokenType.TBangEqual
dfa[(TokenType.TEqual, TypesLiteral.TyEqual)] = TokenType.TEqualEqual
dfa[(TokenType.TLess, TypesLiteral.TyEqual)] = TokenType.TLessEqual
dfa[(TokenType.TGreater, TypesLiteral.TyEqual)] = TokenType.TGreaterEqual

# Cadenas de texto
dfa[(TokenType.THalfString, TypesLiteral.TyNumber)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyChar)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TySpace)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyLeftParen)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyRightParen)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyLeftBrace)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyRightBrace)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyComma)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyDot)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyMinus)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyPlus)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TySemiColon)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyStar)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TySlash)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyBang)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyEqual)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyLess)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyGreater)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyLine)] = TokenType.THalfString
dfa[(TokenType.THalfString, TypesLiteral.TyQuote)] = TokenType.TString

# Comentarios
dfa[(TokenType.TSlash, TypesLiteral.TySlash)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyChar)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TySpace)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyLeftParen)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyRightParen)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyLeftBrace)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyRightBrace)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyComma)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyDot)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyMinus)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyPlus)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TySemiColon)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyStar)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TySlash)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyBang)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyEqual)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyLess)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyGreater)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyQuote)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyLine)] = TokenType.TCommentLine

# para los flotantes
dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.TUnfinishedFloat
dfa[(TokenType.TUnfinishedFloat, TypesLiteral.TyNumber)] = TokenType.TFloat
dfa[(TokenType.TFloat, TypesLiteral.TyNumber)] = TokenType.TFloat


# Estados finales para acabar el token
dfa[(TokenType.TIdentifier, TypesLiteral.TySpace)] = None
dfa[(TokenType.TSpace, TypesLiteral.TyChar)] = None

# flotantes (o se queda con el numero entero o lee un punto y se queda con el decimal tambien)

# -----------------------------------------------------------------------------------------

# --------------------------------- FUNCIONES ---------------------------------------------

# set para mejorar el tiempo de busqueda

# Los estados no finales son los incompletos. Si se encuentra uno de estos, se debe seguir buscando
# para completar el token.
estados_no_finales: set = {TokenType.THalfString, TokenType.TNothing}

# Los estados ignorados son los que no se deben tener en cuenta para la salida final.
# Por ejemplo, los comentarios y los espacios no son tokens válidos.
estados_ignorados: set = {TokenType.TComment, TokenType.TCommentLine, TokenType.TSpace, TokenType.TUnfinishedFloat}


def is_final_state(state):
    """
    Función que verifica si un estado es final.

    Un estado final significa que se ha reconocido un token válido y se puede emitir.

    Parámetros:
    - state (TokenType): Estado actual del DFA.

    Retorna:
    - bool: True si el estado es final, False en caso contrario.
    """
    return state not in estados_no_finales


def tokenize(entrada: str):
    """
    Función que tokeniza una cadena de entrada, dividiéndola en una lista de tokens.

    Parámetros:
    - entrada (str): Código fuente a analizar.

    Retorna:
    - Generador de objetos Token con la información de cada token identificado. Es decir,
      retorna y sigue con la ejecucion para el siguiente elemento.
    """

    line = 1  # Número de línea actual
    pos = 0  # Posición actual en la cadena de entrada
    pos_final = 0  # Última posición válida de un token reconocido
    state = TokenType.TNothing  # Estado inicial del DFA

    while pos < len(entrada):  # Recorremos la entrada carácter por carácter
        ch = entrada[pos]  # Obtenemos el carácter actual

        # Determinar el tipo de carácter según TypesLiteral
        # si se quiere anhadir otro literal tambien hay que anhadirlo aqui
        if ch == "\n":
            type_literal = TypesLiteral.TyLine
        elif ch.isspace():
            type_literal = TypesLiteral.TySpace
        elif ch == "/":
            type_literal = TypesLiteral.TySlash
        elif ch == '"':
            type_literal = TypesLiteral.TyQuote
        elif ch.isdigit():
            type_literal = TypesLiteral.TyNumber
        elif ch.isalpha():
            type_literal = TypesLiteral.TyChar
        elif ch == "(":
            type_literal = TypesLiteral.TyLeftParen
        elif ch == ")":
            type_literal = TypesLiteral.TyRightParen
        elif ch == "{":
            type_literal = TypesLiteral.TyLeftBrace
        elif ch == "}":
            type_literal = TypesLiteral.TyRightBrace
        elif ch == ",":
            type_literal = TypesLiteral.TyComma
        elif ch == ".":
            type_literal = TypesLiteral.TyDot
        elif ch == "-":
            type_literal = TypesLiteral.TyMinus
        elif ch == "+":
            type_literal = TypesLiteral.TyPlus
        elif ch == ";":
            type_literal = TypesLiteral.TySemiColon
        elif ch == "*":
            type_literal = TypesLiteral.TyStar
        elif ch == "!":
            type_literal = TypesLiteral.TyBang
        elif ch == "=":
            type_literal = TypesLiteral.TyEqual
        elif ch == "<":
            type_literal = TypesLiteral.TyLess
        elif ch == ">":
            type_literal = TypesLiteral.TyGreater
        else:
            type_literal = (
                TypesLiteral.TyNothing
            )  # Si el carácter no coincide con ninguno, se marca como 'none'

        # una vez detectado el tipo usamos el diccionario:
        # Obtener el próximo estado del DFA basado en el estado actual y el tipo de carácter
        next_state = dfa[(state, type_literal)]

        # Si existe una transición válida en el DFA
        if next_state:
            state = next_state  # Actualizamos el estado actual
            pos_final = (
                pos + 1 if is_final_state(state) else pos_final
            )  # Actualizamos la última posición válida
            pos += 1  # Avanzamos al siguiente carácter

        # Si no hay transición válida, generamos un token con el valor encontrado hasta ahora
        # siempre que no sea un ignorado
        else:
            if state not in estados_ignorados:
                yield Token(line, entrada[:pos_final], state)  # Se emite el token

            # Reiniciamos la posición y ajustamos la entrada eliminando lo procesado
            pos = 0
            entrada = entrada[pos_final:]

            # especial:
            # Si encontramos un salto de línea, incrementamos el contador de líneas
            if type_literal == TypesLiteral.TyLine:
                line += 1
                pos += 1  # Avanzamos al siguiente carácter después del salto de línea

            state = (
                TokenType.TNothing
            )  # Reiniciamos el estado para empezar a procesar un nuevo token

    # Si al finalizar el bucle aún estamos en un estado válido, generamos un último token con lo que queda
    if state != TokenType.TNothing:
        yield Token(line, entrada, state)


# ------------------------------------------------------------------------------------------

# ---------------------------------------- PRUEBAS -----------------------------------------

# Definición de los colores como constantes
COLOR_TITULO = "\033[1;34m"  # Azul para el título
COLOR_TOKEN = "\033[1;32m"  # Verde para los tokens
COLOR_SALIDA = "\033[1;37m"  # Blanco para la salida esperada
COLOR_SALIDA_TITULO = "\033[1;33m"  # Amarillo para la salida esperada
COLOR_RESET = "\033[0m"  # Restablecer el color

# Definición de las pruebas de ejemplo
prueba1 = "a = 1\n a"
prueba2 = "a"
prueba3 = '"esto es un string" b'
prueba4 = "or and "
prueba5 = 'if x > 10 and y < 5: print("Hola")'

# Salidas esperadas para cada prueba

# Salida esperada para prueba 1
prueba1_solucion = """
[Token(lineno=1, value='a', tipo=TokenType.TIdentifier),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='=', tipo=TokenType.TEqual),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='1', tipo=TokenType.TNumber),
 Token(lineno=2, value='\n ', tipo=TokenType.TSpace),
 Token(lineno=2, value='a', tipo=TokenType.TIdentifier)]
"""

# Salida esperada para prueba 2
prueba2_solucion = """
[Token(lineno=1, value='a', tipo=TokenType.TIdentifier)]
"""

# Salida esperada para prueba 3
prueba3_solucion = """
[Token(lineno=1, value='"esto es un string"', tipo=TokenType.TString),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='b', tipo=TokenType.TIdentifier)]
"""

# Salida esperada para prueba 4
prueba4_solucion = """
[Token(lineno=1, value='or', tipo=TokenType.TOr),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='and', tipo=TokenType.TAnd),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace)]
"""

# Salida esperada para prueba 5 (más compleja)
prueba5_solucion = """
[Token(lineno=1, value='if', tipo=TokenType.TIf),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='x', tipo=TokenType.TIdentifier),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='>', tipo=TokenType.TGreaterThan),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='10', tipo=TokenType.TNumber),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='and', tipo=TokenType.TAnd),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='y', tipo=TokenType.TIdentifier),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='<', tipo=TokenType.TLessThan),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='5', tipo=TokenType.TNumber),
 Token(lineno=1, value=':', tipo=TokenType.TColon),
 Token(lineno=1, value=' ', tipo=TokenType.TSpace),
 Token(lineno=1, value='print', tipo=TokenType.TPrint),
 Token(lineno=1, value='(', tipo=TokenType.TParenthesisLeft),
 Token(lineno=1, value='"Hola"', tipo=TokenType.TString),
 Token(lineno=1, value=')', tipo=TokenType.TParenthesisRight)]
"""

# ---------------------------------------- EJECUCIÓN DE LAS PRUEBAS -----------------------------------------

# Función para ejecutar las pruebas y mostrar resultados


def ejecutar_prueba(prueba, solucion_esperada, num_prueba):
    print(
        f"{COLOR_TITULO}Prueba {num_prueba}:{COLOR_RESET}"
    )  # Título de la prueba en azul
    for i in tokenize(prueba):
        print(f"{COLOR_TOKEN}El token es {i}{COLOR_RESET}")  # Tokens en verde
    print(f"\n{COLOR_SALIDA_TITULO}Salida esperada:{COLOR_RESET}")
    print(
        f"{COLOR_SALIDA}{solucion_esperada}{COLOR_RESET}"
    )  # Salida esperada en blanco
    print("\n")


# Ejecutando las pruebas
# ejecutar_prueba(prueba1, prueba1_solucion, 1)
# ejecutar_prueba(prueba2, prueba2_solucion, 2)
# ejecutar_prueba(prueba3, prueba3_solucion, 3)
# ejecutar_prueba(prueba4, prueba4_solucion, 4)
# ejecutar_prueba(prueba5, prueba5_solucion, 5)

# mas pruebas para ver si funciona bien los casos dificiles
prueba6 = 'x = 2 "hola que tal'  # string cortado
prueba7 = "x = 2 \n y = 3"  # saltitos
prueba8 = "x = 123123"  # numeros enteros
prueba9 = "x = 1.23123"  # numeros decimales
prueba10 = "x = 12.31.23"  # numeros decimales error 1
prueba11 = "x = 12...31..23"  # numeros decimales error 2

ejecutar_prueba(prueba6, "", 6)
ejecutar_prueba(prueba7, "", 7)
ejecutar_prueba(prueba8, "", 8)
ejecutar_prueba(prueba9, "", 9)
ejecutar_prueba(prueba10, "", 10)
ejecutar_prueba(prueba11, "", 11)
