# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ""
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

    # Definir precedencia para eliminar conflictos shift/reduce
    # resolviendo la ambigüedad, especialmente en gramáticas de
    # expresión.
    precedence = (
        ("left", "NOT"),
        ("left", "LE", "<", "="),
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("left", "ISVOID"),
        ("left", "~"),
        ("left", "@"),
        ("left", "."),
    )

    @_("INT_CONST")
    def expression(self, p):
        return Entero(valor=p[0])

    @_("STR_CONST")
    def expression(self, p):
        return String(valor=p[0])

    @_("BOOL_CONST")
    def expression(self, p):
        return Booleano(valor=p[0])

    @_("OBJECTID")
    def expression(self, p):
        return Objeto(nombre=p[0])

    @_("expression '+' expression")
    def expression(self, p):
        return Suma(izquierda=p[0], derecha=p[2])
    
    @_("expression '-' expression")
    def expression(self, p):
        return Resta(izquierda=p[0], derecha=p[2])

    @_("expression '*' expression")
    def expression(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])

    @_("expression '/' expression")
    def expression(self, p):
        return Division(izquierda=p[0], derecha=p[2])

    @_("expression '<' expression")
    def expression(self, p):
        return Menor(izquierda=p[0], derecha=p[2])

    @_("expression LE expression")
    def expression(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])
    
    @_("expression '=' expression")
    def expression(self, p):
        return Igual(izquierda=p[0], derecha=p[2])

    @_("'(' expression ')'") 
    def expression(self, p):
        return p[1]

    @_("NOT expression") 
    def expression(self, p):
        return Not(expr=p[1])
    
    @_("ISVOID expression")
    def expression(self, p):
        return EsNulo(expr=p[1])
    
    @_("'~' expression")
    def expression(self, p):
        return Neg(expr=p[1])
    
    @_("expression '@' TYPEID '.' OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=[])

    @_("expression '@' TYPEID '.' OBJECTID '(' listExpresiones ')'")
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=p[6])
    
    @_("expression")
    def listExpresiones(self, p):
        return [p[0]]
    
    @_("listExpresiones ',' expression")
    def listExpresiones(self, p):
        return p[0]+[p[2]]   
    
    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])

    @_('WHILE expression LOOP expression POOL')
    def expression(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])

    # Regla para la expresión let
    @_("LET let_list IN expression")
    def expression(self, p):
        # Se transforma la lista de declaraciones en Let anidados.
        result = p.expression
        for decl in reversed(p.let_list):
            decl.cuerpo = result
            result = decl
        return result

    # Regla para la lista de declaraciones let (uno o más)
    @_("let_list ',' let_decl")
    def let_list(self, p):
        return p.let_list + [p.let_decl]

    @_("let_decl")
    def let_list(self, p):
        return [p.let_decl]

    # Regla para una declaración let sin asignación
    @_("OBJECTID ':' TYPEID")
    def let_decl(self, p):
        # Se utiliza NoExpr() para representar la ausencia de inicialización.
        return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=NoExpr(), cuerpo=None)

    # Regla para una declaración let con asignación
    @_("OBJECTID ':' TYPEID ASSIGN expression")
    def let_decl(self, p):
        return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=p.expression, cuerpo=None)

     
    @_('CASE expression OF darrowlist ESAC')
    def expression(self, p):
        return Swicht(linea=p.lineno, expr=p.expression , casos=p.darrowlist)
    
    @_('OBJECTID ":" TYPEID DARROW expression')
    def darrowlist(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expression)]
    
    @_('OBJECTID ":" TYPEID DARROW expression darrowlist')
    def darrowlist(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expression)]+p.darrowlist
    
    @_("NEW TYPEID")
    def expr(self, p):
        """Creación de una nueva instancia del tipo especificado."""
        return Nueva(linea=p.lineno, tipo=p.TYPEID)
    


    
    # @_("NEW TYPEID '{' listExpresiones '}'")
    # def expression(self, p):
    #     return Nueva(clase=p[1], expresiones=p[3])


    
# PRUEBAS 
""" a = CoolLexer()
b = CoolParser()
objecto = b.parse(a.tokenize("1+2*3"))
print(objecto.str(0)) """

# Definir las expresiones a analizar
expressions = [
    '5',            # Entero
    '"verde"',      # String
    'true',         # Booleano
    '1+2*3',        # Suma y multiplicación
    '4-5/2',        # Resta y división
    '10<20',        # Menor que
    '30<=40',       # LeIgual
    '50=60',        # Igual
    '(false)',      # (expression)
    'NOT true',     # Not
    'isvoid 0',     # Es nulo
    '~5',           # Negación
    'obj@Tipo.metodo()',  # Llamada a método estático sin argumentos
    'obj@Tipo.metodo(1, 2, 3)',  # Llamada a método estático con argumentos
    'IF true THEN 1 ELSE 2 FI',  # Condicional
    'WHILE true LOOP 1 POOL',    # Bucle
    'CASE x OF y: int => 1; ESAC', 
    # Prueba para la expresión let
    'LET hello: String <- "Hello, ", name: String, ending: String <- "!\n" IN hello'
]

# Definir el lexer y el parser
lexer = CoolLexer()
parser = CoolParser()

# Iterar sobre las expresiones y analizarlas
for expr in expressions:
    print(f"Analizando expresión: {expr}")
    
    # Imprimir tokens generados por el lexer
    print("Tokens generados por el lexer:")
    for token in lexer.tokenize(expr):
        print(token)
    
    # Pasar los tokens al parser y comprobar si se puede parsear
    try:
        resultado = parser.parse(lexer.tokenize(expr))
        print("Resultado del parser:")
        print(resultado.str(0))
    
    # Capturar errores de parseo
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")




# @_("Clase ';'")
# def Programa(self, p):
#     pass


# @_("Programa Clase ';'")
# def Programa(self, p):
#     pass

# @_("CLASS TYPEID hereda '{'serie_atr_met '}'")
# def Clase(self, p):
#     pass

# @_("", "INHERITS TYPEID")
# def hereda(self, p):
#     pass

# @_("", "atributo", "metodo", "serie_atr_met atributo", "serie_atr_met metodo")
# def serie_atr_met(self, p):
#     pass
