# coding: utf-8
from dataclasses import dataclass, field
from typing import List


@dataclass
class Nodo:
    linea: int = 0
    tipo: str = "_no_type"

    def Tipo(self):
        return self.tipo

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'


@dataclass
class Formal(Nodo):
    nombre_variable: str = "_no_set"
    tipo: str = "_no_type"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado


class Expresion(Nodo):
    cast: str = "_no_type"

    def Tipo(self, ctx=None):
        # Si no se pasa contexto, usamos el global
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos()
            ctx = contexto_tipos
        # Por defecto, solo devuelve el tipo almacenado
        return self.cast


@dataclass
class Asignacion(Expresion):
    nombre: str = "_no_set"
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # El tipo de la asignación es el tipo de la expresión a la derecha
        if self.cuerpo:
            self.cuerpo.Tipo(ctx)
            if ctx.tipo_de(self.nombre) == self.cuerpo.cast:
                self.cast = self.cuerpo.cast
            else:
                raise Exception(
                    f"{self.linea}: Type {self.cuerpo.cast} of assigned expression does not conform to declared type {ctx.tipo_de(self.nombre)} of identifier {self.nombre}.\nCompilation halted due to static semantic errors."
                )
        return self.cast


@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion = None
    clase: str = "_no_type"
    nombre_metodo: str = "_no_set"
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += "".join([c.str(n + 2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: _no_type\n'
        return resultado

    def Tipo(self, ctx=None):
        # Aquí podríamos buscar el tipo de retorno del método en la clase, pero por ahora solo algunos casos
        self.cuerpo.Tipo(ctx)
        if self.nombre_metodo == "copy":
            self.cast = self.cuerpo.cast
        elif self.nombre_metodo == "length":
            self.cast = "Int"
        else:
            self.cast = "_no_type"
        return self.cast


@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion = None
    nombre_metodo: str = "_no_set"
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += "".join([c.str(n + 2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        self.cuerpo.Tipo(ctx)
        for arg in self.argumentos:
            arg.Tipo(ctx)
        # Usamos la clase actual del contexto
        clase_actual = ctx.clase_actual if ctx else None
        if (
            isinstance(self.cuerpo, Objeto)
            and self.cuerpo.nombre == "self"
            and clase_actual
        ):
            # Buscar el método en la clase actual
            for m in clase_actual.caracteristicas:
                if isinstance(m, Metodo) and m.nombre == self.nombre_metodo:
                    self.cast = m.tipo
                    break
            else:
                self.cast = "_no_type"
        elif self.nombre_metodo == "copy":
            self.cast = self.cuerpo.cast
        elif self.nombre_metodo == "length":
            self.cast = "Int"
        else:
            self.cast = "_no_type"
        return self.cast


@dataclass
class Condicional(Expresion):
    condicion: Expresion = None
    verdadero: Expresion = None
    falso: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n + 2)
        resultado += self.verdadero.str(n + 2)
        resultado += self.falso.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # El tipo del if es el tipo común de las ramas then y else (aquí: Object si son distintos)
        if self.condicion:
            self.condicion.Tipo(ctx)
        tipo_then = self.verdadero.Tipo(ctx) if self.verdadero else None
        tipo_else = self.falso.Tipo(ctx) if self.falso else None
        if tipo_then == tipo_else:
            self.cast = tipo_then
        elif tipo_then is not None and tipo_else is not None:
            self.cast = "Object"
        elif tipo_then is not None:
            self.cast = tipo_then
        elif tipo_else is not None:
            self.cast = tipo_else
        else:
            self.cast = "_no_type"
        return self.cast


@dataclass
class Bucle(Expresion):
    condicion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n + 2)
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # El tipo de un bucle en COOL es siempre Object
        if self.condicion:
            self.condicion.Tipo(ctx)
        if self.cuerpo:
            self.cuerpo.Tipo(ctx)
        self.cast = "Object"  # En COOL, el tipo de loop es siempre Object
        return self.cast


@dataclass
class Let(Expresion):
    nombre: str = "_no_set"
    tipo: str = "_no_set"
    inicializacion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n + 2)
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # let x:T <- ... in ... crea un nuevo ámbito y declara x:T
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos()
            ctx = contexto_tipos
        if self.inicializacion:
            self.inicializacion.Tipo(ctx)
        ctx_local = ctx.entrar_ambito()
        ctx_local.declarar(self.nombre, self.tipo)
        if self.cuerpo:
            self.cuerpo.Tipo(ctx_local)
            self.cast = self.cuerpo.cast
        else:
            self.cast = self.tipo if self.tipo != "_no_set" else "_no_type"
        return self.cast


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += "".join([e.str(n + 2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += "\n"
        return resultado

    def Tipo(self, ctx=None):
        # El tipo de un bloque es el tipo de la última expresión
        for e in self.expresiones:
            e.Tipo(ctx)
            self.cast = e.cast
        return self.cast


@dataclass
class RamaCase(Nodo):
    nombre_variable: str = "_no_set"
    cast: str = "_no_set"
    tipo: str = "_no_set"
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2)
        return resultado

    def Tipo(self, ctx=None):
        # Cada rama del case crea un nuevo ámbito con la variable de la rama
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos()
            ctx = contexto_tipos
        ctx_local = ctx.entrar_ambito()
        ctx_local.declarar(self.nombre_variable, self.tipo)
        if self.cuerpo:
            self.cuerpo.Tipo(ctx_local)
            self.cast = self.cuerpo.cast
        else:
            self.cast = self.tipo if self.tipo != "_no_type" else "Object"
        return self.cast


@dataclass
class Swicht(Expresion):
    expr: Expresion = None
    casos: List[RamaCase] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n + 2)
        resultado += "".join([c.str(n + 2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # El tipo del case es el tipo común de todas las ramas (aquí simplificado)
        if self.expr:
            self.expr.Tipo(ctx)
        tipos = []
        for caso in self.casos:
            caso.Tipo(ctx)
            tipos.append(caso.cast)
        if tipos and all(t == tipos[0] for t in tipos):
            self.cast = tipos[0]
        elif tipos:
            self.cast = "Object"
        else:
            self.cast = "Object"
        return self.cast


@dataclass
class Nueva(Expresion):
    tipo: str = "_no_set"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # El tipo de new T es T
        self.cast = self.tipo
        return self.cast


@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion = None
    derecha: Expresion = None

    def Tipo(self, ctx=None):
        # Por defecto, operaciones binarias devuelven Int
        if self.izquierda:
            self.izquierda.Tipo(ctx)
        if self.derecha:
            self.derecha.Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Suma(OperacionBinaria):
    operando: str = "+"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Suma siempre devuelve Int
        if self.izquierda:
            self.izquierda.Tipo(ctx)
        if self.derecha:
            self.derecha.Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Resta(OperacionBinaria):
    operando: str = "-"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Resta siempre devuelve Int
        super().Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = "*"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Multiplicación siempre devuelve Int
        super().Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Division(OperacionBinaria):
    operando: str = "/"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # División siempre devuelve Int
        super().Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Menor(OperacionBinaria):
    operando: str = "<"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Menor siempre devuelve Bool
        super().Tipo(ctx)
        self.cast = "Bool"
        return self.cast


@dataclass
class LeIgual(OperacionBinaria):
    operando: str = "<="

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Menor o igual siempre devuelve Bool
        super().Tipo(ctx)
        self.cast = "Bool"
        return self.cast


@dataclass
class Igual(OperacionBinaria):
    operando: str = "="

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Igual siempre devuelve Bool
        if self.izquierda:
            self.izquierda.Tipo(ctx)
        if self.derecha:
            self.derecha.Tipo(ctx)
        self.cast = "Bool"
        return self.cast


@dataclass
class Neg(Expresion):
    expr: Expresion = None
    operador: str = "~"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Negación aritmética siempre devuelve Int
        if self.expr:
            self.expr.Tipo(ctx)
        self.cast = "Int"
        return self.cast


@dataclass
class Not(Expresion):
    expr: Expresion = None
    operador: str = "NOT"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Not lógico siempre devuelve Bool
        if self.expr:
            self.expr.Tipo(ctx)
        self.cast = "Bool"
        return self.cast


@dataclass
class EsNulo(Expresion):
    expr: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # isvoid siempre devuelve Bool
        if self.expr:
            self.expr.Tipo(ctx)
        self.cast = "Bool"
        return self.cast


@dataclass
class Objeto(Expresion):
    nombre: str = "_no_set"
    tipo: str = "_no_type"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos()
            ctx = contexto_tipos
        if self.nombre == "self":
            self.cast = "SELF_TYPE"
            return self.cast
        tipo = ctx.tipo_de(self.nombre)
        if tipo:
            self.cast = tipo
        else:
            self.cast = "Object"
        return self.cast


@dataclass
class NoExpr(Expresion):
    nombre: str = ""

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # NoExpr no tiene tipo
        self.cast = "_no_type"
        return self.cast


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Los enteros siempre son Int
        self.cast = "Int"
        return self.cast


@dataclass
class String(Expresion):
    valor: str = "_no_set"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Los strings siempre son String
        self.cast = "String"
        return self.cast


@dataclass
class Booleano(Expresion):
    valor: bool = False

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, ctx=None):
        # Los booleanos siempre son Bool
        self.cast = "Bool"
        return self.cast


@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += "".join([c.str(n + 2) for c in self.secuencia])
        return resultado

    def genera_codigo(self):
        return "print(fich)"

    def Tipo(self):
        contexto_tipos = ContextoTipos()
        for clase in self.secuencia:
            contexto_tipos.anhade_padre(clase.nombre, clase.padre)
            
        for c in self.secuencia:
            c.Tipo(ctx=contexto_tipos)
        return None


@dataclass
class Caracteristica(Nodo):
    nombre: str = "_no_set"
    tipo: str = "_no_set"
    cuerpo: Expresion = None

    def Tipo(self):
        if self.cuerpo:
            self.cuerpo.Tipo()
        return self.tipo


@dataclass
class Clase(Nodo):
    nombre: str = "_no_set"
    padre: str = "_no_set"
    nombre_fichero: str = "_no_set"
    caracteristicas: List[Caracteristica] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += "".join([c.str(n + 2) for c in self.caracteristicas])
        resultado += "\n"
        resultado += f'{(n+2)*" "})\n'
        return resultado

    def Tipo(self, ctx=None):
        # Creamos un nuevo contexto de tipos con la clase actual
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos(clase_actual=self)
            ctx = contexto_tipos
        else:
            ctx = ContextoTipos(ctx, clase_actual=self)
        for c in self.caracteristicas:
            if isinstance(c, Metodo):
                # Añadimos el método al contexto de tipos
                ctx.declarar(c.nombre, c.tipo)
            elif isinstance(c, Atributo):
                # Añadimos el atributo al contexto de tipos
                ctx.declarar(c.nombre, c.tipo)
            c.Tipo(ctx)
        return self.tipo


@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += "".join([c.str(n + 2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2)

        return resultado

    def Tipo(self, ctx=None):
        global contexto_tipos
        if ctx is None:
            if contexto_tipos is None:
                contexto_tipos = ContextoTipos()
            ctx = contexto_tipos
        ctx_local = ctx.entrar_ambito()
        for formal in self.formales:
            ctx_local.declarar(formal.nombre_variable, formal.tipo)
        if self.cuerpo:
            self.cuerpo.Tipo(ctx_local)
        return self.tipo


class Atributo(Caracteristica):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2)
        return resultado

    def Tipo(self, ctx=None):
        # Ahora acepta el contexto de tipos y lo propaga
        if self.cuerpo:
            self.cuerpo.Tipo(ctx)
        return self.tipo


# ----------------------
# Contexto de tipos para análisis estático
# ----------------------
class ContextoTipos:
    def __init__(self, padre=None, clase_actual=None):
        self.padre = padre  # Referencia al contexto padre (para anidamiento)
        self.tabla = {}  # Diccionario de variables -> tipo
        self.clase_actual = (
            clase_actual
            if clase_actual is not None
            else (padre.clase_actual if padre else None)
        )
        self.arbol_clases = {}  # Diccionario de clases -> atributos y métodos

    def entrar_ambito(self):
        # Crea un nuevo contexto hijo (nuevo ámbito), heredando la clase_actual
        return ContextoTipos(self, self.clase_actual)

    def salir_ambito(self):
        # Sale al contexto padre
        return self.padre

    def declarar(self, nombre, tipo):
        # Declara una variable en el contexto actual
        self.tabla[nombre] = tipo

    def tipo_de(self, nombre):
        # Busca el tipo de una variable, subiendo por los ámbitos si hace falta
        if nombre in self.tabla:
            return self.tabla[nombre]
        elif self.padre:
            return self.padre.tipo_de(nombre)
        else:
            return None
        
    def anhade_padre(self, nombre_clase, padre):
        # Añade una clase al contexto de tipos
        self.arbol_clases[nombre_clase] = padre
        
    def dime_padre(self, nombre_clase):
        # Devuelve el padre de una clase
        if nombre_clase == "Object":
            return "Object"
        return self.arbol_clases.get(nombre_clase, None)
    
    def dime_herencia(self, clase_A, clase_B):
        if clase_A == "Object":
            return True
        if clase_A == clase_B:
            return True
        padre_a = self.dime_padre(clase_A)
        padre_b = self.dime_padre(clase_B)
        
        return self.dime_herencia(padre_a, padre_b) if padre_a else False

# ----------------------
# Ámbito de ejecución (para valores en tiempo de ejecución)
# ----------------------
class Ambito:
    actual = dict()  # Diccionario de variables -> valor
    pila = []  # Pila de diccionarios para anidar ámbitos

    def devuelve_valor(self, nombre):
        # Devuelve el valor de una variable (lanza excepción si no existe)
        valor = self.actual[nombre]
        return valor

    def anadir_valor(self, nombre, valor):
        # Añade o actualiza el valor de una variable en el ámbito actual
        self.actual[nombre] = valor

    def entramos_funcion(self):
        # Entra en un nuevo ámbito (por ejemplo, al entrar en una función)
        nuevo_actual = dict()
        self.pila.append(self.actual)
        self.actual = nuevo_actual

    def salimos_funcion(self):
        # Sale del ámbito actual y vuelve al anterior
        self.actual = self.pila.pop()


# Instancia global de ámbito de ejecución
ambito = Ambito()

contexto_tipos = None
