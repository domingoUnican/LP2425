from sly import Lexer

class SVGLexer(Lexer):
    tokens = {ABRE, CIERRE, ABRECIERRE}
    ignore = ' \t'

    @_(r'<\w+(\s|[\w-]+=\"[\w,:/.]+\")*>')
    def ABRE(self, t):
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

print("hola")
lexer = SVGLexer()
for tok in lexer.tokenize('<rect x="10" y="10" width="100" height="100">'):
    print(tok)
