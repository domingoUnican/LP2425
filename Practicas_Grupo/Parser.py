# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens.union(CoolLexer.literals)
    debugfile = "salida.out"
    errores = []

    @_("NEW TYPEID")
    def expression(self, p):
        return Nueva(tipo=p[1])
    
    @_("OBJECTID")
    def expression(self, p):
        return Objeto(nombre=p[0])

    @_("INT_CONST")
    def expression(self, p):
        return Entero(valor=p[0])
    
    @_("STR_CONST")
    def expression(self, p):
        return String(valor=p[0])
    
    @_("BOOL_CONST")
    def expression(self, p):
        return Booleano(valor=p[0])
    
    @_("expression + expression")
    def expression(self, p):
        return Suma(izquierda=p[0], derecha=p[2])
    
    @_("expression - expression")
    def expression(self, p):
        return Resta(izquierda=p[0], derecha=p[2])
    
    @_("expression * expression")
    def expression(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])
    
    @_("expression / expression")
    def expression(self, p):
        return Division(izquierda=p[0], derecha=p[2])
    
    @_("expression < expression")
    def expression(self, p):
        return Menor(izquierda=p[0], derecha=p[2])
    
    @_("expression <= expression")
    def expression(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])
    
    @_("expression = expression")
    def expression(self, p):
        return Igual(izquierda=p[0], derecha=p[2])
    
    @_("( expression )")
    def expression(self, p):
        return p[1]
    
    @_("NOT expression )")
    def expression(self, p):
        return Not(p[1])
    
    @_("ISVOID expression )")
    def expression(self, p):
        return  EsNulo(p[1])
    
    @_("~ expression )")
    def expression(self, p):
        return  Neg(p[1])
    
    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])
    
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])
    
    @_("{ expressions }")
    def expression(self, p):
         #TODO: comprobar que no de problema el ; y que haya más de una expresion 
        return Bloque(expressions=p[1])
    
    @_("expression ;")
    def expressions(self, p):
        return [p[0]]
    
    @_("expressions expression ;")
    def expressions(self, p): 
         #se lia porque no sabe el tipo de p y no esta seguro de si es una lista
        p[0].append(p[1])
        return p[0]
    

    

a = CoolLexer()
b = CoolParser()
objeto = b.parse(a.tokenize("NEW INT"))
print(objeto.str(0))