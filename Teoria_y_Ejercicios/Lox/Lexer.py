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
    TDecimalNumber = "_DecimalNumber"
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
@dataclass sirve para que autogeneren las funciones __init__ y __repr__.
La clase Token sirve para retornar los Tokens en un único objeto.
El __post_init__ se ejecuta después de la inicialización y hace que las palabras resevadas (and, or...) 
se identifiquen con el tipo correcto y no TIdentifier.
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

        #para los decimales sean TNumber
        if self.tipo == TokenType.TDecimalNumber:
            self.tipo = TokenType.TNumber
    
    # cambiado para que el print sea igual al resultado 
    def __repr__(self):
        return f"Token(lineno={self.lineno}, value={self.value}, tipo={self.tipo})"



dfa = defaultdict(lambda:None)
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNothing, TypesLiteral.TyChar)] = TokenType.TIdentifier
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
dfa[(TokenType.TNothing, TypesLiteral.TySlash)] = TokenType.TSlash
dfa[(TokenType.TNothing, TypesLiteral.TyBang)] = TokenType.TBang
dfa[(TokenType.TNothing, TypesLiteral.TyEqual)] = TokenType.TEqual
dfa[(TokenType.TNothing, TypesLiteral.TyLess)] = TokenType.TLess
dfa[(TokenType.TNothing, TypesLiteral.TyGreater)] = TokenType.TGreater
dfa[(TokenType.TNothing, TypesLiteral.TyQuote)] = TokenType.THalfString
dfa[(TokenType.TNothing, TypesLiteral.TyLine)] = TokenType.TLine
dfa[(TokenType.TNothing, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TNumber, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNumber, TypesLiteral.TyDot)] = TokenType.TDecimalNumber
dfa[(TokenType.TDecimalNumber, TypesLiteral.TyNumber)] = TokenType.TDecimalNumber
dfa[(TokenType.TDot, TypesLiteral.TyNumber)] = TokenType.TDecimalNumber
dfa[(TokenType.TBang, TypesLiteral.TyEqual)] = TokenType.TBangEqual
dfa[(TokenType.TEqual, TypesLiteral.TyEqual)] = TokenType.TEqualEqual
dfa[(TokenType.TLess, TypesLiteral.TyEqual)] = TokenType.TLessEqual
dfa[(TokenType.TGreater, TypesLiteral.TyEqual)] = TokenType.TGreaterEqual
dfa[(TokenType.TSpace, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TIdentifier, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TIdentifier, TypesLiteral.TyNumber)] = TokenType.TIdentifier
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
dfa[(TokenType.THalfString, TypesLiteral.TyQuote)] = TokenType.TString
dfa[(TokenType.THalfString, TypesLiteral.TyLine)] = TokenType.THalfString
dfa[(TokenType.TSlash, TypesLiteral.TySlash)] = TokenType.TComment
dfa[(TokenType.TComment, TypesLiteral.TyLine)] = TokenType.TCommentLine
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
dfa[(TokenType.TIdentifier, TypesLiteral.TySpace)] = None
dfa[(TokenType.TSpace, TypesLiteral.TyChar)] = None

#TODO: arreglar el numero para que funcione bien con punto 3.4 valido 3.4.4 no valido, 3..4 no valido


def is_final_state(state):
    return (state not in [TokenType.THalfString, TokenType.TNothing])
        

def tokenize(entrada):
    line = 1
    pos = 0
    pos_final = 0
    state = TokenType.TNothing
    ignore_token_state = [TokenType.TSpace]
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
            if (state not in ignore_token_state):
                yield Token(line, entrada[:pos_final],state)
            pos = 0
            entrada = entrada[pos_final:]
            if type_literal == TypesLiteral.TyLine:
                line += 1
                pos += 1
            state = TokenType.TNothing
    if state != TokenType.TNothing:
        if (state not in ignore_token_state):
            yield Token(line, entrada, state)

# prueba1 = "a = 1\n a"
# prueba2 = "a"
# prueba3 = '"esto es un string..." b 3.14.15 3..15'
# prueba4 = "or and else"

# for i in tokenize(prueba4):
#     print("El token es", i)

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
