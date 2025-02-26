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
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN}
    ignore = '\t '
    literals = {'.'}
    ELSE = r'\b[eE][lL][sS][eE]\b'
    STR_CONST = r'"[a-zA-Z0-9_/]*"'
    
    @_(r'\b[a-z][A-Z0-9_a-z]*\b')
    def OBJECTID(self, t):
        if (t.value.upper() in self.tokens):
            t.type = t.value.upper()
        else:
            t.type = 'OBJECTID'
        return t
    
    @_(r'\b[A-Z][A-Z0-9_a-z]*\b')
    def TYPEID(self, t):
        if (t.value.upper() in self.tokens):
            t.type = t.value.upper()
        else:
            t.type = 'TYPEID'
        return t
    
    @_(r'[0-9]+')
    def INT_CONST(self, t):
        t.value = int(t.value)
        t.type = 'INT_CONST'
        return t
    
    @_(r'"[\w\s]*"')
    def STR_CONST(self, t):
        t.type = 'STR_CONST'
        # Ignoro las comillas, los /b, /t, /n y /r, pero sustitullo los /. por el caracter correspondiente
        print("Antes", t.value)
        t.value = re.sub(r'\\([^\Wbtnr])', r'\1', t.value)
        print("Despues", t.value)
        return t

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1
    
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

if __name__ == '__main__':
    lexer = CoolLexer()
    text = """

    class Main {
        main(): Object {
            out_string("Hello, World mohamed\n");
            out_int(0);
            out_string("\n");
            return 0;
        };
    };
    """

    for tk in CoolLexer().tokenize(text):
        print(tk)