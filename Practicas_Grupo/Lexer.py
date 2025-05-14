# coding: utf-8

from sly import Lexer
import os
import re
import sys

from sly import lex

class Comentario(Lexer):
    tokens = {}

    _numero_anidados = 1


    @_(r'\n')
    def LINEA(self, t):
        self.lineno += 1
        if self._numero_anidados == 0:
            self.begin(CoolLexer)

    @_(r'\*\)')
    def VOLVER(self, t):
        self._numero_anidados -= 1
        if self._numero_anidados == 0:
            self.begin(CoolLexer)
        pass

    @_(r'\(\*')
    def ANIDAR(self, t):
        if self._numero_anidados != 0:
            self._numero_anidados += 1

    @_(r'.')
    def PASAR(self, t):
        pass

class CadenaTexto(Lexer):
    tokens = {}
    _cadena = ''

    @_(r'\\\x00\"\n')
    def ERROR_NULL(self, t):
        t.value = '"String contains escaped null character."'
        t.type = 'ERROR'
        self._cadena = ''
        return t

    @_(r'\\"')
    def COMILLAS(self, t):
        if len(self.text) <= t.end and t.value != '"':
            t.value = '"EOF in string constant"'
            t.type = 'ERROR'
            self._cadena = ''
            return t
        self._cadena += '\\"'

    @_(r'\\\r\n')
    def BARRA_RN_BIEN(self, t):
        self._cadena += '\\n' 

    @_(r'\\\t')
    def BARRA_T_TRIPLE(self, t):
        self._cadena += '\\t'

    @_(r'\\\x08')
    def BARRA_B(self, t):
        self._cadena += '\\b'

    @_(r'\\\x0c')
    def BARRA_F(self, t):
        self._cadena += '\\f'

    @_(r'\\')
    def BARA_BARA(self, t):
        self._cadena += t.value

    @_(r'\"')
    def VOLVER(self, t):
        self.begin(CoolLexer)
        t.value = '"' + self._cadena +'"'
        t.type = 'STR_CONST'
        self._cadena = ''
        return t

    @_(r'\r\n')
    def BARRA_RN(self, t):
        self.begin(CoolLexer)
        t.value = '"Unterminated string constant"'
        t.type = 'ERROR'
        self._cadena = ''
        return t

    @_(r'\n')
    def BARRA_N(self, t):
        self._cadena += '\\n'

    @_(r'\t')
    def BARRA_T(self, t):
        self._cadena += '\\t'
    
    @_(r'\r')
    def BARRA_R(self, t):
        self._cadena += '\\015'

    @_(r'\x1b')
    def BARRA_E(self, t):
        self._cadena += '\\033'

    @_(r'\\.')
    def BARRA(self, t):
        self._cadena += t.value[1]


    @_(r'.')
    def CUALQUIER_COSA(self, t):
        if t.index == 95:
            print(t.value)
        if len(self.text) <= t.end and t.value != '"':
            t.value = '"EOF in string constant"'
            t.type = 'ERROR'
            self._cadena = ''
            return t
        self._cadena += t.value

class ASSIGN(Lexer):
    tokens = {}


    @_(r'\-')
    def VOLVER(self, t):
        self.begin(CoolLexer)
        t.type = 'ASSIGN'
        t.value = ''
        return t

    @_(r'.')
    def CUALQUIER_COSA(self, t):
        self.begin(CoolLexer)
        return t
    
class BOOLEANT(Lexer):
    tokens = {}
    _cadena = 'tru'

    @_(r'[^eE][a-zA-Z0-9]*')
    def VOLVERNOBOOL(self, t):
        t.value = self._cadena + t.value
        self.begin(CoolLexer)
        t.type = 'OBJECTID'
        return t

    @_(r'[eE][a-zA-Z0-9]+')
    def VOLVERCASIBOOL(self, t):
        t.value = self._cadena + t.value
        self.begin(CoolLexer)
        t.type = 'OBJECTID'
        return t
    
    @_(r'[eE]')
    def VOLVER(self, t):
        self.begin(CoolLexer)
        t.type = 'BOOL_CONST'
        t.value = True
        return t

class BOOLEANF(Lexer):
    tokens = {}
    _cadena = 'fals'

    @_(r'[^eE][a-zA-Z0-9]*')
    def VOLVERNOBOOL(self, t):
        t.value = self._cadena + t.value
        self.begin(CoolLexer)
        t.type = 'OBJECTID'
        return t

    @_(r'[eE][a-zA-Z0-9]+')
    def VOLVERCASIBOOL(self, t):
        t.value = self._cadena + t.value
        self.begin(CoolLexer)
        t.type = 'OBJECTID'
        return t
    
    @_(r'[eE]')
    def VOLVER(self, t):
        self.begin(CoolLexer)
        t.type = 'BOOL_CONST'
        t.value = False
        return t

class CoolLexer(Lexer):
    tokens = {BOOL_CONST, OBJECTID, INT_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, STR_CONST, LE, DARROW, ASSIGN,
              TRUE, FALSE, COMMENT, COMMENT1LINEA, LE}
    ignore = '\t '
    literals = {'=', '+', '-', '*', '/', '(', ')', '<', '>', '.', '~', ',', ';', ':', '@', '{', '}'}
    key_words = {'else', 'if', 'fi', 'then', 'not', 'in', 'case', 'esac', 'class', 'inherits', 'isvoid',
                 'let', 'loop', 'new', 'of', 'pool', 'then', 'while'}

    #LE = r'\b[lL][eE]\b'
    #DARROW = r'\b[\=][\>]\b'
   # ASSIGN = r'\b[\<][\-]\b'
    #STR_CONST = r'"[a-zA-Z0-9_\:\\\s\b\r\n]*"'


    _numero_anidados = 0


    # @_(r'\"[a-zA-Z0-9_\-\:\\\s\t\b\f\015\033]*\"')
    # def STR_CONST(self, t):
    #     t.value = t.value.replace('\t', r't').replace('\b', r'b').replace('\f', r'f').replace('\015', '\\015').replace('\033', '\\033')
    #     return t

    @_(r'\=\>')
    def DARROW(self, t):
        t.type = 'DARROW'
        return t
    
    @_(r'\<\=')
    def LE(self, t):
        t.type = 'LE'
        return t

    @_(r'\<\-')
    def ASSIGN(self, t):
        t.type = 'ASSIGN'
        return t

    @_(r'\"')
    def STRING(self, t):
        self.begin(CadenaTexto)

    #aqui antes iba '-?\d+'
    @_(r'\d+')
    def INT_CONST(self, t):
        #t.value = int(t.value)
        return t

    @_(r't[rR][uU]')
    def BOOL_CONSTT(self, t):
        t.type = 'BOOL_CONST'
        self.begin(BOOLEANT)

    @_(r'f[aA][lL][sS]')
    def BOOL_CONSTF(self, t):
        t.type = 'BOOL_CONST'
        self.begin(BOOLEANF)

    @_(r'\_')
    def BARRABAJA(self, t):
        t.type = 'ERROR'
        t.value = '"_"'
        return t

    @_(r'[a-z][A-Z0-9_a-z]*')
    def OBJECTID(self, t):
        if t.value.lower() in self.key_words:
            t.type = t.value.upper()
        return t
    @_(r'[A-Z][A-Z0-9_a-z]*')
    def TYPEID(self, t):
        if t.value.lower() in self.key_words:
            t.type = t.value.upper()
        return t
    
    @_(r'\n|\r')
    def LINEBREAK(self, t):
        self.lineno += 1

    @_(r'\b[wW][hH][iI][lL][eE]\b')
    def WHILE(self, t):
        t.value = (t.value) + 'dddd'
        return t

    @_(r'\(\*')
    def COMMENT(self, t):
        self._numero_anidados += 1
        self.begin(Comentario)

    @_(r'\*\)')
    def ERRORCIERRE(self, t):
        t.value = '"Unmatched *)"'
        t.type = 'ERROR'
        return t

    @_(r'--.*')
    def COMMENT1LINEA(self, t):
        pass

    @_(r'[\!\#\$\%\^\&\_\>\?\`\[\]\|]')
    def CARACTER_INVALIDO(self, t):
        t.value = '"' + t.value + '"'
        t.type = 'ERROR'
        return t
    
    @_(r'\\')
    def BARRA_SOLA(self, t):
        t.value = '"\\\\"'
        t.type = 'ERROR'
        return t
    
    @_(r'\x01|\x02|\x03|\x04')
    def ERRORES_CONTROL(self, t):
        valor = t.value
        match valor:
            case '\x01':
                t.value = '"\\001"'
            case '\x02':
                t.value = '"\\002"'
            case '\x03':
                t.value = '"\\003"'
            case '\x04':   
                t.value = '"\\004"'
        t.type = 'ERROR'
        return t


    @_(r'.')
    def ERROR(self, t):
        if t.value is None:
            t.value = '"EOF in string constant"'
            t.type = 'ERROR'
            return t
        if t.value in self.literals:
            t.type = t.value
            return t
        print(t)

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
            if token.type == 'COMMENT':
                result += f'(* {token.value} *)'
            elif token.type == 'COMMENT1LINEA':
                result += f'-- {token.value}'
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type == 'ASSIGN':
                result = f" {token.type}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\''
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append('\n'+result)
        return list_strings
