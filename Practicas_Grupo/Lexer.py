# coding: utf-8

from sly import Lexer
import os
import re
import sys


class Comentario(Lexer):
    _nivel_anidado = 0
    tokens = {}

    @_(r'\(\*')
    def LINEA(self, t):
        print("Detectado (* BBBBBBBBBBBBB")
        nivel_anidado += 1

    @_(r'\*\)')
    def VOLVER(self, t):
        print("Detectado *) AAAAAAAAAAAAAA")
        if self._nivel_anidado > 0: self._nivel_anidado -= 1
        if self._nivel_anidado == 0: self.begin(CoolLexer)
    
    @_(r'.')
    def PASAR(self, t):
        pass



class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN}
    
    RESERVED_WORDS = ("IF", "FI", "THEN", "NOT", "IN", 
                      "CASE","ELSE", "ESAC", "CLASS", "INHERITS", 
                      "ISVOID","LET", "LOOP", "NEW", "OF", "POOL", 
                      "THEN", "WHILE", "TRUE", "FALSE")
    ignore = '\t '
    literals = ('.')
    ELSE = r'\b[eE][lL][sS][eE]\b'
    STR_CONST = r'"[a-zA-Z0-9_/]*"'
    
    @_(r'\(\*')
    def IR_BLOQUE(self, t):
        print("Entrando a Comentario")
        Comentario._nivel_anidado += 1
        self.begin(Comentario)
    
    @_(r'--.*')
    def IR_LINEA(self, t):
        if Comentario._nivel_anidado != 0: pass
        print("PAPAPAPAPAPA")
        self.lineno += 1

    @_(r'\*\)')
    def ERROR_PARENTESIS(self, t):
        t.type = "ERROR \"Unmatched *)\""
        return t

    @_(r'\b[a-z][A-Z0-9_a-z]*\b')
    def OBJECTID(self, t):
        if t.value.upper() in self.RESERVED_WORDS:
            t.type = t.value.upper()
        if t.value.upper() in ("TRUE," "FALSE"):
            t.type = "BOOL_CONST"
            t.value = t.value.upper() == "TRUE"
        return t
    
    @_(r'\d+')
    def INT_CONST(self, t):
        t.type = "INT_CONST"
        t.value = int(t.value)
        return t

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1
    
    @_(r'[A-Z][A-Z0-9_a-z]*')
    def TYPEID(self, t):
        if t.value.upper() not in self.RESERVED_WORDS:
            t.type = "TYPEID"
        return t

    @_(r'.')
    def ERROR(self, t):
        print(t)
        if t.value in self.literals:
            t.type = t.value
            return t

    def error(self, t):
        self.index += 1
    
    
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
                result = f'#{token.lineno} \'{token.type}\' '
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
