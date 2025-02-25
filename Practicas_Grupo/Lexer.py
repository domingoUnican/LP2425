# coding: utf-8

from sly import Lexer
import os
import re
import sys


class Comentario(Lexer):
    tokens = {}
    @_(r'.')
    def PASAR(self, t):
        pass
    @_(r'\n')
    def LINEA(self, t):
        self.lineno += 1
    @_(r'\*\)')
    def VOLVER(self, t):
        self.begin(CoolLexer)




class CoolLexer(Lexer):
    tokens = {BOOL_CONST, OBJECTID, INT_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN, TRUE, FALSE}
    ignore = '\t '
    literals = {'.', ',', ';', ':', '@', '(', ')', '{', '}', '+', '-', '*', '/', '<', '=', '~'}
    keywords = {'else', 'if', 'fi', 'then', 'not', 'in', 'case', 'esac', 'class',
                'inherits', 'isvoid', 'let', 'loop', 'new', 'of', 'pool', 'then', 'while'}
    LE = r'<='
    DARROW = r'=>'
    ASSIGN = r'<-'
    #STR_CONST = r'"[a-zA-Z0-9_\:\\\s]*"'

    @_(r'"[a-zA-Z0-9_\:\\\s\n\b\f\t\033\015]*"')
    def STR_CONST(self, t):
        t.value = t.value.replace('\n', r'n').replace('\b', r'b').replace('\f', r'f').replace('\t', r't').replace('\033', '\\033').replace('\015', '\\015')
        return t
    

    @_(r'\b[0-9]+\b')
    def INT_CONST(self, t):
        t.value = int(t.value)
        return t
    
    @_(r't[rR][uU][eE]')
    def BOOL_CONST(self, t):
        t.value = True
        return t

    @_(r'\b[a-z][A-Z0-9_a-z]*\b')
    def OBJECTID(self, t):
        if t.value in self.keywords:
            t.type = t.value.upper()
        return t
    
    @_(r'\b[A-Z][A-Z0-9_a-z]*\b')
    def TYPEID(self, t):
        if t.value in self.keywords:
            t.type = t.value.upper()
        return t
    

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1

    
    
    @_(r'\b[wW][hH][iI][lL][eE]\b')
    def WHILE(self, t):
        t.value = (t.value) + 'dddd'
        return t
    @_(r'.')
    def ERROR(self, t):
        print(t)
        if t.value in self.literals:
            t.type = t.value
    
    @_(r'\w+')
    def TYPEID(self, t):
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
            if token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'STR_CONST':
                result += f'"{token.value}"'
            elif token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'ASSIGN':
                result += '<-'
            elif token.type == 'DARROW':
                result += '=>'
            elif token.type == 'LE':            
                result += '<='
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
