from sly import Lexer
import re

class SVGLexer(Lexer):
    tokens = {ABRE, CIERRE, ABRECIERRA}
    ignore = ' \t'
    atributos: dict[str, dict[str]] = dict()

    @_(r'<\w+(\s|[\w-]+=\"[\w,:/.]+\")*>')
    def ABRE(self, t):
        etiqueta = re.search(r'<(\w+)', t.value).group(1)
        atts = re.findall(r'[\w-]+=\"[\w,:/.]+\"', t.value)
        self.atributos[etiqueta] = dict()
        for att in atts:
            key, value = att.split("=")
            value = value[1:-1]
            self.atributos[etiqueta][key] = value
        t.value = self.atributos[etiqueta]
        t.value["name"] = etiqueta
        return t

    @_(r'<\w+(\s|[\w-]+=\"[\w,:/.]+\")*/>')
    def ABRECIERRA(self, t):
        etiqueta = re.search(r'<(\w+)', t.value).group(1)
        atts = re.findall(r'[\w-]+=\"[\w,:/.]+\"', t.value)
        self.atributos[etiqueta] = dict()
        for att in atts:
            key, value = att.split("=")
            value = value[1:-1]
            self.atributos[etiqueta][key] = value
        t.value = self.atributos[etiqueta]
        t.value["name"] = etiqueta
        return t

    @_(r'</\w+>')
    def CIERRE(self, t):
        return t
    
    @_(r'\s+')
    def ESPACIOS(self, t):
        self.lineno += t.value.count('\n')
    
    @_(r'<!--[^>]*>')
    def COMENTARIO(self, t):
        pass
DEBUG = 0
if DEBUG :
    print("hola")

    with open("Ejemplos\\ejemplo.xml", "r") as f:
        svg = f.read()

    ejemplo = '<rect x="10" y="10" width="100" height="100">'
    lexer = SVGLexer()
    for tok in lexer.tokenize(svg):
        print(tok)

    print(lexer.atributos)
