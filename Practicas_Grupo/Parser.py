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

    #TODO: OBJECTID ASSIGN ⟨Expresion⟩
    @_("OBJECTID ASSIGN expression")
    def expression(self, p):
        return Asignacion(identificador=p[0], expresion=p[2])

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
    
    #TODO:  ⟨Expresion⟩ @ TYPEID . OBJECTID ( )

    #TODO: ⟨Expresion⟩ @ TYPEID . OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )

    #TODO: [ ⟨Expresion⟩ .] OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    
    #TODO: [ ⟨Expresion⟩ .] OBJECTID ( )
    # @_("OBJECTID ( )")
    # def expression(self, p):
    #     return LlamadaMetodo()

    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])
    
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])
    
    # TODO: LET OBJECTID : TYPEID [<- ⟨Expresion⟩] (, OBJECTID : TYPEID [<- ⟨Expresion⟩])* IN ⟨Expresion⟩
    # def expression(self, p):
    #     return Let(nombre=p[1], tipo=p[3], inicializacion=p[], cuerpo=p[])

    # TODO: CASE ⟨Expresion⟩ OF (OBJECTID : TYPEID DARROW <Expresion>)+ ; ESAC

    @_("NEW TYPEID")
    def expression(self, p):
        return Nueva(tipo=p[1])
    
    @_("expression ;")
    def expressions(self, p):
        return [p[0]]
    
    @_("expressions expression ;")
    def expressions(self, p): 
        #se lia porque no sabe el tipo de p y no esta seguro de si es una lista
        p[0].append(p[1])
        return p[0]

    @_("{ expressions }")
    def expression(self, p):
        return Bloque(expressions=p[1])
    

a = CoolLexer()
b = CoolParser()
objeto = b.parse(a.tokenize("{ 1 + 2; 3 + 4; }"))
print(objeto.str(0))