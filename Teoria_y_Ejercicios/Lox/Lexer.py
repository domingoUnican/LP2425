from dataclasses import dataclass, field
from typing import List
from enum import Enum
from collections import defaultdict


class TokenType(Enum):
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

""" 
La clase Token representa una unidad léxica del código, identificada por el analizador léxico. 

Contiene tres atributos: 
    'lineno' indica la línea donde aparece el token, 
    'value' almacena el valor literal extraído del texto
    'tipo' representa el tipo de token, clasificado mediante la enumeración TokenType. 
    
El método especial __post_init__ se ejecuta automáticamente después de la creación del objeto y trata de 
convertir el 'value' en un TokenType, lo cual es útil para reconocer palabras clave directamente por su valor, 
incluso si fueron inicialmente clasificadas de manera más general (como identificadores). 
"""

@dataclass
class Token:
    lineno: int = 0
    value: str = ""
    tipo: TokenType = TokenType.TNothing

    def __post_init__(self):
        try:
            self.tipo = TokenType(self.value)
        except:
            pass
       

dfa = defaultdict(lambda:None)

# TNumber
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.TNumber # coma flotante
 
# TSlash
dfa[(TokenType.TNothing, TypesLiteral.TySlash)] = TokenType.TSlash

dfa[(TokenType.TSlash, TypesLiteral.TySlash)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyChar)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TySpace)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyLeftParen)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyRightParen)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyLeftBrace)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyRightBrace)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyComma)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyDot)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyPlus)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TySemiColon)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyStar)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TySlash)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyBang)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyEqual)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyLess)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyGreater)] = TokenType.TComment
dfa[(TokenType.TSlash, TypesLiteral.TyQuote)] = TokenType.TComment
# TCommentEnd
dfa[(TokenType.TSlash, TypesLiteral.TyLine)] = TokenType.TCommentLine


dfa[(TokenType.TNothing, TypesLiteral.TyLeftParen)] = TokenType.TLeftParen

dfa[(TokenType.TNothing, TypesLiteral.TyRightParen)] = TokenType.TRightParen

dfa[(TokenType.TNothing, TypesLiteral.TyLeftBrace)] = TokenType.TLeftBrace

dfa[(TokenType.TNothing, TypesLiteral.TyComma)] = TokenType.TComma

dfa[(TokenType.TNothing, TypesLiteral.TyDot)] = TokenType.TDot

dfa[(TokenType.TNothing, TypesLiteral.TyMinus)] = TokenType.TMinus

dfa[(TokenType.TNothing, TypesLiteral.TyPlus)] = TokenType.TPlus

dfa[(TokenType.TNothing, TypesLiteral.TySemiColon)] = TokenType.TSemiColon

dfa[(TokenType.TNothing, TypesLiteral.TyStar)] = TokenType.TStar

dfa[(TokenType.TNothing, TypesLiteral.TyBang)] = TokenType.TBang
dfa[(TokenType.TBang, TypesLiteral.TyEqual)] = TokenType.TBangEqual

dfa[(TokenType.TNothing, TypesLiteral.TyEqual)] = TokenType.TEqual
dfa[(TokenType.TEqual, TypesLiteral.TyEqual)] = TokenType.TEqualEqual

dfa[(TokenType.TNothing, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TSpace, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TSpace, TypesLiteral.TyChar)] = None

dfa[(TokenType.TNothing, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TIdentifier, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TIdentifier, TypesLiteral.TyNumber)] = TokenType.TIdentifier
dfa[(TokenType.TIdentifier, TypesLiteral.TySpace)] = None

dfa[(TokenType.TNothing, TypesLiteral.TyLess)] = TokenType.TLess
dfa[(TokenType.TLess, TypesLiteral.TyEqual)] = TokenType.TLessEqual

dfa[(TokenType.TNothing, TypesLiteral.TyGreater)] = TokenType.TGreater
dfa[(TokenType.TGreater, TypesLiteral.TyEqual)] = TokenType.TGreaterEqual

dfa[(TokenType.TNothing, TypesLiteral.TyLine)] = TokenType.TLine

dfa[(TokenType.TNothing, TypesLiteral.TyQuote)] = TokenType.THalfString
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


def is_final_state(state):
    return (state not in [TokenType.THalfString, TokenType.TNothing])
        

def tokenize(entrada):
    line = 1
    pos = 0
    pos_final = 0
    state = TokenType.TNothing
    tokens_ignorados = [TokenType.TSpace, TokenType.TLine, TokenType.TComment, TokenType.TCommentLine]
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
            token = Token(line, entrada[:pos_final], state)
            if token.tipo not in tokens_ignorados:
                yield token
            entrada = entrada[pos_final:]
            pos = 0
            if type_literal == TypesLiteral.TyLine:
                line += 1
            state = TokenType.TNothing
    if state != TokenType.TNothing:
        token = Token(line, entrada, state)
        if token.tipo not in tokens_ignorados:
            yield token
# prueba1 = "a = 1\n a"
# prueba2 = "a"
# prueba3 = '"esto es un string" b'
# prueba4 = "or and "

# for i in tokenize(prueba1):
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
