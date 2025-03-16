# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    literals = CoolLexer.literals
    # reservados = CoolLexer._key_words
    debugfile = "salida.out"
    errores = []

    @_("INT_CONST")
    def expression(self, p):
        return Entero(valor=p[0])

    @_("STR_CONST")
    def expression(self, p):
        return String(valor=p[0])

    @_("BOOL_CONST")
    def expression(self, p):
        return Booleano(valor=p[0])

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

    @_("expression '<=' expression")
    def expression(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])
    
    @_("expression '=' expression")
    def expression(self, p):
        return Igual(izquierda=p[0], derecha=p[2])

    @_("'(' expresion ')'") 
    def expression(self, p):
        return p[0]

    @_("NOT expresion") 
    def expression(self, p):
        return Not(expr=p[0])
    
    @_("ISVOID expression")
    def expression(self, p):
        return EsNulo(expr=p[0])
    
    @_("'~' expression")
    def expression(self, p):
        return Neg(expr=p[0])
    
    @_("expresion @ TYPEID . OBJECTID ()")
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[3], argumentos=[])

    @_("expresion @ TYPEID . OBJECTID ( listExpresiones )")
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[3], argumentos=p[5])
    @_("expresion")
    def listExpresiones(self, p):
        return [p[0]]
    
    @_("listExpresion ',' expresion")
    def listExpresiones(self, p):
        return p[0]+[p[2]]   

    # @_("IF expresion THEN expresion ELSE expresion")
    # def expression(self, p):
    #     return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])

    # @_('WHILE expresion LOOP expresion POOL')
    # def expression(self, p):
    #     return Bucle(condicion=p[1], cuerpo=p[3])
    
a = CoolLexer()
b = CoolParser()
objecto = b.parse(a.tokenize("1+2+3"))
print(objecto.str(0))


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




# CON OPERACION BINARIA SE PUEDE HACER LO DE PONER MUCHAS JUNTAS