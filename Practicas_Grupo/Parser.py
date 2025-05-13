# coding: utf-8

from Clases import *
from Lexer import CoolLexer
from sly import Parser


class CoolParser(Parser):
    nombre_fichero = ""
    tokens = CoolLexer.tokens
    key_words = CoolLexer._key_words
    literals = CoolLexer.literals
    debugfile = "salida.out"
    errores = []

    precedence = (
        ("right", "ASSIGN"),
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
            padre="Object",
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p[3],
        )

    @_("CLASS TYPEID INHERITS TYPEID '{' componentes '}'")
    def clase(self, p):
        return Clase(
            linea=p.lineno,
            nombre=p[1],
            padre=p[3],
            nombre_fichero=self.nombre_fichero,
            caracteristicas=p[5],
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

    @_("error ';'")
    def componentes(self, p):
        return []

    @_("OBJECTID '(' ')' ':' TYPEID '{' expresion '}'")
    def componente(self, p):
        return Metodo(linea=p.lineno, nombre=p[0], tipo=p[4], cuerpo=p[6], formales=[])

    @_("OBJECTID '(' ')' ':' TYPEID '{' error '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[4], cuerpo=NoExpr(), formales=[]
        )

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expresion '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=p[7], formales=p[2]
        )

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' error '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=NoExpr(), formales=p[2]
        )

    @_("OBJECTID '(' error ')' ':' TYPEID '{' expresion '}'")
    def componente(self, p):
        return Metodo(
            linea=p.lineno, nombre=p[0], tipo=p[5], cuerpo=p[7], formales=NoExpr()
        )

    @_("OBJECTID ':' TYPEID")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    @_("OBJECTID ':' error")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    @_("OBJECTID ':' TYPEID ASSIGN expresion")
    def componente(self, p):
        return Atributo(linea=p.lineno, nombre=p[0], tipo=p[2], cuerpo=p[4])

    # fin componentes

    # ini formales
    @_("formal")
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
    @_("OBJECTID ASSIGN expresion")
    def expresion(self, p):
        return Asignacion(linea=p.lineno, nombre=p[0], cuerpo=p[2])

    # fin asignacion

    # ini llamada metodo
    @_("expresion '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(
            linea=p.lineno, cuerpo=p[0], nombre_metodo=p[2], argumentos=[]
        )

    @_("expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(
            linea=p.lineno, cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=[]
        )

    @_("expresion '.' OBJECTID '(' params ')'")
    def expresion(self, p):
        return LlamadaMetodo(
            linea=p.lineno, cuerpo=p[0], nombre_metodo=p[2], argumentos=p[4]
        )

    @_("expresion '@' TYPEID '.' OBJECTID '(' params ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(
            linea=p.lineno, cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=p[6]
        )

    @_("OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p[0],
            argumentos=[],
        )

    @_("OBJECTID '(' params ')'")
    def expresion(self, p):
        return LlamadaMetodo(
            linea=p.lineno,
            cuerpo=Objeto(linea=p.lineno, nombre="self"),
            nombre_metodo=p[0],
            argumentos=p[2],
        )

    @_("expresion")
    def params(self, p):
        return [p[0]]

    @_("params ',' expresion")
    def params(self, p):
        p[0].append(p[2])
        return p[0]

    # fin llamada metodo

    # ini condicionales
    @_("IF expresion THEN expresion ELSE expresion FI")
    def expresion(self, p):
        return Condicional(linea=p.lineno, condicion=p[1], verdadero=p[3], falso=p[5])

    # fin condicionales

    # ini bucles
    @_("WHILE expresion LOOP error LOOP")
    def expresion(self, p):
        return Bucle(linea=p.lineno, condicion=p[1], cuerpo=NoExpr())

    @_("WHILE expresion LOOP expresion POOL")
    def expresion(self, p):
        return Bucle(linea=p.lineno, condicion=p[1], cuerpo=p[3])

    # fin bucles

    # ini bloque
    @_("'{' expresiones '}'")
    def expresion(self, p):
        return Bloque(linea=p.lineno, expresiones=p[1])

    # fin bloque

    # ini punto y coma
    @_("expresion ';'")
    def expresiones(self, p):
        return [p[0]]

    @_("expresiones expresion ';'")
    def expresiones(self, p):
        p[0].append(p[1])
        return p[0]

    @_("error ';'")
    def expresiones(self, p):
        return []

    # fin punto y coma

    # ini let
    @_("LET declslet IN expresion")
    def expresion(self, p):
        declslet = p[1]
        cuerpo = p[3]
        for nombre, tipo, inicializacion in reversed(declslet):
            cuerpo = Let(
                linea=p.lineno,
                nombre=nombre,
                tipo=tipo,
                inicializacion=inicializacion,
                cuerpo=cuerpo,
            )
        return cuerpo

    @_("OBJECTID ':' TYPEID ASSIGN expresion")
    def decllet(self, p):
        return p[0], p[2], p[4]

    @_("OBJECTID ':' TYPEID")
    def decllet(self, p):
        return p[0], p[2], NoExpr()

    @_("declslet ',' decllet")
    def declslet(self, p):
        p[0].append(p[2])
        return p[0]

    @_("decllet")
    def declslet(self, p):
        return [p[0]]

    # fin let

    # ini switch
    @_("CASE expresion OF ramas ESAC")
    def expresion(self, p):
        return Switch(linea=p.lineno, expr=p[1], casos=p[3])

    @_('rama ";"')
    def ramas(self, p):
        return [p[0]]

    @_('ramas rama ";"')
    def ramas(self, p):
        p[0].append(p[1])
        return p[0]

    @_('OBJECTID ":" TYPEID DARROW expresion')
    def rama(self, p):
        return RamaCase(linea=p.lineno, nombre_variable=p[0], tipo=p[2], cuerpo=p[4])

    # fin switch

    # ini nueva
    @_("NEW TYPEID")
    def expresion(self, p):
        return Nueva(linea=p.lineno, tipo=p[1])

    @_("error TYPEID")
    def expresion(self, p):
        return Nueva(linea=p.lineno, tipo=p[1])

    # fin nueva

    # ini nulo
    @_("ISVOID expresion")
    def expresion(self, p):
        return EsNulo(linea=p.lineno, expr=p[1])

    @_("ISVOID error")
    def expresion(self, p):
        return EsNulo(linea=p.lineno, expr=NoExpr())

    # fin nulo

    # ini operaciones aritmeticas
    @_("expresion '+' expresion")
    def expresion(self, p):
        return Suma(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expresion '-' expresion")
    def expresion(self, p):
        return Resta(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expresion '*' expresion")
    def expresion(self, p):
        return Multiplicacion(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expresion '/' expresion")
    def expresion(self, p):
        return Division(linea=p.lineno, izquierda=p[0], derecha=p[2])

    # fin operaciones aritmeticas

    # ini operaciones logicas
    @_("'~' expresion")
    def expresion(self, p):
        return Neg(linea=p.lineno, expr=p[1])

    @_("expresion '<' expresion")
    def expresion(self, p):
        return Menor(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expresion LE expresion")
    def expresion(self, p):
        return LeIgual(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("expresion '=' expresion")
    def expresion(self, p):
        return Igual(linea=p.lineno, izquierda=p[0], derecha=p[2])

    @_("NOT expresion")
    def expresion(self, p):
        return Not(linea=p.lineno, expr=p[1])

    # fin operaciones logicas

    # ini parentesis
    @_("'(' expresion ')'")
    def expresion(self, p):
        return p[1]

    # fin parentesis

    # ini objetos
    @_("OBJECTID")
    def expresion(self, p):
        return Objeto(linea=p.lineno, nombre=p[0])

    @_("INT_CONST")
    def expresion(self, p):
        return Entero(linea=p.lineno, valor=p[0])

    @_("STR_CONST")
    def expresion(self, p):
        return String(linea=p.lineno, valor=p[0])

    @_("BOOL_CONST")
    def expresion(self, p):
        return Booleano(linea=p.lineno, valor=p[0])

    # fin objetos

    def error(self, p):
        if p is None:
            resultado = f'"{self.nombre_fichero}", line 0: syntax error at or near EOF'
        elif p.value.lower() in self.key_words or p.type == "LE":
            resultado = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type}'
        elif p.value.lower() in self.literals:
            resultado = f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near '{p.type}'"
        else:
            resultado = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type} = {p.value}'

        self.errores.append(resultado)


def main():
    fichero = "casenoexpr.test"
    with open(f"02/grading/{fichero}", "r") as f:
        txt = f.read()

    lexer = CoolLexer()
    tokens = lexer.tokenize(txt)
    parser = CoolParser()
    parser.nombre_fichero = fichero

    try:
        parsed = parser.parse(tokens)

        if parsed:
            print("____PARSE____")
            print(parsed)
            print("\n____AST_TREE____")
            print(parsed.str(0))

        if parser.errores:
            print("\n".join(parser.errores))
            print("Compilation halted due to lex and parse errors")

    except Exception as e:
        print(f"Parser error: {e}")


if __name__ == "__main__":
    main()
