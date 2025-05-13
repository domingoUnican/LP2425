from dataclasses import dataclass, field
from typing import List
from enum import Enum
from collections import defaultdict


class TokenType(Enum):
    """
    Enumeración que define todos los tipos de tokens posibles en el lenguaje Lox.
    
    Incluye:
    - Símbolos individuales (paréntesis, operadores, etc.)
    - Palabras reservadas (keywords)
    - Literales (números, strings, identificadores)
    - Estados especiales (comentarios, tokens incompletos)
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
    THalfFloat = "_Unfinised Float"
    TFloat = "_Float"  
    TString = '"text"'
    TNumber = "_Number"  # or '123.45'
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

class TypesLiteral(Enum):
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


# Esto es por si queremos quitar TokenType.TAnd a todos los tokens    
# globals().update(TokenType.__members__)
# Esto es por si queremos quitar TypesLiteral a todos los tokens    
# globals().update(TypesLiteral.__members__)

    
@dataclass
class Token:
    """
    Clase que representa una unidad léxica (token) identificada durante el análisis del código fuente.
    
    Atributos:
    - lineno: Número de línea donde se encontró el token
    - value: Valor literal del token (el texto exacto que se encontró)
    - tipo: Tipo del token (según la enumeración TokenType)
    
    El método __post_init__ se ejecuta automáticamente después de la inicialización
    y se encarga de ajustar el tipo del token según su valor.
    """
    lineno: int = 0 # Línea de código donde se encuentra el token
    value: str = "" # Valor del token
    tipo: TokenType = TokenType.TNothing # Tipo del token (por defecto TNothing)

    def __post_init__(self):
        """
        Método que se ejecuta después de la inicialización del objeto Token.
        Se encarga de asignar el valor del token a su tipo correspondiente
        (número, cadena, etc.).
        Si el valor del token coincide con un tipo de token específico, 
        se asingará el tipo correspondiente.
        Si el valor no coincide con ningún tipo, se mantendrá como TNothing.
        """
        
        try:
            if self.tipo == TokenType.TFloat: # Aquí se gestiona que no haya distinción entre float y number
                self.tipo = TokenType.TNumber
            else:
                self.tipo = TokenType(self.value)
        except:
            pass
       


# Definición del autómata finito determinista (DFA) para el análisis léxico en el lenguaje Lox.
dfa = defaultdict(lambda:None)
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.TNumber

dfa[(TokenType.TNothing, TypesLiteral.TySlash)] = TokenType.TSlash
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

dfa[TokenType.TNothing, TypesLiteral.TyLeftParen] = TokenType.TLeftParen

dfa[TokenType.TNothing, TypesLiteral.TyRightParen] = TokenType.TRightParen

dfa[TokenType.TNothing, TypesLiteral.TyLeftBrace] = TokenType.TLeftBrace

dfa[TokenType.TNothing, TypesLiteral.TyRightBrace] = TokenType.TRightBrace

dfa[TokenType.TNothing, TypesLiteral.TyComma] = TokenType.TComma

dfa[TokenType.TNothing, TypesLiteral.TyDot] = TokenType.TDot

dfa[TokenType.TNothing, TypesLiteral.TyMinus] = TokenType.TMinus

dfa[TokenType.TNothing, TypesLiteral.TyPlus] = TokenType.TPlus

dfa[TokenType.TNothing, TypesLiteral.TySemiColon] = TokenType.TSemiColon

dfa[TokenType.TNothing, TypesLiteral.TyStar] = TokenType.TStar

dfa[TokenType.TNothing, TypesLiteral.TyBang] = TokenType.TBang
dfa[TokenType.TBang, TypesLiteral.TyEqual] = TokenType.TBangEqual

dfa[TokenType.TNothing, TypesLiteral.TyEqual] = TokenType.TEqual
dfa[TokenType.TEqual, TypesLiteral.TyEqual] = TokenType.TEqualEqual

dfa[TokenType.TNothing, TypesLiteral.TySpace] = TokenType.TSpace
dfa[TokenType.TSpace, TypesLiteral.TySpace] = TokenType.TSpace
dfa[TokenType.TSpace, TypesLiteral.TyChar] = None

dfa[TokenType.TNothing, TypesLiteral.TyChar] = TokenType.TIdentifier
dfa[TokenType.TIdentifier, TypesLiteral.TyChar] = TokenType.TIdentifier
dfa[TokenType.TIdentifier, TypesLiteral.TyNumber] = TokenType.TIdentifier
dfa[TokenType.TIdentifier, TypesLiteral.TySpace] = None

dfa[TokenType.TNothing, TypesLiteral.TyLess] = TokenType.TLess
dfa[TokenType.TLess, TypesLiteral.TyEqual] = TokenType.TLessEqual

dfa[TokenType.TNothing, TypesLiteral.TyGreater] = TokenType.TGreater
dfa[TokenType.TGreater, TypesLiteral.TyEqual] = TokenType.TGreaterEqual

dfa[TokenType.TNothing, TypesLiteral.TyLine] = TokenType.TLine

dfa[TokenType.TNothing, TypesLiteral.TyQuote] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyNumber] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyChar] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TySpace] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyLeftParen] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyRightParen] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyLeftBrace] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyRightBrace] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyComma] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyDot] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyMinus] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyPlus] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TySemiColon] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyStar] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TySlash] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyBang] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyEqual] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyLess] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyGreater] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyLine] = TokenType.THalfString
dfa[TokenType.THalfString, TypesLiteral.TyQuote] = TokenType.TString

dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.THalfFloat
dfa[(TokenType.THalfFloat, TypesLiteral.TyNumber)] = TokenType.TFloat
dfa[(TokenType.TFloat, TypesLiteral.TyNumber)] = TokenType.TFloat





def is_final_state(state):
    """
    Determina si un estado del DFA es un estado final (aceptación).
    
    Parámetros:
    - state: Estado actual del DFA (TokenType)
    
    Retorna:
    - True si es un estado final (token completo), False si es intermedio o inicial
    """
    return (state not in [TokenType.THalfString, TokenType.TNothing])
        

def tokenize(entrada, ignore_tokens=None):
    """
    Función principal que convierte una cadena de entrada en una secuencia de tokens.
    
    Parámetros:
    - entrada: Cadena de texto a tokenizar
    - ignore_tokens: Lista de tipos de tokens a ignorar (no incluir en la salida)
    
    Retorna:
    - Generador que produce objetos Token uno por uno
    
    Funcionamiento:
    1. Inicializa el estado y posición
    2. Para cada carácter:
       a. Determina su tipo (TypesLiteral)
       b. Consulta el DFA para la transición
       c. Actualiza estado y posición
    3. Cuando no hay transición válida, emite el token (si no está en ignore_tokens)
    4. Reinicia el proceso con el resto de la cadena
    """
    if ignore_tokens is None:
        ignore_tokens = []
    
    line = 1
    pos = 0
    pos_final = 0
    state = TokenType.TNothing
    while pos < len(entrada):
        ch = entrada[pos]
        if ch == '\n':
            type_literal = TypesLiteral.TyLine
        elif ch.isspace():
            type_literal = TypesLiteral.TySpace
        elif ch == '/':
            type_literal = TypesLiteral.TySlash
        elif ch == '"':
            type_literal = TypesLiteral.TyQuote
        elif ch.isdigit():
            type_literal = TypesLiteral.TyNumber
        elif ch.isalpha():
            type_literal = TypesLiteral.TyChar
        elif ch == '(':
            type_literal = TypesLiteral.TyLeftParen
        elif ch == ')':
            type_literal = TypesLiteral.TyRightParen
        elif ch == '{':
            type_literal = TypesLiteral.TyLeftBrace
        elif ch == '}':
            type_literal = TypesLiteral.TyRightBrace
        elif ch == ',':
            type_literal = TypesLiteral.TyComma
        elif ch == '.':
            type_literal = TypesLiteral.TyDot
        elif ch == '-':
            type_literal = TypesLiteral.TyMinus
        elif ch == '+':
            type_literal = TypesLiteral.TyPlus
        elif ch == ';':
            type_literal = TypesLiteral.TySemiColon
        elif ch == '*':
            type_literal = TypesLiteral.TyStar
        elif ch == '!':
            type_literal = TypesLiteral.TyBang
        elif ch == '=':
            type_literal = TypesLiteral.TyEqual
        elif ch == '<':
            type_literal = TypesLiteral.TyLess
        elif ch == '>':
            type_literal = TypesLiteral.TyGreater
        else:
            type_literal = TypesLiteral.TyNothing
        next_state = dfa[(state, type_literal)]
        if next_state:
            state = next_state
            pos_final = pos + 1 if is_final_state(state) else pos_final
            pos = pos + 1
        else:
            if state not in ignore_tokens:
                yield Token(line, entrada[:pos_final], state)
            pos = 0
            entrada = entrada[pos_final:]
            if type_literal == TypesLiteral.TyLine:
                line += 1
                pos += 1
            state = TokenType.TNothing
    if state != TokenType.TNothing and state not in ignore_tokens:
        yield Token(line, entrada, state)





# EJEMPLO DE USO:
ignore_tokens = [TokenType.TComment, TokenType.TCommentLine, TokenType.TSpace, TokenType.THalfFloat]

prueba1 = "a = 1\n a"
prueba2 = "a"
prueba3 = '"esto es un string" b'
prueba4 = "or and "
prueba5 = "a = 1.0\n a"

# print("Salida de prueba 1")
# for i in tokenize(prueba1, ignore_tokens):
#     print("El token es ", i)

# print("\nSalida de prueba 2")
# for i in tokenize(prueba2, ignore_tokens):
#     print("El token es ", i)

# print("\nSalida de prueba 3")
# for i in tokenize(prueba3, ignore_tokens):
#     print("El token es ", i)

# print("\nSalida de prueba 4")
# for i in tokenize(prueba4, ignore_tokens):
#     print("El token es ", i)

# print("\nSalida de prueba 5")
# for i in tokenize(prueba5, ignore_tokens):
#     print("El token es ", i)




# salida de prueba 1

"""
[Token(lineno=1, value='a', tipo=TokenType.TIdentifier),
Token(lineno=1, value=' ', tipo=TokenType.TSpace),
Token(lineno=1, value='=', tipo=TokenType.TEqual),
Token(lineno=1, value=' ', tipo=TokenType.TSpace),
Token(lineno=1, value='1', tipo=TokenType.TNumber),
Token(lineno=2, value='\n ', tipo=TokenType.TSpace),
Token(lineno=2, value='a', tipo=TokenType.TIdentifier)]
"""

# salida de prueba 2

"""
[Token(lineno=1, value='a', tipo=TokenType.TIdentifier)]
"""


# salida de prueba 3

"""
[Token(lineno=1, value='"esto es un string"', tipo=TokenType.TString),
Token(lineno=1, value=' ', tipo=TokenType.TSpace),
Token(lineno=1, value='b', tipo=TokenType.TIdentifier)]
"""

# salida de prueba 4

"""
[Token(lineno=1, value='or', tipo=TokenType.TOr),
Token(lineno=1, value=' ', tipo=TokenType.TSpace),
Token(lineno=1, value='and', tipo=TokenType.TAnd),
Token(lineno=1, value=' ', tipo=TokenType.TSpace)]
"""
