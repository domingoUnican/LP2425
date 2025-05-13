# coding: utf-8

from sly import Lexer
import os
import re
import sys

# ---------------------------------- Para los comentarios ------------------------------------

class Comentario(Lexer):
    tokens = {}

    @_(r"\n")
    def LINEA(self, t):
        self.lineno += 1

    @_(r"\*\)")
    def VOLVER(self, t):
        self.begin(CoolLexer)

    @_(r".")
    def PASAR(self, t):
        pass


# --------------------------------------------------------------------------------------------

# ---------------------------------- Para el lexer de Cool ------------------------------------


class CoolLexer(Lexer):
    # Definición de los tokens para Cool. (aqui da igual el orden)
    tokens = {
        # Palabras clave del lenguaje Cool
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
        # Cadenas de texto
        STR_CONST,  # Constantes de tipo string
        # Operadores y símbolos especiales
        LE,  # Operador <= (menor o igual)
        DARROW,  # Flecha => (usada en case)
        ASSIGN,  # Operador <- (asignación)
        BOOL_CONST,  # Constantes booleanas (true, false)
        INT_CONST,  # Constantes enteras (números)
        OBJECTID,  # Identificadores de variables o métodos en minúsculas
        TYPEID,  # Identificadores de tipos (nombres de clases, comienzan con mayúscula)
    }

    # Lista de caracteres literales que el lexer reconoce directamente sin asociarlos a un token específico.
    literals = {
        "=",
        "+",
        "-",
        "*",
        "/",  # Operadores matemáticos
        "(",
        ")",  # Paréntesis para agrupaciones
        "<",
        ">",  # Operadores relacionales
        ".",
        "~",
        ",",
        ";",  # Símbolos de sintaxis
        ":",
        "@",
        "{",
        "}",  # Otros símbolos usados en la gramática de Cool
    }

    # tiene que haber un ignore y luego ya los demas les pones el nombre con _
    ignore = " "
    ignore_tab = "\t"
    ignore_carriage = "\r"

    # ahora las definiciones de los tokens. EL ORDEN IMPORTA!!

    # Operadores y símbolos especiales
    LE = r"<="  # Operador <= (menor o igual)
    DARROW = r"=>"  # Flecha => (usada en case)
    ASSIGN = r"<-"  # Operador de asignación

    # Constantes y tipos
    INT_CONST = r"\d+"  # Constantes enteras (números)
    BOOL_CONST = (
        r"\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b"  # Constantes booleanas (true, false)
    )
    STR_CONST = r'"[a-zA-Z0-9_/]*"'  # Constantes de tipo string (entre comillas dobles)

    # Identificadores (lo ultimo porque es muy general)
    OBJECTID = r"\b[a-z][A-Z0-9_a-z]*\b"  # Identificadores de variables o métodos en minúsculas
    TYPEID = r"[A-Z][a-zA-Z0-9_]*"  # Identificadores de tipos (nombres de clases, comienzan con mayúscula)

    # una vez definidos los tokens, se pueden definir las funciones que se encargan de manejar los tokens
    # para que hagan cosas especiales

    def OBJECTID(self, t):
        if t.value.upper() in self.tokens:
            t.type = t.value.upper()
        return t

    def TYPEID(self, t):
        if t.value.upper() in self.tokens:
            t.type = t.value.upper()
        return t

    @_(r"--.*")
    def COMMENT1LINE(self, t):
        pass

    @_(r"\*\)")
    def COMMENTEND(self, t):
        t.value = '"Unmatched *)"'
        t.type = "ERROR"
        return t
    # Para ir a los comentarios de linea 
    
    # ------------------------------Cosas que no entiendo ---------------------------------------------
    @_(r"\n")
    def LINEBREAK(self, t):
        self.lineno += 1

    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode("ascii")
        for i in ["0", "1"]
        for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r"\(\*")
    def IR(self, t):
        self.begin(Comentario)

    # --------------------------------------------------------------------------------------------

    def error(self, t):
        """
        Maneja errores léxicos cuando se encuentra un carácter no reconocido.

        Parámetros:
        t (Token): Token que contiene el carácter ilegal encontrado.

        Descripcion:
        - Imprime un mensaje indicando el carácter ilegal y la línea en la que se encontró.
        - Avanza el índice de análisis léxico para evitar quedarse atascado en el error.
        """

        # Se imprime un mensaje indicando el carácter ilegal encontrado
        print(f"Error encontrado: '{t.value[0]}'")

        # Se avanza el índice del lexer para seguir analizando el texto
        self.index += 1

    def salida(self, texto):
        """
        Analiza el texto de entrada utilizando el lexer y genera una lista con
        la representación textual de los tokens encontrados.

        Parámetros:
        texto (str): Cadena de entrada que contiene el código a ser analizado.

        Retorna:
        list: Lista de strings, donde cada string representa un token en el
        formato '#<línea> <tipo> <valor>' o '#<línea> <tipo>' si no tiene valor.

        Descripción:
        - Utiliza la clase CoolLexer para tokenizar el texto de entrada.
        - Para cada token, genera una representación en formato de salida con:
            * Número de línea en la que aparece el token.
            * Tipo del token.
            * Valor del token si aplica (identificadores, constantes, cadenas, etc.).
        - Maneja errores detectados durante el análisis léxico.
        """

        list_strings = (
            []
        )  # Lista donde se almacenarán los tokens procesados como strings

        lexer = CoolLexer()  # Se crea una nueva instancia del analizador léxico

        # Se analiza el texto de entrada con el lexer
        for token in lexer.tokenize(texto):
            # Se comienza construyendo el string con el número de línea y el tipo de token
            result = f"#{token.lineno} {token.type} "

            # Si el token es un identificador de objeto, se agrega su valor
            if token.type == "OBJECTID":
                result += f"{token.value}"

            # Si el token es un booleano, se traduce el valor a "true" o "false"
            elif token.type == "BOOL_CONST":
                result += "true" if token.value else "false"

            # Si el token es un identificador de tipo, se agrega su valor como string
            elif token.type == "TYPEID":
                result += f"{str(token.value)}"

            # Si el token es un carácter literal (como '+', '-', etc.), se formatea de manera diferente
            elif token.type in self.literals:
                result = f"#{token.lineno} '{token.type}'"

            # Si el token es una cadena de texto, se agrega su valor
            elif token.type == "STR_CONST":
                result += token.value

            # Si el token es un número entero, se agrega su valor en formato string
            elif token.type == "INT_CONST":
                result += str(token.value)

            # Si el token es un error, se formatea de manera especial para mostrar el mensaje de error
            elif token.type == "ERROR":
                result = f"#{token.lineno} {token.type} {token.value}"

            # Para cualquier otro tipo de token, solo se incluye el número de línea y el tipo
            else:
                result = f"#{token.lineno} {token.type}"

            # Se agrega la representación del token a la lista de resultados
            list_strings.append(result)

        return list_strings  # Se devuelve la lista de tokens procesados como strings
