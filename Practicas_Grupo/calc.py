from sly import Lexer, Parser
from Clases import *


class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, CLASS }
    ignore = ' \t'
    literals = {'{', '}', '=', '+', '-', '*', '/', '(', ')', ',' }

    # Tokens
    CLASS = r'class'
    NAME = r'[A-Z]'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    @_(r'clases')
    def programa(self, p):
        return p.clase

    @_(r"clase ';' clases ")
    def clases(self, p):
        pass

    @_(r' CLASS NAME "{" "}" ')
    def clase(self, p):
        return Clase(nombre = p.NAME)
        
if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            print(parser.parse(lexer.tokenize(text)).str(0))
