# coding: utf-8

from sly import Lexer


class Strings(Lexer):
    tokens = {ERROR, STR_CONST}
    _caracteres = '"'
    _contador = 0

    @_(r'\\"$')
    def ERROR_ESCAPED_QUOTE(self, t):
        self.lineno += 1
        self._caracteres = '"'
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        self._caracteres = '"'
        self._contador = 0
        self.begin(CoolLexer)
        return t
    
    @_(r'(\\\\)*"')
    def STR_CONST(self, t):
        self._contador *= (len(t.value)-1)//2
        if self._contador < 1024:
            self._caracteres += t.value
            t.value = self._caracteres
        else:
            t.value = '"String constant too long"'
            t.type = "ERROR"
        self._caracteres = '"'
        self._contador = 0
        self.begin(CoolLexer)
        return t

    @_(r'\\[\\"ntbf]')
    def ADD_SPECIAL(self, t):
        self._contador += 1
        self._caracteres += t.value

    @_(r'\\\w')
    def ADD_SCAPED(self, t):
        self._contador += 1        
        self._caracteres += t.value[-1]

    @_(r'\t')
    def TAB(self, t):
        self._contador += 1        
        self._caracteres += r"\t"


    @_(r'\\\n$')
    def ERROR_ADD_LINE(self, t):
        self.lineno += 1
        self._caracteres = '"'
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        self._caracteres = '"'
        self._contador = 0
        self.begin(CoolLexer)
        return t
    

        


    @_(r'\\\n')
    def ADD_LINE(self, t):
        self._contador += 1
        self.lineno += 1
        self._caracteres += r'\n'

    
    
    @_(r'([^"]|(\\\n))$')
    def FIN_FICHERO(self, t):
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        self._caracteres = '"'
        self.begin(CoolLexer)
        return t

    @_(r'.*\x00[^"]*"?')
    def CARACTER_FIN(self, t):
        self._caracteres = '"'
        t.type = "ERROR"
        if '\\\x00' in t.value: 
            t.value = '"String contains escaped null character."'
        else:
            t.value = '"String contains null character."'
        self.begin(CoolLexer)
        return t

    @_(r'\n')
    def SALTO_LINEA(self, t):
        self._caracteres = '"'
        self.lineno += 1
        t.type = "ERROR"
        t.value = '"Unterminated string constant"'
        self._contador = 0
        self.begin(CoolLexer)
        return t
    @_(r'.')
    def CAR(self, t):
        self._contador += 1
        if t.value in CoolLexer.CARACTERES_CONTROL:
                self._caracteres += (
                    '\\'+str(oct(int(t.value.encode("ascii").hex(), 16)).replace('o', '0'))[-3:])
        else:
            self._caracteres += t.value

    def error(self, t):
        print(f'ERROR en linea {t.lineno} por {t.value}\n')

class Comments(Lexer):
    tokens = {}
    profundidad = 1


    @_(r'\n?\(\*\*\)')
    def COMMENTOPEN(self, t):
        pass
        
    @_(r'[^\\]\*\)$')
    def ERROR(self, t):
        self.profundidad -= 1
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)
        else:
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            self.begin(CoolLexer)
            return t

    @_(r'(.|\n)$')
    def ERROR2(self, t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        self.begin(CoolLexer)
        return t
    
    @_(r'([^\\]\*\))')
    def INSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad -= 1
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)

    @_(r'[^\\]\(\*')
    def OUTSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad += 1
    @_(r'\n')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'.')
    def EAT(self, t):
        pass

    def salida(self, texto):
        return ['#1 ERROR "EOF in string constant"']
    

class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC,
              CLASS, INHERITS, ISVOID, LET, LOOP,
              NEW, OF, POOL, THEN, WHILE, STR_CONST,
              LE, DARROW, ASSIGN}
    _key_words = {'else', 'if', 'fi', 'then', 'not',
                  'in', 'case', 'esac', 'class', 'inherits',
                  'isvoid', 'let', 'loop', 'new', 'of', 'pool',
                  'then', 'while'}
    #ignore = '\t '
    literals = {'=', '+', '-', '*', '/',
                '(', ')', '<', '>', '.', '~', ',', ';', ':', '@', '{', '}'}

    LE = r'<='
    DARROW = r'=>'
    ASSIGN = r'<-'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r'"')
    def STR_CONST(self, t):
        self.begin(Strings)
        

    @_(r'[!#$%^&_>\?`\[\]\\\|\x00]')
    def ERROR2(self, t):
        t.type = "ERROR"
        if t.value == '\\':
            t.value = '\\\\'
        if t.value in self.CARACTERES_CONTROL:
            t.value = '\\' + \
                str(oct(int(t.value.encode("ascii").hex(), 16)
                        ).replace('o', '0')[-3:])
        t.value = '"'+t.value+'"'
        return t

    @_(r'\(\*\*\)')
    def COMMENT0(self, t):
        pass
    @_(r'\(\*$')
    def ERROR7(self, t):
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        return t

    
    @_(r'\(\*')
    def COMMENT(self, t):
        Comments.profundidad = 1
        self.begin(Comments)

    
    @_(r'\*\)')
    def ERRORCIERRE(self, t):
        t.value = '"Unmatched *)"'
        t.type = 'ERROR'
        return t
        
    @_(r'--.*(\n|$)')
    def LINECOMMENT(self, t):
        self.lineno += t.value.count("\n")

    @_(r'\d+')
    def INT_CONST(self, t):
        t.value = t.value
        return t

    @_(r'\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b')
    def BOOL_CONST(self, t):
        t.value = t.value[0] =='t'
        return t

    @_(r'[A-Z][a-zA-Z0-9_]*')
    def TYPEID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r'[a-z_][a-zA-Z0-9_]*')
    def OBJECTID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    def salida(self, texto):
        list_strings = []
        lexer = CoolLexer()
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\''
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

    def tests(self):
        for fich in TESTS:
            f = open(os.path.join(DIR, fich), 'r')
            g = open(os.path.join(DIR, fich + '.out'), 'r')
            resultado = g.read()
            entrada = f.read()
            texto = '\n'.join(self.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")

