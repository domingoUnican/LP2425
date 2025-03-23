# coding: utf-8

from sly import Lexer
import os
import re
import sys


class Comentario(Lexer):
    tokens = {}
    profundidad = 1

    @_(r"\(\*")
    def OPEN_COMMENT(self, t):
        self.profundidad += 1

    @_(r"\n")
    def LINEA(self, t):
        self.lineno += 1

    @_(r"\*\)")
    def VOLVER(self, t):
        if self.profundidad == 1:
            self.begin(CoolLexer)
        else:
            self.profundidad -= 1

    @_(r".")
    def PASAR(self, t):
        pass


class CoolLexer(Lexer):
    tokens = {
        OBJECTID,
        INT_CONST,
        BOOL_CONST,
        TYPEID,
        ELSE,
        IF,
        FI,
        THEN,
        NOT,
        IN,
        CASE,
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
        STR_CONST,
        LE,
        DARROW,
        ASSIGN,
    }

    _key_words = (
        "if",
        "fi",
        "then",
        "not",
        "in",
        "case",
        "else",
        "esac",
        "class",
        "inherits",
        "is" "void",
        "let",
        "loop",
        "new",
        "of",
        "pool",
        "then",
        "while",
        "true",
        "false",
    )
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
        ">",
        ".",
        "~",
        ",",
        ";",
        ":",
        "@",
        "{",
        "}",
    }

    ELSE = r"\b[eE][lL][sS][eE]\b"
    STR_CONST = r'"[a-zA-Z0-9_/]*"'

    @_(r"--.*\n")
    def SIMPLE_COMMENT(self, t):
        t.type = "COMMENT"

    @_(r"\*\)")
    def COMMENT_ERROR(self, t):
        t.value = '"Unmatched *)"'
        t.type = "ERROR"
        return t

    @_(r"\(\*")
    def COMMENT(self, t):
        t.type = "COMMENT"
        Comentario.profundidad = 1
        self.begin(Comentario)

    @_(r"\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b")
    def BOOL_CONST(self, t):
        t.type = "BOOL_CONST"
        return t

    @_(r"[A-Z][a-zA-Z0-9_]*")
    def TYPEID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r"[a-z_][a-zA-Z0-9_]*")
    def OBJECTID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r"\d+")
    def INT_CONST(self, t):
        t.type = "INT_CONST"
        return t

    @_(r"\r|\n")
    def LINEBREAK(self, t):
        self.lineno += 1

    @_(r"\b[wW][hH][iI][lL][eE]\b")
    def WHILE(self, t):
        t.value = (t.value) + "dddd"
        return t

    @_(r".")
    def ERROR(self, t):
        if t.value in self.literals:
            t.type = t.value
        return t

    def error(self, t):
        self.index += 1

    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode("ascii")
        for i in ["0", "1"]
        for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r"\(\*")
    def IR(self, t):
        self.begin(Comentario)

    def error(self, t):
        self.index += 1

    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            # list_strings.append("\t")
            result = f"#{token.lineno} {token.type} "
            if token.type == "OBJECTID":
                result += f"{token.value}"
            elif token.type == "BOOL_CONST":
                result += "true" if token.value else "false"
            elif token.type == "TYPEID":
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f"#{token.lineno} '{token.type}'"
            elif token.type == "STR_CONST":
                result += token.value
            elif token.type == "INT_CONST":
                result += str(token.value)
            elif token.type == "ERROR":
                result = f"#{token.lineno} {token.type} {token.value}"
            else:
                result = f"#{token.lineno} {token.type}"
            list_strings.append(result)
        return list_strings


if 0:
    texto = """
    -- (* This isn't
    what the programmer thought it was *) 
    .
    (* -- neither is this *) if 5 then

    """

    a = CoolLexer()
    for i in a.tokenize(texto):
        print(i)
