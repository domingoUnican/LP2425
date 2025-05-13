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

    precedence = (
    ('left', '.'),          
    ('left', '@'),
    ('right', '~'),          
    ('right', 'ISVOID'),    
    ('left', '*', '/'), 
    ('left', '+', '-'),   
    ('nonassoc', 'LE', '<', '='),      
    ('right', 'NOT'),    
    ('right', 'ASSIGN') 
    )

    @_("clases")
    def programa(self, p):
        return Programa(secuencia=p[0])
    
    @_("clase")
    def clases(self, p):
        return [p[0]]

    @_("clases clase")
    def clases(self, p):
        p[0].append(p[1])
        return p[0]
    
    @_("CLASS TYPEID '{' caracteristicas '}' ';'")
    def clase(self, p):
        return Clase(nombre=p[1], caracteristicas=p[3], padre="Object", nombre_fichero=self.nombre_fichero)
    
    @_("CLASS TYPEID INHERITS TYPEID '{' caracteristicas '}' ';'")
    def clase(self, p):
        return Clase(nombre=p[1], padre=p[3], caracteristicas=p[5], nombre_fichero=self.nombre_fichero)
    
    @_("OBJECTID ':' TYPEID ASSIGN expression ';'")
    def caracteristica(self, p):
        return Atributo(nombre=p[0], tipo=p[2], cuerpo=p[4])
    
    @_("OBJECTID ':' TYPEID ';'")
    def caracteristica(self, p):
        return Atributo(nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    @_("OBJECTID '(' ')' ':' TYPEID '{' expression '}' ';'") 
    def caracteristica(self, p):
        return Metodo(nombre=p[0], tipo=p[4], cuerpo=p[6])

    @_("OBJECTID '(' formal ')' ':' TYPEID '{' expression '}' ';'")
    def caracteristica(self, p):
        return Metodo(nombre=p[0], formales=p[2] ,tipo=p[5], cuerpo=p[7])
    
    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expression '}' ';'")
    def caracteristica(self, p):
        return Metodo(nombre=p[0], formales=p[2] ,tipo=p[5], cuerpo=p[7])

    @_("caracteristica")
    def caracteristicas(self, p):
        return [p[0]]

    @_("caracteristicas caracteristica")
    def caracteristicas(self, p):
        p[0].append(p[1])
        return p[0]

    # ⟨Formal⟩ ::= OBJECTID : TYPEID
    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        return Formal(nombre_variable=p[0], tipo=p[2])
    
    @_("formal")
    def formales(self, p):
        return [p[0]]
    
    @_("formales ',' formal")
    def formales(self, p):
        p[0].append(p[1])
        return p[0]

    @_("OBJECTID ASSIGN expression")
    def expression(self, p):
        return Asignacion(nombre=p[0], cuerpo=p[2])

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
    
    @_("( expression )")
    def expression(self, p):
        return p[1]
    
    @_("NOT expression")
    def expression(self, p):
        return Not(p[1])
    
    @_("ISVOID expression")
    def expression(self, p):
        return  EsNulo(p[1])
    
    @_("'~' expression")
    def expression(self, p):
        return  Neg(p[1])
    
    @_("expression '@' TYPEID '.' OBJECTID '(' ')'") # () @ Tipo
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=[])

    @_("expression '@' TYPEID '.' OBJECTID '(' expressions ')'")
    def expression(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=p[6])
    
    @_("expression '.' OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[2] )
    
    @_("expression '.' OBJECTID '(' expressions ')'")
    def expression(self, p):
        return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[2], argumentos=p[4])
    
    @_("OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodo(nombre_metodo=p[0])
    
    @_("OBJECTID '(' expressions ')'")
    def expression(self, p):
        return LlamadaMetodo(nombre_metodo=p[0], argumentos=p[2])
    
    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])
    
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])
    
    # TODO: definir expresiones
    # TODO:
    # LET OBJECTID : TYPEID [<- ⟨Expresion⟩] (, OBJECTID : TYPEID [<- ⟨Expresion⟩])* IN ⟨Expresion⟩
    # LET OBJECTID : TYPEID [ASSIGN expression] (, OBJECTID : TYPEID [ASSIGN expression])* IN expression
    # LET OBJECTID : TYPEID [asignacion] (, declaracion [asignacion])* IN expression
    # ASSIGN expression = asignacion
    # , OBJECTID : TYPEID = declaracion
    # (, declaracion [asignacion]) = variables
    # LET variables IN expression
    # Los lets hay que hacerlos anidados si hay mas de una declaracion
    # es decir Let(nombre=p[], tipo=p[], cuerpo=Let(...)) hasta llegar al cuerpo real
    # recomendable empezar desde el caso del cuerpo real e ir hacia arriba

    # @_("LET OBJECTID : TYPEID IN expression")
    # def expression(self, p):
    #     return Let(nombre=p[1], tipo=p[3], cuerpo=p[5], inicializacion=NoExpr())

    @_("LET OBJECTID ':' TYPEID IN expression")
    def expression(self, p):
        return Let(nombre=p[1], tipo=p[3], cuerpo=p[5], inicializacion=NoExpr())
    
    @_("LET OBJECTID ':' TYPEID asignacion IN expression")
    def expression(self, p):
        return Let(nombre=p[1], tipo=p[3], cuerpo=p[6], inicializacion=p[4])

    @_("LET OBJECTID ':' TYPEID ',' variables IN expression")
    def expression(self, p):
        return Let(nombre=p[1], tipo=p[3], cuerpo=p[6], inicializacion=NoExpr())
    
    @_("LET OBJECTID ':' TYPEID asignacion ',' variables IN expression")
    def expression(self, p):
        return Let(nombre=p[1], tipo=p[3], cuerpo=p[5], inicializacion=p[4])
    
    @_("ASSIGN expression")
    def asignacion(self, p):
        return p[1]
    
    @_("OBJECTID ':' TYPEID")
    def variable(self, p):
        return [(p[0],p[2], NoExpr())]
    
    @_("variables OBJECTID ':' TYPEID")
    def variables(self, p):
        p[0].append((p[1],p[3], NoExpr()))
        return p[0]
    
    @_("OBJECTID ':' TYPEID asignacion")
    def variable(self, p):
        return [(p[0],p[2], p[3])]
    
    @_("variables OBJECTID ':' TYPEID asignacion")
    def variables(self, p):
        p[0].append((p[1],p[3], p[4]))
        return p[0]
    
    @_("variable ','")
    def variables(self, p):
        return p[0]

    # TODO: comprobar CASE y casos
    @_("CASE expression OF casos ';' ESAC")
    def expression(self, p):
        return Switch(expr=p[1], casos=p[3])
    
    @_("OBJECTID ':' TYPEID DARROW expression")
    def casos(self, p):
        return [RamaCase(nombre_variable=p[0], tipo=p[2], cuerpo=p[4])]
    
    @_("casos OBJECTID ':' TYPEID DARROW expression")
    def casos(self, p):
        #se lia porque no sabe el tipo de p y no esta seguro de si es una lista
        p[0].append(RamaCase(nombre_variable=p[1], tipo=p[3], cuerpo=p[5]))
        return p[0]

    @_("NEW TYPEID")
    def expression(self, p):
        return Nueva(tipo=p[1])
    
    @_("expression ';'")
    def expressions(self, p):
        return [p[0]]
    
    @_("expressions expression ';'")
    def expressions(self, p): 
        p[0].append(p[1])
        return p[0]

    @_("'{' expressions '}'")
    def expression(self, p):
        return Bloque(expresiones=p[1])
    
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
    
