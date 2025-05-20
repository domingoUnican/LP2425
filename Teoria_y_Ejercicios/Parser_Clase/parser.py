from lexer import *
from representacion import *
import matplotlib.pyplot as plt

import os

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.current = 0

    def parse(self):
        try:
            resultado = self.svg()
            if not self.isAtEnd():
                raise Exception("Sobran tokens")
            return resultado
        except RuntimeError as e:
            print(f"Error durante el análisis: {e}")
            return None

    def svg(self):
        if self.isAtEnd():
            return None

        # Crear el nodo SVG
        if not self.check("ABRE") and not self.check("ABRECIERRA"):
            raise RuntimeError("Se esperaba una etiqueta ABRE o ABRECIERRA")

        resultado = SVG(tipo=self.peek().value["name"], atributos=dict(), hijos=[])
        del self.peek().value["name"]
        resultado.atributos = self.peek().value

        if self.match("ABRE"):
            while not self.match("CIERRE"):
                if self.isAtEnd():
                    raise RuntimeError("Se esperaba una etiqueta CIERRE, pero se alcanzó el final del archivo")
                hijo = self.svg()
                if hijo:
                    resultado.hijos.append(hijo)

        elif self.match("ABRECIERRA"):
            # Etiqueta auto-cerrada, no tiene hijos
            return resultado

        else:
            raise RuntimeError("Etiqueta no válida encontrada")

        return resultado

    def match(self, tipo):
        if self.check(tipo):
            self.advance()
            return True
        return False

    def check(self, tipo):
        if self.isAtEnd():
            return False
        return self.peek().type == tipo

    def isAtEnd(self):
        return self.current >= len(self.tokens)

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()


if __name__ == "__main__":
    try:
        with open("Ejemplos\\ejemplo.xml", "r") as f:
            svg = f.read()

        lexer = SVGLexer()
        tokens = list(lexer.tokenize(svg))

        parser = Parser(tokens)
        svg = parser.parse()

        # Crear la figura y los ejes
        nrows = int(int(svg.atributos["height"]) / 100)
        ncols = int(int(svg.atributos["width"]) / 100)
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols)
        svg.fig = fig
        svg.ax = ax
        svg.plt = plt
        svg.dibuja()
        plt.show()

        # print(svg)
    except FileNotFoundError:
        print("El archivo 'Ejemplos\\ejemplo.xml' no se encontró.")
