# coding: utf-8

from sly import Lexer


class CommentLexer(Lexer):
    """Lexer para comentarios.

    Se inicializa con profundidad = 1, indicando que hay un comentario abierto `(*` que
    debe ser cerrado. A medida que se encuentran nuevos inicios de comentario, la profundidad
    se incrementa en 1. Asimismo, a medida que se encuentran fines de comentario, esta se
    decrementa en 1, de forma que cuando llega a 0, se habran cerrado todos los comentarios.
    """

    tokens = {}
    profundidad = 1

    @_(r"\(\*\*\)")
    def comentario_vacio(self, t):
        """Si encontramos un comentario vacio `(**)`, lo ignoramos."""
        pass

    @_(r"([^\\]\*\))")
    def fin_comentario(self, t):
        """Si encontramos el fin de un comentario `*)`, cerramos ese comentario.

        Si todos los comentarios anidados estan cerrados (profundidad = 0),
        iniciamos el lexer de Cool.
        """
        self.lineno += t.value.count("\n")
        self.profundidad -= 1
        if self.profundidad == 0:
            self.profundidad = 1
            self.begin(CoolLexer)

    @_(r"[^\\]\(\*")
    def comentario_anidado(self, t):
        """Si encontramos el inicio de un comentario `(*`, abrimos ese comentario.

        Abrir un comentario significa incrementar la profundidad en 1, de modo que
        todos los comentarios anidados se tengan que cerrar en algun momento.
        """
        self.lineno += t.value.count("\n")
        self.profundidad += 1

    @_(r"\n+")
    def saltos_linea(self, t):
        """Si encontramos uno o mas saltos de linea, actualizamos el numero de linea."""
        self.lineno += t.value.count("\n")

    @_(r".")
    def cualquier_otro(self, t):
        """Si encontramos cualquier otro caracter, lo ignoramos."""
        pass


class StringLexer(Lexer):
    """Lexer para strings.

    Va leyendo caracteres hasta que encuentra las comillas de fin de string.
    """

    tokens = {ERROR, STR_CONST}
    _string = '"'
    _num_caracteres = 0
    _limite_caracteres = 1024

    @_(r'(\\\\)*"')
    def STR_CONST(self, t):
        """Si encontramos un numero par de barras invertidas seguidas de comillas `"`, cerramos el string.

        Si el numero caracteres no excede el limite, se genera el token y se vuelve al lexer de Cool.
        En caso contrario, se indica el error de que el string es demasiado largo.
        """
        self._num_caracteres *= (len(t.value) - 1) // 2
        if self._num_caracteres < self._limite_caracteres:
            self._string += t.value
            t.value = self._string
        else:
            t.value = '"String constant too long"'
            t.type = "ERROR"
        self._string = '"'
        self._num_caracteres = 0
        self.begin(CoolLexer)
        return t

    @_(r'\\[btnf"]')
    def secuencia_escape(self, t):
        """Si encontramos una secuencia de escape valida, la concatenamos con el string.

        Las secuencias de escape validas son:
          - backspace `\b`
          - tabulador `\t`
          - salto de linea `\n`
          - salto de pagina `\f`
          - comillas dobles `\"`
        """
        self._string += t.value
        self._num_caracteres += 1

    @_(r"\\\\[0-9a-zA-Z]")
    def barra_octal(self, t):
        """Si encontramos dos barras invertidas seguidas de un alfanum, la concatenamos con el string."""
        self._string += t.value
        self._num_caracteres += len(t.value)

    @_(r"\\[a-zA-Z0-9_]")
    def barra_alfanum(self, t):
        """Si encontramos una barra invertida seguida de un caracter alfanumerico, ignoramos la barra invertida.

        La regla general es que \c se sustituye por el caracter c, con la excepcion de las secuencias de escape
        mostradas en la regla de arriba.
        """
        self._string += t.value[-1]
        self._num_caracteres += 1

    @_(r"\t")
    def tabulador(self, t):
        """Si encontramos un tabulador `\t`, lo concatenamos al string en crudo `r'\t'`."""
        self._string += r"\t"
        self._num_caracteres += 1

    @_(r'[^"]$')
    def error_fin_fichero(self, t):
        """Si encontramos el caracter de fin de fichero `$`, indicamos el error."""
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        self.lineno += 1
        self._num_caracteres = 0
        self._string = '"'
        self.begin(CoolLexer)
        return t

    @_(r'.*\x00[^"]*"?')
    def error_caracter_nulo(self, t):
        """Si encontramos el caracter nulo `\0`, indicamos el error."""
        t.type = "ERROR"
        if "\\\x00" in t.value:
            t.value = '"String contains escaped null character."'
        else:
            t.value = '"String contains null character."'
        self._num_caracteres = 0
        self._string = '"'
        self.begin(CoolLexer)
        return t

    @_(r"\n")
    def salto_linea(self, t):
        """Si encontramos un salto de linea sin escapar, lo concatenamos con el string."""
        self._string = self._string.replace("\\0", "")
        self._string += "\\n"
        self._num_caracteres += 1
        self.lineno += 1

    @_(r"\\$")
    def barra_al_final(self, t):
        """Si encontramos una barra invertida al final del string, la convertimos en un salto de linea."""
        self._string = self._string[:-1]
        self._string += "\n"
        self._num_caracteres += 1

    @_(r".")
    def cualquier_otro(self, t):
        """Si encontramos cualquier otro caracter, lo concatenamos con el string."""
        self._num_caracteres += 1
        if t.value in CoolLexer.CARACTERES_CONTROL:
            self._string += self._a_octal(t.value)
        else:
            self._string += t.value

    @staticmethod
    def _a_octal(value):
        valor = "\\"
        valor += str(oct(int(value.encode("ascii").hex(), 16)).replace("o", "0"))
        return valor[-3]


class CoolLexer(Lexer):
    tokens = {
        # Enteros
        INT_CONST,
        # Identificadores de tipos
        TYPEID,
        # Identificadores de objetos
        OBJECTID,
        # Notacion especial
        LE,
        DARROW,
        ASSIGN,
        # Strings
        STR_CONST,
        # Palabras reservadas
        IF,
        FI,
        THEN,
        NOT,
        IN,
        CASE,
        ELSE,
        ESAC,
        CLASS,
        INHERITS,
        ISVOID,
        LET,
        LOOP,
        NEW,
        OF,
        POOL,
        THEN,
        WHILE,
        BOOL_CONST,
    }
    _key_words = {
        "else",
        "if",
        "fi",
        "then",
        "not",
        "in",
        "case",
        "esac",
        "class",
        "inherits",
        "isvoid",
        "let",
        "loop",
        "new",
        "of",
        "pool",
        "then",
        "while",
    }
    ignore = "\t "
    literals = {
        "=",
        "+",
        "-",
        "*",
        "/",
        "(",
        ")",
        "<",
        ".",
        "~",
        ",",
        ";",
        ":",
        "@",
        "{",
        "}",
    }

    LE = r"<="
    DARROW = r"=>"
    ASSIGN = r"<-"

    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode("ascii")
        for i in ["0", "1"]
        for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r'"')
    def STR_CONST(self, t):
        """Si encontramo el inicio de un string, iniciamos el lexer de strings."""
        self.begin(StringLexer)

    @_(r"\(\*\*\)")
    def comentario_vacio(self, t):
        """Si encontramos un comentario vacio `(**)`, lo ignoramos."""
        pass

    @_(r"\(\*")
    def inicio_comentario(self, t):
        """Si encontramos el inicio de un comentario `(*`, iniciamos el lexer de comentarios."""
        CommentLexer.profundidad = 1
        self.begin(CommentLexer)

    @_(r"\*\)")
    def error_fin_comentario(self, t):
        """Si encontramos el fin de un comentario `*)`, indicamos el error.

        No puede ser el fin comentario porque el metodo `inicio_comentario` garantiza que
        el comentario llega a su fin.
        """
        t.value = '"Unmatched *)"'
        t.type = "ERROR"
        return t

    @_(r"--.*(\n|$)")
    def comentario_simple(self, t):
        """Si encontramos un comentario simple `--`, lo ignoramos y actualizamos el numero de linea."""
        self.lineno += t.value.count("\n")

    @_(r"[0-9]+")
    def INT_CONST(self, t):
        """Si encontramos un numero entero, generamos el token INT_CONST."""
        t.value = t.value
        return t

    @_(r"\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b")
    def BOOL_CONST(self, t):
        """Si encontramos un booleano (true|false), generamos el token BOOL_CONST.

        Los booleanos empiezan por minuscula y el resto pueden ser tanto minusculas como mayusculas.
        """
        t.value = t.value[0] == "t"
        return t

    @_(r"_")
    def error_identificador_guion_bajo(self, t):
        """Si un identificador comienza con `_`, indicamos el error."""
        t.value = '"_"'
        t.type = "ERROR"
        return t

    @_(r"[A-Z][a-zA-Z0-9_]*")
    def TYPEID(self, t):
        """Si encontramos un identificador que empieza por mayuscula, generamos el token TYPEID."""
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r"[a-z_][a-zA-Z0-9_]*")
    def OBJECTID(self, t):
        """Si encontramos un identificador que empieza por minuscula, generamos el token OBJECTID."""
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r"\f|\r|\t|\v| ")
    def espacios(self, t):
        """Si encontramos un caracter en blanco o de control de cadena de texto, lo ignoramos.

        Los caracteres de control de cadena de texto son:
           - salto de pagina: `\f`,
           - retorno de carro `\r`,
           - tabulacion horizontal `\t`,
           - tabulacion vertical `\v`.
        """
        pass

    @_(r"\n+")
    def saltos_linea(self, t):
        """Si encontramos uno o mas saltos de linea, actualizamos el numero de linea."""
        self.lineno += t.value.count("\n")

    def error(self, t):
        """Si encontramos un caracter que no coincide con ninguna regla definida, lo devolvemos como error."""
        t.type = "ERROR"
        valor = repr(t.value[0])[1:-1]
        t.value = f'"{valor}"'
        t.lineno = self.lineno
        self.index += 1  # Avanza el índice para evitar bucles
        return t

    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f"#{token.lineno} {token.type} "
            if token.type == "OBJECTID":
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
