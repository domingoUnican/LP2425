# coding: utf-8
from nltk.corpus import nonbreaking_prefixes

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    keywords = CoolLexer._key_words
    literals = CoolLexer.literals
    debugfile = "salida.out"
    errores = []

    orden = (
        ('right', 'DARROW'),
        ('left', 'NOT'),
        #Porque una vida sin ti, una vida sin ti... No es una vida....
        ('nonassoc', 'LE', '<', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'ISVOID'),
        ('left', '~'),
        ('left', '@'),
        ('left', '.'),
    )

    @_('clases')
    def programa(self, p):
        return Programa(linea=0, secuencia=p.clases)

    @_("clase ','")
    def clases(self, p):
        return [p.clase]

    @_("clases clase ';'")
    def clases(self, p):
        return p.clases.append(p.clase)

    @_("CLASS TYPEID '{' '}'")
    def clase(self, p):
        return Clase(linea=p.lineno,
                     nombre=p.TYPEID,
                     padre='OBJECT',
                     nombre_fichero=self.nombre_fichero,
                     caracteristicas=[]
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1, nombre_fichero=self.nombre_fichero, caracteristicas=[])

    @_("CLASS TYPEID '{' componentes '}'")
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre='OBJECT', nombre_fichero=self.nombre_fichero, caracteristicas=p.componentes)

    @_("CLASS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre='OBJECT', nombre_fichero=self.nombre_fichero,
                     caracteristicas=NoExpr())

    @_("CLASS TYPEID INHERITS TYPEID '{' componentes '}'")
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1, nombre_fichero=self.nombre_fichero,
                     caracteristicas=p.componentes)

    @_("CLASS TYPEID INHERITS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1, nombre_fichero=self.nombre_fichero,
                     caracteristicas=NoExpr())



    @_("OBJECTID ASSIGN expression")
    def expression(self, p):
        return Asignacion(nombre=p[0], cuerpo=p[2])

    @_("expression '+' expression")
    def expression(self, p):
        print(p)
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
        pass #TODO

    @_("NOT expression")
    def expression(self, p):
        return Not(expr=p[1])

    @_("ISVOID expression")
    def expression(self, p):
        return EsNulo(expr=p[1])

    @_("'~' expression")
    def expression(self, p):
        return Neg(expr=p[1])

    #⟨Expresion⟩ @ TYPEID . OBJECTID ( )
    @_("expression '@' TYPEID '.' OBJECTID '(' ')'")
    def expression(self, p):
        pass #TODO

    # ⟨Expresion⟩ @ TYPEID . OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("expression '@' TYPEID '.' OBJECTID '(' (expression ',')* expression ')'")
    def expression(self, p):
        pass #TODO

    #[ ⟨Expresion⟩.] OBJECTID((⟨Expresion⟩,) * ⟨Expresion⟩ )
    @_("[expression '.'] OBJECTID '(' (expression ',')* expression ')'")
    def expression(self, p):
        pass #TODO

    #[ ⟨Expresion⟩.] OBJECTID()
    @_("[expression '.'] OBJECTID '(' ')'")
    def expression(self, p):
        pass #TODO



####IF ⟨Expresion⟩ THEN ⟨Expresion⟩ ELSE ⟨Expresion⟩ FI#   ######################################################
    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])

    @_('IF expression THEN error FI')
    def expression(self, p):
        return Condicional(condicion=p[1], verdadero=NoExpr(), falso=NoExpr())

    @_('IF error THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(condicion=NoExpr(), verdadero=p[3], falso=p[5])

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])
#################################################################################################################
    # WHILE ⟨Expresion⟩ LOOP ⟨Expresion⟩ POOL
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])

    @_('WHILE expression LOOP expression POOL')
    def expr(self, p):
        return Bucle(condicion=p.expr0, cuerpo=p.expr1)

    @_('WHILE error LOOP error POOL')
    def expr(self, p):
        return Bucle(condicion=NoExpr(), cuerpo=NoExpr())

    @_('WHILE error LOOP expression POOL')
    def expr(self, p):
        return Bucle(condicion=NoExpr(), cuerpo=p[3])

    @_('WHILE expression LOOP error POOL')
    def expr(self, p):
        return Bucle(condicion=p[1], cuerpo=NoExpr())



#################################################################################################################

    # LET OBJECTID: TYPEID[ < - ⟨Expresion⟩] (, OBJECTID: TYPEID[< - ⟨Expresion⟩]) * IN ⟨Expresion⟩
    @_("LET listaasignaciones IN expression ")
    def expression(self, p):
        lets = []
        temporal = p[3]
        for nombreVariable, tipoVariable, inicializacion in p[1]:
            temporal = Let(nombre=nombreVariable, tipo=tipoVariable, inicializacion = inicializacion, cuerpo = temporal)
            #lets.append(Let(nombre=asignacion[0], tipo=asignacion[1]))

        return temporal

    #nueva lista de asiganciones
    @_("OBJECTID ':' TYPEID")
    def listaasignaciones(self, p):
        lista = [(p[0], p[2], NoExpr)]
        return lista

    @_("OBJECTID ':' TYPEID ',' listaasignaciones")
    def listaasignaciones(self, p):
        return [(p[0], p[2], NoExpr())] + p[4]

    # CASE ⟨Expresion⟩ OF(OBJECTID: TYPEID DARROW < Expresion >)+; ESAC
    @_("CASE expression OF (OBJECTID ':' TYPEID DARROW expression)+ ESAC")
    def expression(self, p):
        #TODO
        return Swicht(expr=p[1])

    # NEW TYPEID
    @_("NEW TYPEID")
    def expression(self, p):
        return Nueva(tipo=p[1])

    # {(⟨Expresion⟩;) +}
    @_("'{' (expression)+ '}'")
    def expression(self, p):
        pass #TODO

    # OBJECTID
    @_("OBJECTID")
    def expression(self, p):
        return Objeto(nombre=p[0])

    # INT_CONST
    @_("INT_CONST")
    def expression(self, p):
        return Entero(valor=p[0])

    # STR_CONST
    @_("STR_CONST")
    def expression(self, p):
        return String(valor=p[0])

    # BOOL_CONST
    @_("BOOL_CONST")
    def expression(self, p):
        return Booleano(valor = p[0])


a = CoolLexer()
b = CoolParser()
with open("02\\minimos\\classonefield.test", "r") as f:
    txt = f.read()

txt = """class A {
  f(x : Int) : Object {
    let x : Int <- 3 in
      let y : Bool, z : Object in
        let a : Object, b : Object, c : Object in
          let d : Int <- 6 in
            d + 5
  };
};
"""
aux = a.tokenize(txt)
#print("aux=", aux)
objecto = b.parse(aux)
print("EEEY", objecto)
print(objecto.str(0))








