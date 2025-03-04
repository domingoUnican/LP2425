from dataclasses import dataclass, field
from typing import List
from enum import Enum
from collections import defaultdict
##JAVIER LAMAS TABUENCA

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


##### RESPUESTA PREGUNTA 4 #####

#La clase Token se usa para representar los tokens que se generan al analizar el código. Cada token tiene tres atributos:
#lineno: El número de línea donde se encuentra el token.
#value: El texto del token.
#tipo: El tipo de token, definido en la enumeración TokenType.
#En el codigo de la clase queda reflejado con el DFA que token se devuelve para cada entrada en cada token actual (estado).

#El método __post_init__ se ejecuta automáticamente después de crear un token. 
# Intenta asignar el tipo de token basado en su valor. 
# Si el valor coincide con uno de los tipos en TokenType, se asigna ese tipo; si no, se deja como TokenType.TNothing.
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
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
# Rellenar el DFA
dfa[(TokenType.TNothing, TypesLiteral.TyNumber)] = TokenType.TNumber
dfa[(TokenType.TNothing, TypesLiteral.TyChar)] = TokenType.TIdentifier
dfa[(TokenType.TNothing, TypesLiteral.TyQuote)] = TokenType.THalfString
dfa[(TokenType.TNothing, TypesLiteral.TySpace)] = TokenType.TSpace
dfa[(TokenType.TNothing, TypesLiteral.TyLine)] = TokenType.TLine
dfa[TokenType.TSlash,TypesLiteral.TySlash] = TokenType.TComment
dfa[TokenType.TComment,TypesLiteral.TyLine] = TokenType.TCommentLine
dfa[TokenType.THalfString,TypesLiteral.TyChar] = TokenType.THalfString
dfa[TokenType.THalfString,TypesLiteral.TySpace] = TokenType.THalfString
dfa[TokenType.THalfString,TypesLiteral.TyQuote] = TokenType.TString
dfa[TokenType.THalfString,TypesLiteral.TyEqual] = TokenType.TEqual
dfa[(TokenType.THalfString, TypesLiteral.TySpace)] = TokenType.THalfString
dfa[TokenType.THalfString,TypesLiteral.TyLine] = TokenType.THalfString
dfa[TokenType.TNumber,TypesLiteral.TyNumber] = TokenType.TNumber
dfa[TokenType.TString,TypesLiteral.TyLine] = TokenType.TString
dfa[TokenType.TNumber,TypesLiteral.TyDot] = TokenType.TNumber
dfa[TokenType.TIdentifier,TypesLiteral.TyChar] = TokenType.TIdentifier
dfa[TokenType.TIdentifier,TypesLiteral.TyNumber] = TokenType.TIdentifier

def is_final_state(state):
    return (state not in [TokenType.THalfString, TokenType.TNothing])
        



def tokenize(entrada):
    line = 1
    pos = 0
    pos_final = 0
    state = TokenType.TNothing
    ignore_tokens = [TokenType.TSpace, TokenType.TComment, TokenType.TCommentLine]  # Ignorar estos tokens
    
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
            if token.tipo not in ignore_tokens:
                yield token
            pos = 0
            entrada = entrada[pos_final:]
            if type_literal == TypesLiteral.TyLine:
                line += 1
                pos += 1
            state = TokenType.TNothing
    
    if state != TokenType.TNothing:
        token = Token(line, entrada, state)
        if token.tipo not in ignore_tokens:
            yield token

# Test cases
prueba1 = "a = 1\n a"
prueba2 = "a"
prueba3 = '"esto es un string" b'
prueba4 = "or and "
prueba5 = '"prueba numero decimal "1.2'


for i in tokenize(prueba4):
    print("El token es ", i)




