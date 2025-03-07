# coding: utf-8

from sly import Lexer
import os
import re
import sys

# EL ORDEN EN EL QUE SE PONEN LAS FUNCIONES IMPORTA!!
# VA MIRANDO TAL CUAL EL ORDEN QUE SE PONE

# LOS ERRORES TIENE  QUE TENER EL NOMBRE Y TEXTO TAL CUAL

# COMO NO COINCIDA EL NUMERO DE LINEAS, DA ERROR


# ---------------------------------
#           Comentarios
# ---------------------------------
class Comentario(Lexer):
    tokens = {}  # no devuelve tokens porque queremos ignorar comentarios
    profundidad = 1

    # ERRORES QUE DICE EL PDF
    @_(r"[^\\]\*\)$")
    def ERROR_COMENTARIO_NO_CERRADO(self, t):
        """
        Maneja el cierre de comentarios anidados. Si se encuentra un comentario no cerrado,
        marca un error de "EOF en comentario" y vuelve al lexer.
        """
        self.profundidad -= 1

        # si estamos en profundidad 0 cuando llegamos al fin, se ha cerrado bien
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)

        # si no estamos en el final ahi si que es error
        else:
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            self.begin(CoolLexer)
            return t

    @_(r"(.|\n)$")
    def ERROR_FIN_ARCHIVO(self, t):
        """
        Maneja comentarios no cerrados al final del archivo y marca un error
        de "EOF en comentario".
        Cuenta todos los \n que haya de por medio y pone como linea del error
        la ultima linea de todas donde esta el error (si no se queda en la primera)
        """
        self.lineno += t.value.count("\n")
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        self.begin(CoolLexer)
        return t

    # GESTION COMENTARIOS
    @_(r"([^\\]\*\))")
    def CERRAR_COMENTARIO(self, t):
        """Detecta el cierre de un comentario *), evitando escapados
        Cuenta todos los \n porque puede haber varios entre medias del comentario
        """
        self.profundidad -= 1  # Reduce la profundidad de anidamiento
        self.lineno += t.value.count("\n")

        # Si ya no hay comentarios anidados, vuelve al lexer principal
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)

    @_(r"[^\\]\(\*")
    def ENTRAR_COMENTARIO(self, t):
        """Detecta la apertura de un comentario (*, evitando escapados
        Cuenta todos los \n porque puede haber varios entre medias del comentario
        """
        self.profundidad += 1  # Aumenta la profundidad de anidamiento
        self.lineno += t.value.count("\n")

    # COSAS QUE IGNORAR
    @_(r"\n")
    def NUEVA_LINEA(self, t):
        """Maneja nuevas líneas dentro de comentarios."""
        self.lineno += 1

    @_(r".")
    def PASAR(self, t):
        """Ignora cualquier otro carácter dentro del comentario."""
        pass


# ---------------------------------
#            Strings
# ---------------------------------
class Strings(Lexer):
    tokens = {ERROR, STR_CONST}  # tokens que puede devolver
    contador = 0

    # tiene que ser privada porque si no da error el lexer
    # dice que no pertenecen a ningun token y se raya por ser un string
    _caracteres = '"'

    # GESTION CARACTERES ESPECIALES
    @_(r"\t")
    def TABULACIONES(self, t):
        """
        Maneja tabulaciones dentro de una cadena.
        Almacena el carácter de tabulación como '\t' en la cadena.
        """
        self.contador += 1
        self._caracteres += r"\t"
        
    @_(r"\n")
    def SALTO_LINEA(self, t):
        """
        Maneja el caso en que una cadena de texto no se cierra antes de un salto de línea.
        Se genera un error de "Unterminated string constant".
        """
        self._caracteres = '"'  # Resetea la cadena parcial detectada.
        self.lineno += (
            1  # Incrementa el número de línea, ya que se encontró un salto de línea.
        )
        t.type = "ERROR"  # Marca el token como un error.
        t.value = '"Unterminated string constant"'  # Mensaje de error.
        t.lineno = self.lineno
        self.contador = 0  # Resetea el contador de caracteres procesados.
        self.begin(CoolLexer)  # Reinicia el lexer en su estado principal.
        return t

    # VAMOS LEYENDO EL STRING Y ACABAMOS
    @_(r'(\\\\)*"')
    def STR_CONST(self, t):
        """
        Maneja el cierre de una cadena de texto.
        - Si la cadena es menor a 1024 caracteres, la almacena normalmente.
        - Si supera los 1024 caracteres, genera un error "String constant too long".
        """
        if self.contador < 1024:
            self._caracteres += t.value  # Añade la cadena cerrada.
            t.value = self._caracteres  # Asigna el valor final de la cadena.
        else:
            t.value = '"String constant too long"'  # Mensaje de error.
            t.type = "ERROR"  # Define el token como error.

        self._caracteres = '"'  # Resetea la construcción de la cadena.
        self.contador = 0  # Reinicia el contador de caracteres.
        self.begin(CoolLexer)  # Reinicia el lexer en su estado principal.
        return t

    @_(r".")
    def CONSTRUIR_STRING(self, t):
        """Maneja la construcción de una cadena de caracteres."""
        self.contador += 1  # Incrementa el contador de caracteres procesados.
        self._caracteres += t.value


# ---------------------------------
#           Lexer de Cool
# ---------------------------------
class CoolLexer(Lexer):
    # Definición de los tokens para Cool. (aqui da igual el orden)
    tokens = {
        # Palabras clave del lenguaje Cool
        ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC,
        CLASS, INHERITS, ISVOID, LET, LOOP,
        NEW, OF, POOL, THEN, WHILE,

        # Cadenas de texto
        STR_CONST,  # Constantes de tipo string

        # Operadores y símbolos especiales
        LE,     # Operador <= (menor o igual)
        DARROW, # Flecha => (usada en case)
        ASSIGN,  # Operador <- (asignación)
       
        BOOL_CONST, # Constantes booleanas (true, false)
        INT_CONST,  # Constantes enteras (números)
        OBJECTID,   # Identificadores de variables o métodos en minúsculas
        TYPEID,     # Identificadores de tipos (nombres de clases, comienzan con mayúscula) 
        
        ERROR # token para los errores
    }

    # Lista de caracteres literales que el lexer reconoce directamente sin
    # asociarlos a un token específico.
    literals = {
        '=', '+', '-', '*', '/',  # Operadores matemáticos
        '(', ')',                 # Paréntesis para agrupaciones
        '<', '>',                 # Operadores relacionales
        '.', '~', ',', ';',       # Símbolos de sintaxis
        ':', '@', '{', '}'        # Otros símbolos usados en la gramática de Cool
    }

    # tiene que haber un ignore y luego ya los demas les pones el nombre con _
    # ignoramos todos los saltos especiales que existen
    ignore = " "
    ignore_tab = "\t"
    ignore_carriage = "\r"
    ignore_salto_pagina = "\f"
    ignore_salto_vertical = "\v"

    # ahora las definiciones de los tokens. EL ORDEN IMPORTA!!

    # Operadores y símbolos especiales
    LE = r"<="  # Operador <= (menor o igual)
    DARROW = r"=>"  # Flecha => (usada en case)
    ASSIGN = r"<-"  # Operador de asignación

    # Constantes y tipos
    INT_CONST = r"\d+"  # Constantes enteras (números)
    BOOL_CONST = r"\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b" # Constantes booleanas (true, false)
    STR_CONST = r'"'  # Constantes de tipo string (entre comillas dobles)

    # Identificadores (lo ultimo porque es muy general)
    OBJECTID = r"[a-z][A-Z0-9_a-z]*"  # Identificadores de variables o métodos en minúsculas
    TYPEID = r"[A-Z][a-zA-Z0-9_]*"  # Identificadores de tipos (nombres de clases, comienzan con mayúscula)

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                        for i in ['0', '1']
                        for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    # una vez definidos los tokens, se pueden definir las funciones que se encargan de manejar los tokens
    # para que hagan cosas especiales

    # ---------------------------------
    #        Manejo de Strings
    # ---------------------------------
    def STR_CONST(self, t):
        """Empieza un string"""
        self.begin(Strings)

    # ---------------------------------
    #     Manejo de tipos de datos en tokens
    # ---------------------------------
    def BOOL_CONST(self, t):
        """Convierte booleanos para que tengan la sintaxis correcta. (empezar en mayuscula)"""
        lower_val = t.value.lower()
        if lower_val == "true":
            t.value = True
        elif lower_val == "false":
            t.value = False
        return t

    def OBJECTID(self, t):
        """Convierte identificadores en palabras clave si corresponden."""
        if t.value.upper() in self.tokens:
            t.value = t.value.upper()
            t.type = t.value
        return t

    def TYPEID(self, t):
        """Convierte identificadores de tipo en palabras clave si corresponden."""
        if t.value.upper() in self.tokens:
            t.value = t.value.upper()
            t.type = t.value
        return t

    # ---------------------------------
    #      Manejo de Comentarios
    # ---------------------------------
    @_(r"\*\)")
    def ERROR_CIERRE_COMENTARIO(self, t):
        """Maneja errores de comentarios sin abrir."""
        t.value = '"Unmatched *)"'
        t.type = "ERROR"
        return t

    @_(r"\(\*")
    def EMPEZAR_COMENTARIO(self, t):
        """Cambia al modo de comentarios."""
        Comentario.profundidad = 1
        self.begin(Comentario)

    @_(r"--.*(\n|\Z)")
    def COMENTARIO_LINEA(self, t):
        """
        Ignora comentarios de una sola línea.
        Tiene en cuenta que acabe en final de linea o de fichero
        Se suman todos los \n que haya siempre entre medias (si no cuenta solo 1).
        """
        self.lineno += t.value.count("\n")

    # ---------------------------------
    #             Extras
    # ---------------------------------

    @_(r"\n")
    def NUEVA_LINEA(self, t):
        """para los saltos de linea (de uno en uno)"""
        self.lineno += 1

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
        # tiene que tener este formato justo para que lo detecten los tests
        print("Illegal character '%s'" % t.value[0])

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

        list_strings = []

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


# -------------------------------------------------------------------------------
# COSAS QUE FALTAN Y SON PARA COSAS DE GRADING (creo) NO DE MINIMOS


# EN COOL LEXER

#  @_(r'[!#$%^&_>\?`\[\]\\\|\x00]')
#     def ERROR2(self, t):
#         t.type = "ERROR"
#         if t.value == '\\':
#             t.value = '\\\\'
#         if t.value in self.CARACTERES_CONTROL:
#             t.value = '\\' + \
#                 str(oct(int(t.value.encode("ascii").hex(), 16)
#                         ).replace('o', '0')[-3:])
#         t.value = '"'+t.value+'"'
#         return t

#     @_(r'\(\*\*\)')
#     def COMMENT0(self, t):
#         pass
#     @_(r'\(\*$')
#     def ERROR7(self, t):
#         t.type = "ERROR"
#         t.value = '"EOF in comment"'
#         return t


# EN COMENTARIO

# def salida(self, texto):
#     return ['#1 ERROR "EOF in string constant"']

# @_(r'\n?\(\*\*\)')
# def COMMENTOPEN(self, t):
#     pass


# EN STRINGS

# def error(self, t):
#     print(f'ERROR en linea {t.lineno} por {t.value}\n')


# @_(r".")
# def CONSTRUIR_STRING_PRO(self, t):
#     """
#     Maneja la construcción de una cadena de caracteres, transformando
#     los caracteres de control en su representación octal.
#     """
#     self.contador += 1  # Incrementa el contador de caracteres procesados.
#     self._caracteres += t.value
#     if t.value in CoolLexer.CARACTERES_CONTROL:
#         # Convierte el carácter de control a su representación octal.
#         self._caracteres += (
#             "\\"
#             + str(oct(int(t.value.encode("ascii").hex(), 16))).replace("o", "0")[
#                 -3:
#             ]
#         )
#     else:
#         # Si no es un carácter de control, lo añade tal cual.
#         self._caracteres += t.value

# @_(r'.*\x00[^"]*"?')
# def CARACTER_FIN(self, t):
#     self._caracteres = '"'
#     t.type = "ERROR"
#     if '\\\x00' in t.value:
#         t.value = '"String contains escaped null character."'
#     else:
#         t.value = '"String contains null character."'
#     self.begin(CoolLexer)
#     return t


# @_(r'([^"]|(\\\n))$')
# def ERROR_FIN_FICHERO_3(self, t):
#     """
#     Maneja el final de archivo (EOF) dentro de una cadena sin cerrar.
#     Se genera un error de "EOF in string constant".
#     """
#     t.type = "ERROR"  # Marca el token como error.
#     t.value = '"EOF in string constant"'  # Mensaje de error.
#     self._caracteres = '"'  # Resetea la cadena en construcción.
#     self.begin(CoolLexer)  # Reinicia el lexer para continuar el análisis.
#     return t


# @_(r"\\\n$")
# def ERROR_FIN_FICHERO_2(self, t):
#     """
#     Maneja el caso donde un salto de línea escapado aparece justo antes del EOF.
#     Genera un error "EOF in string constant".
#     """
#     self.lineno += (
#         1  # Incrementa el número de línea, ya que detectó un salto de línea.
#     )
#     self._caracteres = '"'  # Resetea la construcción de la cadena.

#     t.type = "ERROR"  # Marca el token como error.
#     t.value = '"EOF in string constant"'  # Mensaje de error indicando que la cadena no se cerró.

#     self.contador = 0  # Resetea el contador de caracteres procesados.
#     self.begin(CoolLexer)  # Reinicia el lexer en su estado principal.
#     return t

# @_(r'\\"$')
# def ERROR_FIN_FICHERO(self, t):
#     """
#     Detecta una comilla escapada (`\"`) al final del archivo sin cerrar la cadena.
#     Genera un error "EOF in string constant".
#     """
#     self.lineno += 1  # Incrementa el número de línea.
#     self._caracteres = '"'  # Resetea la construcción de la cadena.

#     t.type = "ERROR"  # Marca el token como error.
#     t.value = '"EOF in string constant"'  # Mensaje de error.

#     self.contador = 0  # Reinicia el contador de caracteres.
#     self.begin(CoolLexer)  # Vuelve al lexer en su estado principal.
#     return t

# @_(r'\\\n')
# def ADD_LINE(self, t):
#     self.contador += 1
#     self.lineno += 1
#     self._caracteres += r'\n'


# @_(r"\\\w")
# def CARACTERES_ESCAPE_NO_CONOCIDOS(self, t):
#     """
#     Maneja caracteres de escape no reconocidos.
#     Se elimina la barra invertida y solo se mantiene el carácter siguiente.
#     """
#     self.contador += 1
#     self._caracteres += t.value[-1]  # Añade solo el carácter después de '\'.

# @_(r'\\[\\"ntbf]')
# def CARACTERES_ESCAPE_CONOCIDOS(self, t):
#     """
#     Maneja caracteres de escape válidos dentro de una cadena.
#     Agrega el carácter escapado a la cadena en construcción.
#     """
#     self.contador += 1  # Incrementa el contador de caracteres procesados.
#     self._caracteres += t.value  # Añade el carácter escapado a la cadena.


# @_(r"\n")
# def SALTO_LINEA(self, t):
#     """
#     Maneja el caso en que una cadena de texto no se cierra antes de un salto de línea.
#     Se genera un error de "Unterminated string constant".
#     """
#     self._caracteres = '"'  # Resetea la cadena parcial detectada.
#     self.lineno += (
#         1  # Incrementa el número de línea, ya que se encontró un salto de línea.
#     )
#     t.type = "ERROR"  # Marca el token como un error.
#     t.value = '"Unterminated string constant"'  # Mensaje de error.
#     self.contador = 0  # Resetea el contador de caracteres procesados.
#     self.begin(CoolLexer)  # Reinicia el lexer en su estado principal.
#     return t