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

    def error(self, p):
        #print("hola")
        if p:
            if p.type == p.value:
                error_message = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near \'{p.type}\''
            elif p.type == 'FI' or p.type == 'ELSE' or p.type == 'LE' or p.type == 'POOL' or p.type == 'LOOP':
                error_message = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type}'
            else:
                error_message = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type} = {p.value}'
            self.errores.append(error_message)
        else:
            error_message = f'"{self.nombre_fichero}", line 0: syntax error at or near EOF'
            self.errores.append(error_message)


    precedence = (
        ('left', 'ASSIGN'),
        ('left', 'IN'),
        ('left', 'NOT'),
        ('nonassoc', 'LE', '<', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'ISVOID'),
        ('left', '~'),
        ('left', '@'),
        ('left', '.')
    )

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia=[p.Clase])

    @_("Programa Clase")
    def Programa(self, p):
        p.Programa.secuencia.append(p.Clase)
        return p.Programa
    
    @_("CLASS TYPEID INHERITS TYPEID '{' serie_atr_met '}' ';'") 
    def Clase(self, p):
        return Clase(nombre=p.TYPEID0, padre=p.TYPEID1, caracteristicas=p.serie_atr_met, nombre_fichero=self.nombre_fichero)

    @_("CLASS TYPEID '{' serie_atr_met '}' ';'")
    def Clase(self, p):
        return Clase(nombre=p.TYPEID, padre="Object", caracteristicas=p.serie_atr_met, nombre_fichero=self.nombre_fichero)

    @_("serie_atr_met Atributo")
    def serie_atr_met(self, p):
        p.serie_atr_met.append(p.Atributo)
        return p.serie_atr_met

    @_("serie_atr_met Metodo")
    def serie_atr_met(self, p):
        p.serie_atr_met.append(p.Metodo)
        return p.serie_atr_met

    @_("Atributo")
    def serie_atr_met(self, p):
        return [p.Atributo]

    @_("Metodo")
    def serie_atr_met(self, p):
        return [p.Metodo]

    @_("OBJECTID ':' TYPEID ';'")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=NoExpr())
    
    @_("OBJECTID ':' error ';'")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID, cuerpo=NoExpr())

    @_("OBJECTID ':' TYPEID ASSIGN Expresion ';'")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion)

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion, formales=[])

    @_("OBJECTID '(' Parametros ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion, formales=p.Parametros)
    
    @_("OBJECTID '(' Parametros ')' ':' TYPEID '{' error '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, formales=p.Parametros)

    @_("Parametros ',' Formal")
    def Parametros(self, p):
        p.Parametros.append(p.Formal)
        return p.Parametros

    @_("Formal")
    def Parametros(self, p):
        return [p.Formal]
    
    @_("error")
    def Parametros(self, p):
        return []

    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        return Formal(nombre_variable=p.OBJECTID, tipo=p.TYPEID)

    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.Expresion)

    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return Resta(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return Multiplicacion(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return Division(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '<' Expresion")
    def Expresion(self, p):
        return Menor(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion LE Expresion")
    def Expresion(self, p):
        return LeIgual(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        return Igual(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("'(' Expresion ')' ")
    def Expresion(self, p):
        return p.Expresion

    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(expr=p.Expresion)

    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(expr=p.Expresion)

    @_("'~' Expresion")
    def Expresion(self, p):
        return Neg(expr=p.Expresion)

    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')' ")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p.Expresion, clase=p.TYPEID, nombre_metodo=p.OBJECTID, argumentos=[])

    @_("Expresion '@' TYPEID '.' OBJECTID '(' Expresions ')' ")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p.Expresion, clase=p.TYPEID, nombre_metodo=p.OBJECTID, argumentos=p.Expresions)

    @_("Expresions ',' Expresion")
    def Expresions(self, p):
        p.Expresions.append(p.Expresion)
        return p.Expresions

    @_("Expresion")
    def Expresions(self, p):
        return [p.Expresion]

    @_("Expresion '.' OBJECTID '(' Expresions ')' ")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=p.Expresion, nombre_metodo=p.OBJECTID, argumentos=p.Expresions)

    @_("OBJECTID '(' Expresions ')' ")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"), nombre_metodo=p.OBJECTID, argumentos=p.Expresions)

    @_("Expresion '.' OBJECTID '(' ')' ")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=p.Expresion, nombre_metodo=p.OBJECTID, argumentos=[])

    @_("OBJECTID '(' ')' ")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"), nombre_metodo=p.OBJECTID, argumentos=[])

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion=p.Expresion0, verdadero=p.Expresion1, falso=p.Expresion2)

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p.Expresion0, cuerpo=p.Expresion1)

    @_("LET OBJECTID ':' TYPEID Asignacion IN Expresion")
    def Expresion(self, p):

        temp = p.Expresion

        for objeto, tipo, inicializacion in p.Asignacion:
            temp = Let(nombre=objeto, tipo=tipo, inicializacion=inicializacion, cuerpo=temp)

        return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=NoExpr(), cuerpo=temp)
        
    @_("LET OBJECTID ':' TYPEID ASSIGN Expresion Asignacion IN Expresion")
    def Expresion(self, p):

        temp = p.Expresion1

        for objeto, tipo, inicializacion in p.Asignacion:
            temp = Let(nombre=objeto, tipo=tipo, inicializacion=inicializacion, cuerpo=temp)            

        return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=p.Expresion0, cuerpo=temp)
    
    @_("LET OBJECTID ':' TYPEID ASSIGN error Asignacion IN Expresion")
    def Expresion(self, p):

        temp = p.Expresion1

        for objeto, tipo, inicializacion in p.Asignacion:
            temp = Let(nombre=objeto, tipo=tipo, inicializacion=inicializacion, cuerpo=temp)            

        return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=NoExpr(), cuerpo=temp)
        
    @_("',' OBJECTID ':' TYPEID ASSIGN Expresion Asignacion")
    def Asignacion(self, p):
        p.Asignacion.append([p.OBJECTID, p.TYPEID, p.Expresion])
        return p.Asignacion

    @_("',' OBJECTID ':' TYPEID Asignacion")
    def Asignacion(self, p):
        p.Asignacion.append([p.OBJECTID, p.TYPEID, NoExpr()])
        return p.Asignacion

    @_("")
    def Asignacion(self, p):
        return []

    @_("CASE Expresion OF serie_when ESAC")
    def Expresion(self, p):
        return Swich(expr=p.Expresion, casos=p.serie_when)
    
    @_("CASE Expresion OF error ESAC")
    def Expresion(self, p):
        return Swich(expr=p.Expresion)

    @_("serie_when OBJECTID ':' TYPEID DARROW Expresion ';'")
    def serie_when(self, p):
        p.serie_when.append(RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion))
        return p.serie_when

    @_("OBJECTID ':' TYPEID DARROW Expresion ';'")
    def serie_when(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion)]

    @_("NEW TYPEID")
    def Expresion(self, p):
        return Nueva(tipo=p.TYPEID)

    @_("'{' secuencia '}'")
    def Expresion(self, p):
        p.secuencia.reverse()
        return Bloque(expresiones=p.secuencia)

    @_("Expresion ';' secuencia")
    def secuencia(self, p):
        p.secuencia.append(p.Expresion)
        return p.secuencia

    @_("Expresion ';'")
    def secuencia(self, p):
        return [p.Expresion]

    @_("error ';' secuencia")
    def secuencia(self, p):
        return []
    
    @_("error ';'")
    def secuencia(self, p):
        return []

    @_("OBJECTID")
    def Expresion(self, p):
        return Objeto(nombre=p.OBJECTID)

    @_("INT_CONST")
    def Expresion(self, p):
        return Entero(valor=p.INT_CONST)

    @_("STR_CONST")
    def Expresion(self, p):
        return String(valor=p.STR_CONST)

    @_("BOOL_CONST")
    def Expresion(self, p):
        if p.BOOL_CONST:
            return Booleano(valor=True)
        elif p.BOOL_CONST:
            return Booleano(valor=False)
        else:
            return Booleano(valor=p.BOOL_CONST)

lexer = CoolLexer()
parser = CoolParser()
tkns = lexer.tokenize(r"""
class Test {
  foo:Test;
  bar():Int {x=y=z};
};
""")
#print("Tokens:")
#txt1 = lexer.tokenize(r'str="Hola nicolas"')
#for tk in tkns:
#    print(tk)
#print("Fin de los tokens")
#objeto = parser.parse(tkns)
#print(objeto)
#print(objeto.__dict__)
