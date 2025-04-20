# coding: utf-8
import os
import sys

from Clases import *
from Lexer import CoolLexer
from sly import Parser


class CoolParser(Parser):
    nombre_fichero = ""
    tokens = CoolLexer.tokens
    keywords = CoolLexer._key_words
    literals = CoolLexer.literals
    debugfile = "salida.out"
    errores = []

    orden = (
        ("right", "DARROW"),
        ("left", "NOT"),
        ("nonassoc", "LE", "<", "="),
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("left", "ISVOID"),
        ("left", "~"),
        ("left", "@"),
        ("left", "."),
    )

    # ini programa
    @_("clases")
    def programa(self, p):
        return Programa(linea=0, secuencia=p[0])

    # fin programa

    # ini clases
    @_("clase ';'")
    def clases(self, p):
        return [p[0]]

    @_("clases clase ';'")
    def clases(self, p):
        p[0].append(p[1])
        return p[0]

    @_("CLASS TYPEID '{' '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p.TYPEID,
            padre="OBJECT",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=[],
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre=p[3],
            nombre_fichero=self.nombre_fichero,
            caracteristicas=[],
        )

    @_("CLASS TYPEID '{' componentes '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre="OBJECT",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p[3],
        )

    @_("CLASS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre="OBJECT",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=NoExpr(),
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' componentes '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre=p[3],
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p.componentes,
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre=p[3],
            nombre_fichero=self.nombre_fichero,
            caracteristicas=NoExpr(),
        )

    # fin clases

    # ini componentes
    @_("componente ';'")
    def componentes(self, p):
        return [p[0]]

    @_("componentes componente ';'")
    def componentes(self, p):
        p[0].append(p[1])
        return p[0]

    @_("OBJECTID '(' ')' ':' TYPEID '{' expression '}'")
    def componente(self, p):
        return Metodo(linea=p.lineno, nombre=p[0], tipo=p[4], cuerpo=p[6], formales=[])

    @_("OBJECTID '(' ')' ':' TYPEID '{' error '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[4], cuerpo=NoExpr(), formales=[]
        )

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expression '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=p[7], formales=p[2]
        )

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' error '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=NoExpr(), formales=p[2]
        )

    @_("OBJECTID '(' error ')' ':' TYPEID '{' expression '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=p[7], formales=NoExpr()
        )

    @_("OBJECTID ':' TYPEID")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    @_("OBJECTID ':' TYPEID ASSIGN expression")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=p[4])

    @_("OBJECTID ':' TYPEID ASSIGN error")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    # fin componentes

    # ini formales
    @_("formal ")
    def formales(self, p):
        return [p[0]]

    @_("formales ',' formal")
    def formales(self, p):
        p[0].append(p[2])
        return p[0]

    @_('OBJECTID ":" TYPEID')
    def formal(self, p):
        return Formal(linea=p.lineno, nombre_variable=p[0], tipo=p[2])

    # fin formales

    # ini asignacion
    @_("OBJECTID ASSIGN expression")
    def expression(self, p):
        return Asignacion(linea=p.lineno, nombre=p[0], cuerpo=p[2])

    @_("OBJECTID ASSIGN error")
    def expression(self, p):
        return Asignacion(linea=p.lineno, nombre=p[0], cuerpo=NoExpr())

    # fin asignacion

    # ini llamada metodo
    @_("expression '.' OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodo(
            linea=p.lineno, cuerpo=p[0], nombre_metodo=p[2], argumentos=[]
        )

    @_("expression '@' TYPEID '.' OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodoEstatico(
            linea=p.lineno, cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=[]
        )

    @_("expression '.' OBJECTID '(' parametros ')'")
    def expression(self, p):
        return LlamadaMetodo(
            linea=p.lineno, cuerpo=p[0], nombre_metodo=p[2], argumentos=p[4]
        )

    @_("expression '@' TYPEID '.' OBJECTID '(' parametros ')'")
    def expression(self, p):
        return LlamadaMetodoEstatico(
            linea=p.lineno, cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=p[6]
        )

    @_("OBJECTID '(' ')'")
    def expression(self, p):
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p[0],
            argumentos=[],
        )

    @_("OBJECTID '(' parametros ')'")
    def expression(self, p):
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p[0],
            argumentos=p[2],
        )

    @_("expression")
    def parametros(self, p):
        return [p[0]]

    @_("parametros ',' expression")
    def parametros(self, p):
        p[0].append(p[2]).append(p[1])
        return p[0]

    # fin llamada metodo

    # ini condicionales
    @_("IF expression THEN error FI")
    def expression(self, p):
        return Condicional(
            linea=p.lineno, condicion=p[1], verdadero=NoExpr(), falso=NoExpr()
        )

    @_("IF error THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(
            linea=p.lineno, condicion=NoExpr(), verdadero=p[3], falso=p[5]
        )

    @_("IF expression THEN expression ELSE expression FI")
    def expression(self, p):
        return Condicional(linea=p.lineno, condicion=p[0], verdadero=p[1], falso=p[2])

    # fin condicionales

    # ini bucles
    @_("WHILE expression LOOP expression POOL")
    def expression(self, p):
        return Bucle(linea=p.lineno, condicion=p[1], cuerpo=p[3])

    @_("WHILE error LOOP error POOL")
    def expression(self, p):
        return Bucle(linea=p.lineno, condicion=NoExpr(), cuerpo=NoExpr())

    @_("WHILE error LOOP expression POOL")
    def expression(self, p):
        return Bucle(linea=p.lineno, condicion=NoExpr(), cuerpo=p[3])

    @_("WHILE expression LOOP error POOL")
    def expression(self, p):
        return Bucle(linea=p.lineno, condicion=p[1], cuerpo=NoExpr())

    # fin bucles

    # ini punto y coma
    @_("expression ';'")
    def expressions(self, p):
        return [p[0]]

    @_("expressions expression ';'")
    def expressions(self, p):
        p[0].append(p[1])
        return p[0]

    # fin punto y coma

    # ini bloque
    @_("'{' expressions '}'")
    def expression(self, p):
        return Bloque(linea=p.lineno, expresiones=p[1])

    # fin bloque

    # ini error
    @_("error ';'")
    def expressions(self, p):
        return []

    # fin error

    # ini let
    # LET OBJECTID: TYPEID[ < - ⟨Expresion⟩] (, OBJECTID: TYPEID[< - ⟨Expresion⟩]) * IN ⟨Expresion⟩
    @_("LET listaasignaciones IN expression ")
    def expression(self, p):
        lets = []
        temporal = p[3]
        for nombreVariable, tipoVariable, inicializacion in p[1]:
            temporal = Let(
                nombre=nombreVariable,
                tipo=tipoVariable,
                inicializacion=inicializacion,
                cuerpo=temporal,
            )
            # lets.append(Let(nombre=asignacion[0], tipo=asignacion[1]))

        return temporal

    # nueva lista de asiganciones
    @_("OBJECTID ':' TYPEID")
    def listaasignaciones(self, p):
        lista = [(p[0], p[2], NoExpr)]
        return lista

    @_("OBJECTID ':' TYPEID ',' listaasignaciones")
    def listaasignaciones(self, p):
        return [(p[0], p[2], NoExpr())] + p[4]

    # fin let

    # ini switch
    @_("CASE error OF darrowlist ESAC")
    def expression(self, p):
        return Swicht(linea=p.lineno, expr=NoExpr(), casos=p[3])

    @_("CASE expression OF error ESAC")
    def expression(self, p):
        return Swicht(linea=p.lineno, expr=p[1], casos=NoExpr())

    @_("CASE expression OF darrowlist ESAC")
    def expression(self, p):
        return Swicht(linea=p.lineno, expr=p[1], casos=p[3])

    @_('OBJECTID ":" TYPEID DARROW expression ";"')
    def darrowlist(self, p):
        return [RamaCase(linea=p.lineno, nombre_variable=p[0], tipo=p[2], cuerpo=p[4])]

    @_('OBJECTID ":" TYPEID DARROW error ";"')
    def darrowlist(self, p):
        return [
            RamaCase(linea=p.lineno, nombre_variable=p[0], tipo=p[2], cuerpo=NoExpr())
        ]

    @_('darrowlist OBJECTID ":" TYPEID DARROW expression ";"')
    def darrowlist(self, p):
        p[0].append(
            RamaCase(linea=p.lineno, nombre_variable=p[1], tipo=p[3], cuerpo=p[5])
        )
        return p[0]

    # fin switch

    # ini nueva
    @_("NEW TYPEID")
    def expression(self, p):
        return Nueva(linea=p.lineno, tipo=p[1])

    @_("error TYPEID")
    def expression(self, p):
        return Nueva(linea=p.lineno, tipo=p[1])

    # fin nueva

    # ini nulo
    @_("ISVOID expression")
    def expression(self, p):
        return EsNulo(linea=p.lineno, expr=p[1])

    @_("ISVOID error")
    def expression(self, p):
        return EsNulo(linea=p.lineno, expr=NoExpr())

    # fin nulo

    # ini operaciones aritmeticas
    @_("expression '+' expression")
    def expression(self, p):
        print(p)
        return Suma(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expression '-' expression")
    def expression(self, p):
        return Resta(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expression '*' expression")
    def expression(self, p):
        return Multiplicacion(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expression '/' expression")
    def expression(self, p):
        return Division(liena=p.lineno, izquierda=p[0], derecha=p[2])

    # fin operaciones aritmeticas

    # ini operaciones logicas
    @_("'~' expression")
    def expression(self, p):
        return Neg(linea=p.lineno, expr=p[1])

    @_("expression '<' expression")
    def expression(self, p):
        return Menor(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expression LE expression")
    def expression(self, p):
        return LeIgual(liena=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expression '=' expression")
    def expression(self, p):
        return Igual(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("NOT expression")
    def expression(self, p):
        return Not(liena=p.lineno, expr=p[1])

    @_("NOT error")
    def expression(self, p):
        return Not(linea=p.lineno, expr=NoExpr())

    # fin operaciones logicas

    # ini parentesis
    @_("'(' expression ')'")
    def expression(self, p):
        return p[1]

    # fin parentesis

    # ini objetos
    @_("OBJECTID")
    def expression(self, p):
        return Objeto(linea=p.lineno, nombre=p[0])

    @_("INT_CONST")
    def expression(self, p):
        return Entero(linea=p.lineno, valor=p[0])

    @_("STR_CONST")
    def expression(self, p):
        return String(linea=p.lineno, valor=p[0])

    @_("error INT_CONST")
    def expression(self, p):
        return Objeto(linea=p.lineno, nombre="error")

    @_("BOOL_CONST")
    def expression(self, p):
        return Booleano(linea=p.lineno, valor=p[0])

    # end objetos

    def error(self, p):
        if p is None:
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.value in self.keywords:
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.value in self.literals:
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.type in self.keywords:
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.type in self.literals:
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.type == "error":
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        elif p.type == "EOF":
            self.errores.append("Error de sintaxis en la linea: %d" % p.lineno)
        else:
            self.errores.append("Error desconocido en la linea: %d" % p.lineno)


def main():
    with open("02\\minimos\\classonefield.test", "r") as f:
        txt = f.read()

    txt = """class A {
    f(x : Int) : Object {
        3 + 2
    };
    };
    """
    lexer = CoolLexer()
    tokens = lexer.tokenize(txt)
    parser = CoolParser()
    parsed = parser.parse(tokens)
    print("____PARSE____")
    print(parsed)
    print("\n____AST_TREE____")
    print(parsed.str(0))


if __name__ == "__main__":
    main()
