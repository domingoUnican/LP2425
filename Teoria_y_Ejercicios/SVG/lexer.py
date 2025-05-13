from sly import Lexer
import re

class SVGLexer(Lexer):
    tokens = {ABRE, CIERRE, ABRECIERRE}
    ignore = ' \t'

    @_(r'<\w+(\s|[\w-]+=\"[\w,:/.]+\")*>')
    def ABRE(self, t):
        t.type = 'ABRE'
        t.lineno = self.lineno
        m = re.match(r'<(?P<tag>\w+)(?P<attrs>(?:\s+[\w-]+="[\w,:/.]+")*)\s*>', t.value)
        if m:
            tag_name = m.group('tag')
            attrs = {"tag": tag_name}
            for key, val in re.findall(r'([\w-]+)="([\w,:/.]+)"', m.group('attrs')):
                attrs[key] = val
            t.value = attrs
        return t
    
    @_(r'</\w+>')
    def CIERRE(self, t):
        t.type = 'CIERRE'
        t.lineno = self.lineno
        m = re.match(r'</(?P<tag>\w+)>', t.value)
        if m:
            tag_name = m.group('tag')
            t.value = {"tag": tag_name}
        else:
            t.value = {}
        return t
    
    @_(r'<\w+(\s|[\w-]+=\"[\w,:/.]+\")*/>')
    def ABRECIERRE(self, t):
        t.type = 'ABRECIERRE'
        t.lineno = self.lineno
        m = re.match(r'<(?P<tag>\w+)(?P<attrs>(?:\s+[\w-]+="[\w,:/.]+")*)\s*/>', t.value)
        if m:
            tag_name = m.group('tag')
            attrs = {"tag": tag_name}
            for key, val in re.findall(r'([\w-]+)="([\w,:/.]+)"', m.group('attrs')):
                attrs[key] = val
            t.value = attrs
        else:
            t.value = {}
        return t
    
    @_(r'\s+')
    def ESPACIOS(self, t):
        self.lineno += t.value.count('\n')
    
    @_(r'<!--[^>]*>')
    def COMENTARIO(self, t):
        pass


lexer = SVGLexer()
#for tok in lexer.tokenize('<rect x="10" y="10" width="100" height="100"> </rect> <rect x="10" y="10" width="100" height="100"/>'):
#    print(tok)
