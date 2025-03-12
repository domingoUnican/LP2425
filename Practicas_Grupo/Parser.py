# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

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

    @_("OBJECTID '=' expression")
    def asignation(self, p):
        return Asignacion(nombre=p[0], cuerpo=p[2])

    @_("expression '+' expression", "expression '-' expression")
    def expression(self, p):
        operador = p[1]
        if operador == '+':
            return Suma(izquierda=p[0], derecha=p[2])
        if operador == '-':
            return Resta(izquierda=p[0], derecha=p[2])
        

    @_("INT_CONST")
    def expression(self, p):
        return Entero(valor=p[0])
    

        
    


a = CoolLexer()
b = CoolParser()
aux = a.tokenize("a = 5")
#aux = a.tokenize("a = 5 + 5 - 2\na + 2")
# for i in aux:
#     print(i)
# print("\n->AUX (tokenizado)=", aux, "\n")
objecto = b.parse(aux)
print("\n->OBJECTO (parseado) = ", objecto, "\n")
print(objecto.str(0))







    
