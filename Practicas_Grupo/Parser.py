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
        
    @_(" ", "serie_atr_met atributo ';' ", "serie_atr_met metodo ';' ")
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
    
    @_("OBJECTID '(' formal formales ')' ':' TYPEID '{' expresion '}' ")
    def metodo(self, p):
        return Metodo(nombre = p[0], tipo = p[6], cuerpo = p[8], formales = [p[2]] + p[3])
    
    @_(" '{' expresiones2 '}' ")
    def expresion(self, p):
        return Bloque(expresiones= p[1])
    
    @_("formales ',' formal")
    def formales(self, p):
        
        return p[0] + [p[2]]
    
    @_(" ")
    def formales(self, p):
        return []

    @_("OBJECTID ':' TYPEID ")
    def formal(self, p):
        return Formal(nombre_variable = p[0], tipo = p[2])

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

    @_("ASSIGN expresion")
    def expresion(self, p):
        return Asignacion(nombre=p[0], cuerpo = p[1])
    
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
        return Not(expr= p[1])
    
    @_("ISVOID expresion")
    def expresion(self, p):
        return EsNulo(expr = p[1])
    
    @_(" '~' expresion")
    def expresion(self, p):
        return Neg(expr= p[1])
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' ')' ")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase = p[2], nombre_metodo= p[4], argumentos=[])
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' expresiones ')' ")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase= p[2], nombre_metodo= p[4], argumentos= p[6])
    
    @_(" OBJECTID '(' expresiones ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= Objeto(nombre="self"), nombre_metodo= p[0], argumentos= p[2])

    @_(" expresion '.' OBJECTID '(' expresiones ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0], nombre_metodo= p[2], argumentos= p[4])

    @_(" OBJECTID '(' ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= Objeto(nombre="self"), nombre_metodo= p[0], argumentos=[])

    @_(" expresion '.' OBJECTID '(' ')' ")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0], nombre_metodo= p[2], argumentos=[])
    
    @_("IF expresion THEN expresion ELSE expresion FI")
    def expresion(self, p):
        return Condicional(condicion = p[1], verdadero = p[3], falso = p[5])
    
    @_("WHILE expresion LOOP expresion POOL")
    def expresion(self, p):
        return Bucle(condicion = p[1], cuerpo = p[3])
    
    @_("LET expresion3 expresiones IN expresion ") 
    def expresion(self, p):
        if len(p.expresiones) > 0:
            total = p[4]
            for nombre, tipo, inicializacion in p[2]:
                total = Let(nombre = nombre, tipo = tipo, cuerpo = total, inicializacion= inicializacion)

            nombre, tipo, inicializacion = p[1]
            return Let(nombre = nombre, tipo = tipo, cuerpo = total, inicializacion= inicializacion)
        else:
            nombre, tipo, inicializacion = p[1]
            return Let(nombre = nombre, tipo = tipo, cuerpo = p[4], inicializacion= inicializacion)
    
    @_("CASE expresion OF serie_when ESAC")
    def expresion(self, p):
        return Swicht(expr= p[1], casos= p[3])

    @_("serie_when when")
    def serie_when(self, p):
        return p[0] + [p[1]]
    
    @_(" ")
    def serie_when(self, p):
        return []
    
    @_("OBJECTID ':' TYPEID DARROW expresion ';'")
    def when(self, p):
        return RamaCase(nombre_variable= p[0], tipo = p[2], cuerpo = p[4])
    
    @_(" , expresion3 ")
    def expresiones(self, p):
        return [p[1]]

    @_(" expresiones , expresion3 ")
    def expresiones(self, p):
        return [p[2]] + p[0]
    
    @_(" expresiones , expresion ")
    def expresiones(self, p):
        return p[0] + [p[2]]
    
    @_(" expresion ")
    def expresiones(self, p):
        return [p[0]]
    
    @_(" expresion ';' expresiones2 ")
    def expresiones2(self, p):
        return [p[0]] + p[2]
    
    @_(" ")
    def expresiones(self, p):
        return []
    
    @_(" ")
    def expresiones2(self, p):
        return []
    
    @_(" OBJECTID ':' TYPEID")
    def expresion3(self, p):
        return p[0], p[2] , NoExpr()
    
    @_(" OBJECTID ':' TYPEID ASSIGN expresion")
    def expresion3(self, p):
        return p[0] , p[2], p[4]
    

# a = CoolLexer()
# b = CoolParser()

# f = open(r'C:\Users\gopem\OneDrive\Escritorio\Estudios\Uni\Lenguajes de Programacion\Practicas\REPOSITORIO\LP2425\Practicas_Grupo\02\minimos\classonefield.test', 'r')
# objecto = b.parse(a.tokenize(f.read()))
# print(objecto.str(0))
# # for tok in a.tokenize(f.read()):
# #     print(tok)

    
