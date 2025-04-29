# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens.union(CoolLexer.literals).union(CoolLexer.key_words).union(CoolLexer.ignore)
    debugfile = "salida.out"
    errores = []

    precedence = (
        ('right', 'ASSIGN'),
        ('left', 'NOT'),
        ('nonassoc', 'DARROW', '<', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'ISVOID'),
        ('left', '~'),
        ('left', '@'),
        ('left', '.'),
    )

    start = 'Programa'

    @_("Clase ';'")
    def Programa(self, p):
        return Programa(secuencia=[p[0]])

    @_("Programa Clase ';'")
    def Programa(self, p):
        return Programa(secuencia=p[0].secuencia + [p[1]])
    
    @_("CLASS TYPEID hereda '{' serie_atr_met '}' ") 
    def Clase(self, p):
        return Clase(nombre = p[1], nombre_fichero=self.nombre_fichero, padre = p[2], caracteristicas = p[4])

    @_("", "INHERITS TYPEID")
    def hereda(self, p):
        if len(p) == 0:
            return 'Object'
        return p[1]
        
    @_("", "serie_atr_met atributo ';' ", "serie_atr_met metodo ';' ")
    def serie_atr_met(self, p):
        if len(p) == 0:
            return []
        return p[0] + [p[1]]
    
    @_("OBJECTID ':' TYPEID ")
    def atributo(self, p):
        return Atributo(nombre = p[0], tipo = p[2], cuerpo= NoExpr())
    
    @_("OBJECTID '(' ')' ':' TYPEID '{' expresion '}' ")
    def metodo(self, p):
        return Metodo(nombre = p[0], tipo = p[4], cuerpo = p[6])
    
    @_("OBJECTID '(' formales formal ')' ':' TYPEID '{' expresion '}' ")
    def metodo(self, p):
        return Metodo(nombre = p[0], tipo = p[6], cuerpo = p[8], formales = p[2] + [p[3]])
    
    @_(" '{' expresiones2 '}' ")
    def expresion(self, p):
        return Bloque(expresiones= p[1])
    
    @_("formal ',' formales")
    def formales(self, p):
        return [p[0]] + p[2]
    
    @_(" ")
    def formales(self, p):
        return []

    @_("OBJECTID ':' TYPEID ")
    def formal(self, p):
        return Formal(nombre_variable= p[0], tipo = p[2])

    @_("INT_CONST")
    def expresion(self, p):
        return Entero(valor = p[0])
    
    @_("NEW TYPEID")
    def expresion(self, p):
        return Nueva(tipo = p[1])
        
    @_("OBJECTID")
    def expresion(self, p):
        return Objeto(nombre = p[0])
    
    @_("STR_CONST")
    def expresion(self, p):
        return String(valor = p[0])
    
    @_("BOOL_CONST")
    def expresion(self, p):
        return Booleano(valor = p[0])

    @_("OBJECTID ASSIGN expresion")
    def expresion(self, p):
        return Asignacion(nombre=p[0], cuerpo = p[2])

    @_("expresion + expresion")
    def expresion(self, p):
        return Suma(izquierda = p[0], derecha = p[2])
    
    @_("expresion - expresion")
    def expresion(self, p):
        return Resta(izquierda = p[0], derecha = p[2])
    
    @_("expresion '*' expresion")
    def expresion(self, p):
        return Multiplicacion(izquierda = p[0], derecha = p[2])

    @_("expresion '/' expresion")
    def expresion(self, p):
        return Division(izquierda = p[0], derecha = p[2])
    
    @_("expresion '<' expresion")
    def expresion(self, p):
        return Menor(izquierda = p[0], derecha = p[2])
    
    @_("expresion DARROW expresion")
    def expresion(self, p):
        return LeIgual(izquierda = p[0], derecha = p[2])
    
    @_("expresion '=' expresion")
    def expresion(self, p):
        return Igual(izquierda = p[0], derecha = p[2])
    
    @_(" '(' expresion ')' ")
    def expresion(self, p):
        return p[1]
    
    @_("NOT expresion")
    def expresion(self, p):
        return Not(expresion = p[1])
    
    @_("ISVOID expresion")
    def expresion(self, p):
        return EsNulo(expresion = p[1])
    
    @_(" '~' expresion")
    def expresion(self, p):
        return Neg(expresion = p[1])
    
    
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' ')' ")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase = p[2], nombre_metodo= p[5], argumentos=[])
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' expresiones ')' ")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase= p[2], nombre_metodo= p[5], argumentos= p[7])
    
    @_(" expresion '.' OBJECTID '(' expresiones ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0], nombre_metodo= p[2], argumentos= p[4])


    @_(" expresion '.' OBJECTID '(' ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0], nombre_metodo= p[2], argumentos=[])
    
    @_("IF expresion THEN expresion ELSE expresion FI")
    def expresion(self, p):
        return Condicional(condicion = p[1], entonces = p[3], sino = p[5])
    
    @_("WHILE expresion LOOP expresion POOL")
    def expresion(self, p):
        return Bucle(condicion = p[1], cuerpo = p[3])
    
    @_("LET OBJECTID ':' TYPEID expresiones IN expresion ") 
    def expresion(self, p):
        return Let(nombre = p[1], tipo = p[3], cuerpo = p[6], inicializacion= NoExpr())
    
    @_("CASE expresion OF '{' serie_when '}' ESAC")
    def expresion(self, p):
        return Swicht(expresion = p[1], serie_when = p[5])

    @_("serie_when when")
    def serie_when(self, p):
        return p[0] + [p[1]]
    
    @_(" ")
    def serie_when(self, p):
        return []
    
    @_("OBJECTID ':' TYPEID DARROW expresion ';'")
    def when(self, p):
        return RamaCase(variable = p[0], tipo = p[2], valor = p[4])
    
    @_(" expresion , expresiones ")
    def expresiones(self, p):
        return [p[0]] + p[2]
    
    @_(" expresion ';' expresiones2 ")
    def expresiones2(self, p):
        return [p[0]] + p[2]
    
    @_(" ")
    def expresiones(self, p):
        return []
    
    @_(" ")
    def expresiones2(self, p):
        return []
    

# a = CoolLexer()
# b = CoolParser()

# f = open(r'C:\Users\gopem\OneDrive\Escritorio\Estudios\Uni\Lenguajes de Programacion\Practicas\REPOSITORIO\LP2425\Practicas_Grupo\02\minimos\classonefield.test', 'r')
# objecto = b.parse(a.tokenize(f.read()))
# print(objecto.str(0))
# # for tok in a.tokenize(f.read()):
# #     print(tok)

    
