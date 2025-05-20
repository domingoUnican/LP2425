from lexer import *
from representacion import SVG

class Parser:
    current = 0

    def __init__(self,tokens):
        self.tokens = list(tokens)
  

    def match(self,tipo) :
        if  self.check(tipo):
            return True
        return False

    def check(self,tipo):
        if self.isAtEnd():
            return False
        return self.peek().type == tipo

    def isAtEnd(self):
        return self.current >= len(self.tokens)
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current-1]

    def advance(self):
        if self.isAtEnd() == False:
            self.current += 1
        return self.previous()
    
    def parse(self):
        result = self.svg()
        if self.isAtEnd():
            return result
        else:
            raise Exception(f"Error de sintaxis: {self.peek().value}")

    def svg(self):
        if self.match('ABRE'):
            self.advance()
            tag = self.previous().value["tag"]
            atributos = self.previous().value
            atributos = {k: v for k, v in atributos.items() if k != "tag"}
            hijos = []
            while not self.match('CIERRE') and not self.isAtEnd():
                if self.match('ABRE'):
                    hijos.append(self.svg())
                elif self.match('ABRECIERRE'):
                    hijos.append(self.svg())
                else:
                    self.advance()
            if self.match('CIERRE'):
                self.advance()
                return SVG(tag, atributos, hijos)
        elif self.match('ABRECIERRE'):
            tag = self.peek().value["tag"]
            atributos = self.peek().value
            atributos = {k: v for k, v in atributos.items() if k != "tag"}
            self.advance()
            return SVG(tag, atributos, [])
        elif self.match('CIERRE'):
            tag = self.peek().value["tag"]
            return SVG(tag, {}, [])
        return None
    

if __name__ == "__main__":
    lexer = SVGLexer()
    parser = Parser(lexer.tokenize('<rect x="10" y="10" width="100" height="100"> <circle cx="50" cy="50" r="40"> <square x="20" y="20" width="50" height="50"/> </circle> </rect>'))
    svg = parser.parse()
    print(svg)
    

