# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    # Nombre del archivo que se está analizando (puede usarse para reportar errores)
    nombre_fichero = ""

    # Se importan las cosas de coolLexer
    tokens = CoolLexer.tokens
    literals = CoolLexer.literals

    # Archivo donde se guardará la salida de depuración
    debugfile = "salida.out"

    # Lista para almacenar errores sintácticos detectados
    errores = []

    # Reglas de precedencia para evitar conflictos shift/reduce y ambigüedades
    precedence = (
        ("left", "."),                # Llamada a método de instancia: obj.method()
        ("left", "@"),                # Llamada a método estático: obj@Type.method()
        ("left", "~"),                # Negación aritmética (unaria): ~e
        ("left", "ISVOID"),           # Verificación de nulo: isvoid e
        ("left", "*", "/"),           # Multiplicación y división
        ("left", "+", "-"),           # Suma y resta
        ("nonassoc", "LE", "<", "="), # Comparaciones: <=, <, =
        ("left", "NOT"),              # Negación lógica: not e
        ("right", "ASSIGN"),          # Asignación: x <- e
        ("left", "LET", "IN"),        # Expresiones let/in
        ("left", "DARROW")            # Flecha en case-of: => (más baja para evitar conflictos en CASE)
    )
    
    ######### PROGRAMA ###########
    @_("clases")
    def program(self, p):
        """Define el programa como una secuencia de clases."""
        return Programa(linea=0, secuencia=p.clases)

    @_("clase ';'")
    def clases(self, p):
        """Regla para una única clase."""
        return [p.clase]

    @_("clases clase ';'")
    def clases(self, p):
        """Regla para múltiples clases en secuencia."""
        p.clases.append(p.clase)
        return p.clases

    ######### CLASE ###########
    @_("CLASS TYPEID '{'  '}'")
    def clase(self, p):
        """Define una clase sin características, con un padre 'OBJECT'."""
        return Clase(
            linea=p.lineno,
            nombre=p.TYPEID,
            padre="OBJECT",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=[],
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def clase(self, p):
        """Define una clase con herencia de otro tipo (padre especificado)."""
        return Clase(
            linea=p.lineno,
            nombre=p.TYPEID0,
            padre=p.TYPEID1,
            nombre_fichero=self.nombre_fichero,
            caracteristicas=[],
        )

    @_("CLASS TYPEID '{' caracteristicas '}'")
    def clase(self, p):
        """Define una clase con características especificadas y un padre 'OBJECT'."""
        return Clase(
            linea=p.lineno,
            nombre=p.TYPEID,
            padre="OBJECT",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p.caracteristicas,
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' caracteristicas '}'")
    def clase(self, p):
        """Define una clase con herencia y características especificadas."""
        return Clase(
            linea=p.lineno,
            nombre=p.TYPEID0,
            padre=p.TYPEID1,
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p.caracteristicas,
        )

    ######### CARACTERISTICA (para atributo/metodo)###########
    @_("caracteristica ';'")
    def caracteristicas(self, p):
        """Añade una única característica a la lista."""
        return [p.caracteristica]

    @_("caracteristicas caracteristica ';'")
    def caracteristicas(self, p):
        """Añade una característica a la lista de características existentes."""
        lista_caracteristicas = p.caracteristicas
        lista_caracteristicas.append(p.caracteristica)
        return lista_caracteristicas

    ######### ATRIBUTO ###########
    @_("OBJECTID ':' TYPEID")
    def caracteristica(self, p):
        """Define un atributo sin valor asignado (solo tipo y nombre)."""
        return Atributo(
            linea=p.lineno, nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=NoExpr()
        )

    @_("OBJECTID ':' TYPEID ASSIGN expression")
    def caracteristica(self, p):
        """Define un atributo con un valor asignado."""
        return Atributo(
            linea=p.lineno, nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expression
        )

    ######### METODO ###########
    @_("OBJECTID '(' ')' ':' TYPEID '{' expression '}'")
    def caracteristica(self, p):
        """Define un método sin parámetros y con un cuerpo de expresión."""
        return Metodo(
            linea=p.lineno,
            nombre=p.OBJECTID,
            tipo=p.TYPEID,
            cuerpo=p.expression,
            formales=[],
        )

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expression '}'")
    def caracteristica(self, p):
        """Define un método con parámetros y con un cuerpo de expresión."""
        return Metodo(
            linea=p.lineno,
            nombre=p.OBJECTID,
            tipo=p.TYPEID,
            cuerpo=p.expression,
            formales=p.formales,
        )

    ######### FORMAL ###########
    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        """Define un formal con un nombre y tipo."""
        return Formal(linea=p.lineno, nombre_variable=p.OBJECTID, tipo=p.TYPEID)

    @_("formal ")
    def formales(self, p):
        """Devuelve una lista con un único parámetro formal."""
        return [p.formal]

    @_("formales ',' formal")
    def formales(self, p):
        """Añade un nuevo parámetro formal a la lista de parámetros existentes."""
        lista_formales = p.formales
        lista_formales.append(p.formal)
        return lista_formales

    ######### EXPRESION ###########
    @_("OBJECTID ASSIGN expression")
    def expression(self, p):
        """Define una asignación de una expresión a una variable."""
        return Asignacion(linea=p.lineno, nombre=p.OBJECTID, cuerpo=p.expression)

    # las operaciones binarias
    @_("expression '+' expression")
    def expression(self, p):
        """Suma de dos expresiones."""
        return Suma(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_("expression '-' expression")
    def expression(self, p):
        """Resta de dos expresiones."""
        return Resta(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_("expression '*' expression")
    def expression(self, p):
        """Multiplicación de dos expresiones."""
        return Multiplicacion(
            linea=p.lineno, izquierda=p.expression0, derecha=p.expression1
        )

    @_("expression '/' expression")
    def expression(self, p):
        """División de dos expresiones."""
        return Division(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_("expression '<' expression")
    def expression(self, p):
        """Comparación de menor que entre dos expresiones."""
        return Menor(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_("expression LE expression")
    def expression(self, p):
        """Comparación de menor o igual entre dos expresiones."""
        return LeIgual(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_("expression '=' expression")
    def expression(self, p):
        """Comparación de igualdad entre dos expresiones."""
        return Igual(linea=p.lineno, izquierda=p.expression0, derecha=p.expression1)

    @_('"(" expression ")"')
    def expression(self, p):
        """Expresión entre paréntesis."""
        return p.expression

    @_("NOT expression")
    def expression(self, p):
        """Negación de una expresión."""
        return Not(linea=p.lineno, expr=p.expression)

    @_("ISVOID expression")
    def expression(self, p):
        """Comprobación si una expresión es nula."""
        return EsNulo(linea=p.lineno, expr=p.expression)

    @_("NEW TYPEID")
    def expression(self, p):
        """Creación de una nueva instancia del tipo especificado."""
        return Nueva(linea=p.lineno, tipo=p.TYPEID)

    @_("'~' expression")
    def expression(self, p):
        """Negación a nivel de bit (operador ~) para una expresión."""
        return Neg(linea=p.lineno, expr=p.expression)

    # las mas complicadas, llamadas
    @_("expression '@' TYPEID '.' OBJECTID '(' ')'")
    def expression(self, p):
        """Llamada a un método estático sin parámetros."""
        return LlamadaMetodoEstatico(
            linea=p.lineno,
            cuerpo=p.expression,
            clase=p.TYPEID,
            nombre_metodo=p.OBJECTID,
            argumentos=[],
        )

    @_("expression '@' TYPEID '.' OBJECTID '(' parametros ')'")
    def expression(self, p):
        """Llamada a un método estático con parámetros."""
        return LlamadaMetodoEstatico(
            linea=p.lineno,
            cuerpo=p.expression,
            clase=p.TYPEID,
            nombre_metodo=p.OBJECTID,
            argumentos=p.parametros,
        )

    @_("expression '.' OBJECTID '(' ')'")
    def expression(self, p):
        """Llamada a un método de instancia sin parámetros."""
        return LlamadaMetodo(
            linea=p.lineno, cuerpo=p.expression, nombre_metodo=p.OBJECTID, argumentos=[]
        )

    @_("expression '.' OBJECTID '(' parametros ')'")
    def expression(self, p):
        """Llamada a un método de instancia con parámetros."""
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=p.expression,
            nombre_metodo=p.OBJECTID,
            argumentos=p.parametros,
        )

    @_("OBJECTID '(' ')'")
    def expression(self, p):
        """Llamada a un método sin receptor explícito (implícitamente `self`), sin parámetros."""
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p.OBJECTID,
            argumentos=[],
        )

    @_("OBJECTID '(' parametros ')'")
    def expression(self, p):
        """Llamada a un método sin receptor explícito (implícitamente `self`), con parámetros."""
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p.OBJECTID,
            argumentos=p.parametros,
        )

    # las ultimas simples
    @_("OBJECTID")
    def expression(self, p):
        """Identificador de objeto."""
        return Objeto(linea=p.lineno, nombre=p.OBJECTID)

    @_("INT_CONST")
    def expression(self, p):
        """Constante entera."""
        return Entero(linea=p.lineno, valor=p.INT_CONST)

    @_("STR_CONST")
    def expression(self, p):
        """Constante de tipo string."""
        return String(linea=p.lineno, valor=p.STR_CONST)

    @_("BOOL_CONST")
    def expression(self, p):
        """Constante booleana."""
        return Booleano(linea=p.lineno, valor=p.BOOL_CONST)

    # lista expresiones
    @_("expression ';'")
    def expressions(self, p):
        """Añade una única expresión a la lista de expresiones."""
        return [p.expression]

    @_("expressions expression ';'")
    def expressions(self, p):
        """Añade una expresión a la lista de expresiones existentes."""
        lista_expresiones = p.expressions
        lista_expresiones.append(p.expression)
        return lista_expresiones

    @_("'{' expressions '}'")
    def expression(self, p):
        """Define un bloque que contiene múltiples expresiones."""
        return Bloque(linea=p.lineno, expresiones=p.expressions)

    # lista parametros para poner en las llamadas a metodos
    @_("expression")
    def parametros(self, p):
        """Define una lista de parámetros con una única expresión."""
        return [p.expression]

    @_("parametros ',' expression")
    def parametros(self, p):
        """Añade una expresión a la lista de parámetros existente."""
        lista_param = p.parametros
        lista_param.append(p.expression)
        return lista_param

    # if
    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        """Define una estructura condicional `if-then-else`, que evalúa una condición y ejecuta una de dos expresiones según el resultado."""
        return Condicional(
            linea=p.lineno,
            condicion=p.expression0,
            verdadero=p.expression1,
            falso=p.expression2,
        )

    # let
    @_("LET let_list IN expression")
    def expression(self, p):
        """Regla para la expresión LET con lista de declaraciones y una expresión.
        Se anidan las declaraciones LET en orden inverso."""
        result = p.expression
        for decl in reversed(p.let_list):
            decl.cuerpo = result
            result = decl
        return result

    @_("let_list ',' let_decl")
    def let_list(self, p):
        """Regla para una lista de declaraciones LET separadas por comas."""
        return p.let_list + [p.let_decl]

    @_("let_decl")
    def let_list(self, p):
        """Regla para una lista de declaraciones LET con un solo elemento."""
        return [p.let_decl]

    @_("OBJECTID ':' TYPEID")
    def let_decl(self, p):
        """Regla para una declaración LET sin asignación."""
        return Let(
            nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=NoExpr(), cuerpo=None
        )

    @_("OBJECTID ':' TYPEID ASSIGN expression")
    def let_decl(self, p):
        """Regla para una declaración LET con asignación de valor inicial."""
        return Let(
            nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=p.expression, cuerpo=None
        )

    # while
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        """Define un bucle `while`, que ejecuta repetidamente una expresión mientras se cumpla la condición."""
        return Bucle(linea=p.lineno, condicion=p.expression0, cuerpo=p.expression1)

    # case
    @_("CASE expression OF darrowlist ESAC")
    def expression(self, p):
        """Define una estructura de control `case`, que evalúa una expresión y selecciona una de las ramas."""
        return Swicht(linea=p.lineno, expr=p.expression, casos=p.darrowlist)

    @_("OBJECTID ':' TYPEID DARROW expression ';'")
    def darrowlist(self, p):
        """Define una única rama en la lista de opciones de un `case`."""
        return [
            RamaCase(
                linea=p.lineno,
                nombre_variable=p.OBJECTID,
                tipo=p.TYPEID,
                cuerpo=p.expression,
            )
        ]

    @_("darrowlist OBJECTID ':' TYPEID DARROW expression ';'")
    def darrowlist(self, p):
        """Añade una nueva rama a la lista de opciones de un `case`."""
        lista = p.darrowlist
        lista.append(
            RamaCase(
                linea=p.lineno,
                nombre_variable=p.OBJECTID,
                tipo=p.TYPEID,
                cuerpo=p.expression,
            )
        )
        return lista
    
    ######### ERRORES ###########
    # Errores de tipo Clase
    @_("CLASS TYPEID '{' error '}'")
    def clase(self, p):
        """Regla para una clase con error en las características."""
        return Clase(
            linea = p.lineno, 
            nombre = p.TYPEID, 
            padre = 'OBJECT', 
            nombre_fichero = self.nombre_fichero, 
            caracteristicas = NoExpr())
    
    @_("CLASS TYPEID INHERITS TYPEID '{' error '}'")
    def clase(self, p):
        """Regla para una clase con error en las características y herencia."""
        return Clase(
            linea = p.lineno, 
            nombre = p.TYPEID0, 
            padre = p.TYPEID1, 
            nombre_fichero = self.nombre_fichero, 
            caracteristicas = NoExpr())

    
    def error(self, p):
        self.errores.append(f"Error{p}")

