# coding: utf-8

from sly import Lexer

### TODO
# (Carlos dice) Fallos que encuentro y no conseguí solucionar:
    ## 1: El lineno de los STRINGS da error en al menos 3 tests. El fallo se puede comprobar con un print que anhadí
    ##    al main. Este print saca primero la salida generada nuestra y despues la salida correcta. Se puede apreciar 
    ##    que el error que da esto de los lineno es porque el primer token en la salida empieza en el lineno=2, y de ahi 
    ##    en adelante "crecen" igual, o muy parecidos. Tengo la duda de si los tests estan mal hechos, no me explico lo de
    ##    que empiecen en lineno=2
    
    ## 2: Los caracteres especiales dan problemas. Estos son "\b", "\t", "\f" . Hay mas caarctes especiales, pero no los he
    ##    encontrado en los tests que he intentado pasar. El problema es que no se leen como espero (se ponen como 
    ##    <slash>+<numero> o como <slash><slash>+<letra>, nunca termino medio, que es el correcto.).
    
    ## Estos errosres son los mas repetidos entre los tests que fallan, por lko que es de esperar que cuando se solucionen 
    ## tendremos mas tests que pasen que los propiamente tratados, por no decir que todos.
    

class Strings(Lexer):
    tokens = {ERROR, STR_CONST}
    _caracteres = '"'
    _contador = 0
    
    

    def _reset_state(self):
        self._caracteres = '"'
        self._contador = 0
        self.begin(CoolLexer)

    def _set_error(self, t, message):
        t.type = "ERROR"
        t.value = f'"{message}"'
        self._reset_state()
        return t


    @_(r'\\"$')
    def ERROR_ESCAPED_QUOTE(self, t):
        self.lineno += 1
        return self._set_error(t, "EOF in string constant")

    @_(r'(\\\\)*"')
    def STR_CONST(self, t):
        self._contador *= (len(t.value) - 1) // 2
        if self._contador < 1024:
            self._caracteres += t.value
            t.value = self._caracteres
            t.type = "STR_CONST"
        else:
            return self._set_error(t, "String constant too long")
        self._reset_state()
        # self.lineno += 1
        return t

    @_(r'\\[\\"ntbf]')
    def ADD_SPECIAL(self, t):
        print(f"Carácter de escape: {t.value}")
        self._contador += 1
        if t.value == "\\n":
            self._caracteres += r"\n"
        elif t.value == "\\t":
            self._caracteres += r"\t"
        elif t.value == "\\b":
            self._caracteres += r"\b"
        elif t.value == "\\f":
            self._caracteres += r"\f"
        elif t.value == "\\r":
            self._caracteres += r"\r"
        elif t.value == '\\"':
            self._caracteres += r'\"'
        elif t.value == "\\\\":
            self._caracteres += r"\\"
        else:
            self._caracteres += t.value[-1]
        # self.lineno += 1
    


    @_(r"\\\w")
    def ADD_ESCAPED(self, t):
        # print(f"Carácter de escape: {t.value}")
        # self.lineno += 1
        self._contador += 1
        self._caracteres += t.value[-1]

    @_(r"\\t")
    def TAB(self, t):
        self._contador += 1
        self._caracteres += r'\\\t'

    @_(r"\\\n$")
    def ERROR_ADD_LINE(self, t):
        self.lineno += 1
        return self._set_error(t, "EOF in string constant")

    @_(r"\\\n")
    def ADD_LINE(self, t):
        self._contador += 1
        self.lineno += 1
        self._caracteres += r"\n"
        print(f"ESTTTTTSSTTSST de continuación de línea: {t.value}")

    @_(r'([^"]|(\\\n))$')
    def FIN_FICHERO(self, t):
        return self._set_error(t, "EOF in string constant")

    @_(r'.*\x00[^"]*"?')
    def CARACTER_FIN(self, t):
        message = "String contains escaped null character." if "\\\x00" in t.value else "String contains null character."
        return self._set_error(t, message)

    @_(r'\\\r\n')
    def SALTO_LINEA_EXTRANHO(self, t):
        
        self._contador += 2
        self.lineno += 1
        self._caracteres += r"\n"
        
    @_(r"\n")
    def SALTO_LINEA(self, t):
        message = "Unterminated string constant"
        self.lineno += 1
        self._contador += 1
        
        return self._set_error(t, message)

    @_(r".")
    def CAR(self, t):
        self._contador += 1
        if t.value in CoolLexer.CARACTERES_CONTROL:
            octal = oct(ord(t.value)).replace("o", "0")[-3:]
            self._caracteres += "\\" + octal
        else:
            self._caracteres += t.value

    def error(self, t):
        print(f"ERROR en linea {t.lineno} por {t.value}\n")



class Comments(Lexer):
    tokens = {}

    def __init__(self):
        self.profundidad = 1
        self.lineno = 1

    # Comentario que se abre con (**)
    @_(r"\n?\(\*\*\)")
    def COMMENTOPEN(self, t):
        pass  # Se ignora el marcador de apertura especial

    # Comentario que cierra incorrectamente (sin apertura o mal balanceado)
    @_(r"[^\\]\*\)$")
    def ERROR(self, t):
        self.profundidad -= 1
        if self.profundidad == 0:
            self.profundidad = 1
            self.begin(CoolLexer)
        else:
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            self.begin(CoolLexer)
            return t

    # Captura cualquier carácter hasta el fin del archivo sin cerrar el comentario
    @_(r"(.|\n)$")
    def ERROR2(self, t):
        self.lineno += t.value.count("\n")
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        self.begin(CoolLexer)
        return t

    # Comentario bien cerrado
    @_(r"[^\\]\*\)")
    def INSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad -= 1
        if self.profundidad == 0:
            self.profundidad = 1
            self.begin(CoolLexer)

    # Comentario anidado (abre uno nuevo)
    @_(r"[^\\]\(\*")
    def OUTSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad += 1

    # Contador de líneas
    @_(r"\n")
    def newline(self, t):
        self.lineno += 1

    # Todo lo demás dentro del comentario
    @_(r".")
    def EAT(self, t):
        pass

    def salida(self, texto):
        return ['#1 ERROR "EOF in string constant"']


class CoolLexer(Lexer):
    tokens = {
        OBJECTID, INT_CONST, BOOL_CONST, TYPEID, STR_CONST,
        ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS, INHERITS,
        ISVOID, LET, LOOP, NEW, OF, POOL, WHILE, LE, DARROW, ASSIGN
    }

    _key_words = {
        "else", "if", "fi", "then", "not", "in", "case", "esac",
        "class", "inherits", "isvoid", "let", "loop", "new",
        "of", "pool", "while"
    }

    literals = {
        "=", "+", "-", "*", "/", "(", ")", "<", ">", ".", "~",
        ",", ";", ":", "@", "{", "}"
    }

    # Regular expressions for multi-character operators
    LE = r"<="
    DARROW = r"=>"
    ASSIGN = r"<-"

    # Control characters
    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode("ascii")
        for i in ["0", "1"] for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    # String handling
    @_(r'"')
    def STR_CONST(self, t):
        self.begin(Strings)
        # print(f"Se está leyendo el caracter: {t.value}")

    # Error for invalid characters
    @_(r"[!#$%^&_>\?`\[\]\\\|\x00]")
    def ERROR2(self, t):
        t.type = "ERROR"
        if t.value == "\\":
            t.value = "\\\\"
        elif t.value in self.CARACTERES_CONTROL:
            ascii_code = int(t.value.encode("ascii").hex(), 16)
            t.value = "\\" + oct(ascii_code).replace("o", "0")[-3:]
        t.value = f'"{t.value}"'
        return t

    # Comments
    @_(r"\(\*\*\)")
    def COMMENT0(self, t):
        pass

    @_(r"\(\*$")
    def ERROR7(self, t):
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        return t

    @_(r"\(\*")
    def COMMENT(self, t):
        Comments.profundidad = 1
        self.begin(Comments)

    @_(r"\*\)")
    def ERRORCIERRE(self, t):
        t.type = "ERROR"
        t.value = '"Unmatched *)"'
        return t

    @_(r"--.*(\n|$)")
    def LINECOMMENT(self, t):
        self.lineno += t.value.count("\n")

    # Tokens
    @_(r"\d+")
    def INT_CONST(self, t):
        t.value = int(t.value)
        return t

    @_(r"\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b")
    def BOOL_CONST(self, t):
        t.value = t.value.lower() == "true"
        return t

    @_(r"[A-Z][a-zA-Z0-9_]*")
    def TYPEID(self, t):
        lowered = t.value.lower()
        if lowered in self._key_words:
            t.type = t.value.upper()
        return t

    @_(r"[a-z_][a-zA-Z0-9_]*")
    def OBJECTID(self, t):
        lowered = t.value.lower()
        if lowered in self._key_words:
            t.type = t.value.upper()
        return t

    @_(r"\t| |\v|\r|\f")
    def spaces(self, t):
        pass

    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    # Error handler
    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1

    # Output formatting
    def salida(self, texto):
        output = []
        lexer = CoolLexer()
        for token in lexer.tokenize(texto):
            line = f"#{token.lineno} {token.type}"

            if token.type == "OBJECTID":
                line += f" {token.value}"
            elif token.type == "TYPEID":
                line += f" {token.value}"
            elif token.type == "BOOL_CONST":
                line += " true" if token.value else " false"
            elif token.type == "STR_CONST":
                line += f" {token.value}"
            elif token.type == "INT_CONST":
                line += f" {token.value}"
            elif token.type == "ERROR":
                line += f" {token.value}"
            elif token.type in self.literals:
                line = f"#{token.lineno} '{token.type}'"

            output.append(line)
        return output
