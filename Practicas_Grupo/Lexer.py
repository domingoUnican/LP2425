# coding: utf-8

from sly import Lexer
import os
import re
import sys



class Comentario(Lexer):
    tokens = {}

    _numero_anidados = 1

    
    @_(r'\n')
    def LINEA(self, t):
        self.lineno += 1
        if self._numero_anidados == 0:
            self.begin(CoolLexer)
        
        
    @_(r'\*\)')
    def VOLVER(self, t):
        self._numero_anidados -= 1
        if self._numero_anidados == 0:
            self.begin(CoolLexer)
        pass

    
        
    @_(r'\(\*')
    def ANIDAR(self, t):
        if self._numero_anidados != 0:
            self._numero_anidados += 1

    @_(r'.')
    def PASAR(self, t):
        pass



class CoolLexer(Lexer):
    tokens = {BOOL_CONST, OBJECTID, INT_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN, 
              TRUE, FALSE, COMMENT, COMMENT1LINEA}
    ignore = '\t '
    literals = {'=', '+', '-', '*', '/',
                '(', ')', '<', '>', '.', '~', ',', ';', ':', '@', '{', '}'}
    key_words = {'else', 'if', 'fi', 'then', 'not', 'in', 'case', 'esac', 'class', 'inherits', 'isvoid', 
                 'let', 'loop', 'new', 'of', 'pool', 'then', 'while'}
    
    LE = r'\b[lL][eE]\b'
    DARROW = r'\b[\=][\>]\b'
    ASSIGN = r'\b[\<][\-]\b'
    #STR_CONST = r'"[a-zA-Z0-9_\:\\\s\b\r\n]*"'

    
    _numero_anidados = 0
    

    @_(r'"[a-zA-Z0-9_\:\\\s\t\b\f\015\033]*"')
    def STR_CONST(self, t):
        t.value = t.value.replace('\t', r't').replace('\b', r'b').replace('\f', r'f').replace('\015', '\\015').replace('\033', '\\033')
        return t


    @_(r'-?\d+')
    def INT_CONST(self, t):
        t.value = int(t.value)
        return t
    
    @_(r't[rR][uU][eE]')
    def BOOL_CONST(self, t):
        t.value = True
        return t
    
    @_(r'[a-z][A-Z0-9_a-z]*')
    def OBJECTID(self, t):
        if t.value.lower() in self.key_words:
            t.type = t.value.upper()
        return t
    @_(r'[A-Z][A-Z0-9_a-z]*')
    def TYPEID(self, t):
        if t.value.lower() in self.key_words:
            t.type = t.value.upper()
        return t
    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1
    
    @_(r'\b[wW][hH][iI][lL][eE]\b')
    def WHILE(self, t):
        t.value = (t.value) + 'dddd'
        return t
    
    @_(r'\(\*')
    def COMMENT(self, t):
        self._numero_anidados += 1
        self.begin(Comentario)
    
    @_(r'\*\)')
    def ERRORCIERRE(self, t):
        t.value = '"Unmatched *)"'
        t.type = 'ERROR'
        return t
        
    @_(r'--.*')
    def COMMENT1LINEA(self, t):
        pass

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
    @_(r'\(\*')
    def IR(self, t):
        self.begin(Comentario)

    def error(self, t):
        self.index += 1
        
    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'COMMENT':
                result += f'(* {token.value} *)'
            elif token.type == 'COMMENT1LINEA':
                result += f'-- {token.value}'
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '

            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        return list_strings
