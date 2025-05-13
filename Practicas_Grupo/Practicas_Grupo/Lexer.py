# coding: utf-8

from sly import Lexer
import os
import re
import sys

class Comentario(Lexer):
    tokens = {}
    anidados = 1

    @_(r'\(\*')
    def COMMENT(self, t):
        self.anidados += 1
    @_(r'\*\)')
    def VOLVER(self, t):
        self.anidados -= 1
        #print("Anidados: ", self.anidados)
        if self.anidados <= 0:
            #print("Me largo")
            self.begin(CoolLexer)
    @_(r'\n')
    def LINEA(self, t):
        self.lineno += 1
    @_(r'.')
    def PASAR(self, t):
        pass

class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN}
    ignore = '\t '
    literals = {'+', '-', '*', '/',
                '(', ')', '<', '>', '.', '~', ',', ';', ':', '@', '{', '}','='}
    ELSE = r'\b[eE][lL][sS][eE]\b'
    STR_CONST = r'"[\w,\s\\\/\+\-\*\=\(\)]*"'
    
    @_(r'\(\*')
    def BLOCKCOMMENT(self, t):
        self.begin(Comentario)
    
    def STR_CONST(self, t):
        t.type = 'STR_CONST'
        t.value = re.sub(r'\\([^btnr])', r'\1', t.value)
        return t
    
    @_(r'--.*')
    def LINECOMMENT(self, t):
        pass

    @_(r'[a-z][A-Z0-9_a-z]*')
    def OBJECTID(self, t):
        if t.value.upper() in ("ELSE", "IF", "FI", "THEN", "NOT", "IN", "CASE", "ESAC", "CLASS",
                               "INHERITS", "ISVOID", "LET", "LOOP", "NEW", "OF",
                               "POOL", "THEN", "WHILE"):
            t.type = t.value.upper()
        if t.value.upper() in ("TRUE", "FALSE"):
            t.type = "BOOL_CONST"
        return t
    @_(r'[A-Z][A-Z0-9_a-z]*')
    def TYPEID(self, t):
        if t.value.upper() in ("ELSE", "IF", "FI", "THEN", "NOT", "IN", "CASE", "ESAC", "CLASS",
                               "INHERITS", "ISVOID", "LET", "LOOP", "NEW", "OF",
                               "POOL", "THEN", "WHILE"):
            t.type = t.value.upper()
        return t
    
    @_(r'[0-9]+')
    def INT_CONST(self, t):
        t.value = int(t.value)
        return t
    @_(r'<=')
    def LE(self, t):
        return t
    @_(r'=>')
    def DARROW(self, t):
        return t
    @_(r'<-')
    def ASSIGN(self, t):
        return t
    @_(r'\s')
    def SPACE(self, t):
        self.lineno += t.value.count('\n')
        pass

    @_(r'\n')
    def LINEBREAK(self, t):
        self.lineno += 1

    @_(r'.')
    def LITERAL(self, t):
        if t.value in self.literals:
            t.type = t.value
        return t

    @_(r'.')
    def ERROR(self, t):
        print(t)
        if t.value in self.literals:
            t.type = t.value
    
    
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
        
if __name__ == '__main__':
    

    txt = r'''
    class Main {
        main(): Object {
            out_string("Hello, World\n");
            out_int(0);
            out_string("\n");
            -- Coment
            return 0
        };
    };
    '''

    for token in CoolLexer().tokenize(txt):
        print(token)

    # directory = './01/grading'
    # for filename in os.listdir(directory):
    #     if filename.endswith(".txt"):
    #         filepath = os.path.join(directory, filename)
    #         with open(filepath, 'r', encoding='utf-8') as file:
    #             content = file.read()
    #             for token in lexer.tokenize(content):
    #                 print(token)
