# coding: utf-8

from sly import Lexer
import os
import re
import sys


# class Comentario(Lexer):
#     _nivel_anidado = 0
#     tokens = {}

#     @_(r'\(\*')
#     def LINEA(self, t):
#         print("entra comentario")
#         self._nivel_anidado += 1

#     @_(r'\*\)')
#     def VOLVER(self, t):
#         print("vuelve de comentario")
#         # if self._nivel_anidado > 0: self._nivel_anidado -= 1
#         # if self._nivel_anidado == 0: self.begin(CoolLexer) #??? 
#         self._nivel_anidado -= 1
#         self.begin(CoolLexer)
    

#     @_(r'\n')
#     def LINEBREAK(self, t):
#         self.lineno += 1
    
#     @_(r'.')
#     def PASAR(self, t):
#         pass

class Comentario(Lexer):
    _nivel_anidado = 0
    tokens = {}

    @_(r'\(\*')
    def LINEA(self, t):
        self._nivel_anidado += 1

    @_(r'\*\)')
    def VOLVER(self, t):
        if self._nivel_anidado > 0: self._nivel_anidado -= 1
        if self._nivel_anidado == 0: self.begin(CoolLexer)
    
    @_(r'.')
    def PASAR(self, t):
        pass

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1

class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN}
    
    RESERVED_WORDS = ("IF", "FI", "THEN", "NOT", "IN", 
                      "CASE","ELSE", "ESAC", "CLASS", "INHERITS", 
                      "ISVOID","LET", "LOOP", "NEW", "OF", "POOL", 
                      "THEN", "WHILE")
    ignore = '\t '
    literals = ('.','+','-','*','/','<','=','(',')','~', ';', '{', '}', 
               ':', ',', '@', '~')
    ELSE = r'\b[eE][lL][sS][eE]\b'
    # STR_CONST = r'\"[^\"]*\"'

    #TODO: arith.cool esta bien pero no lo detecta
    #TODO: io.cool ESTA MAL, no deberia escribir nada porque es todo un comentario
    #TODO: integers2.cool no tiene sentido 0b es int 0 y objectid b y lo mismo con los valores 000001 no puede ser 1 tiene que ser 000001
    #TODO: new_complex.cool esta mal con los parentesis y los brackets???
    #TODO: arreglar comentarios
    #TODO: arreglar TAB \t en strings (es una feature y no un bug?)
    
    @_(r'\"[^\"]*\"')
    def STR_CONST(self, t):
        t.value = t.value.replace("\t", "\\t")
        return t
    
    @_(r'\(\*')
    def IR_BLOQUE(self, t):
        #Comentario._nivel_anidado += 1 #no hace falta porque al entrar en comentario tmb entra ahi en (*
        self.begin(Comentario)
    
    @_(r'--.*')
    def IR_LINEA(self, t):
        # if Comentario._nivel_anidado != 0: pass # deberia dar igual porque al estar dentro de comentario se come todo lo que no sea entrada a comentario de bloque o salida
        self.lineno += 1

    @_(r'\*\)')
    def ERROR_PARENTESIS(self, t):
        t.type = "ERROR \"Unmatched *)\""
        return t

    @_(r'[a-z][A-Z0-9_a-z]*\b')
    def OBJECTID(self, t):
        if t.value.upper() in self.RESERVED_WORDS:
            t.type = t.value.upper()
        if t.value.upper() in ["TRUE", "FALSE"]:
            t.type = "BOOL_CONST"
            t.value = t.value.upper() == "TRUE"
        return t
    
    @_(r'\d+')
    def INT_CONST(self, t):
        t.type = "INT_CONST"
        t.value = t.value
        #t.value = int(t.value)
        #integers2.cool
        return t

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1
    
    @_(r'\b[A-Z][A-Z0-9_a-z]*')
    def TYPEID(self, t):
        if t.value.upper() not in self.RESERVED_WORDS:
            t.type = "TYPEID"
        else:
            t.type = t.value.upper()
        return t

    @_(r'<-')
    def ASSIGN(self, t):
        t.value = "ASSIGN"
        return t
    
    @_(r'<=')
    def LE(self, t):
        t.value = "LE"
        return t
    
    @_(r'=>')
    def DARROW(self, t):
        t.value = "DARROW"
        return t
        
    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1

    @_(r'.')
    def ERROR(self, t):
        if t.value in self.literals:
            t.type = t.value
            return t
    
    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    def error(self, t):
        self.index += 1
        
    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\''
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        return list_strings
