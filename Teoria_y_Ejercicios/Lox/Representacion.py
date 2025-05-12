from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional


@dataclass
class Declaration:
    pass

@dataclass
class Statement(Declaration):
    pass

@dataclass
class Expression(Statement):
    pass

@dataclass
class Primary:
    value: Token

    def tostring(self, n):
        output = " " * n + str(self.value.tipo) + "\n"
        output += " " * (n + 2) + str(self.value.value)
        return output


@dataclass
class Block(Statement):
    declarations: List[Declaration]

    def tostring(self, n):
        output = " " * n + "BlockStmt: \n"
        for declaration in self.declarations:
            output += declaration.tostring(n + 2)
        return output



@dataclass
class Function:
    name: str
    parameters: List[any]
    body: Block

    def tostring(self, n):
        output = " " * n + "Function:" + self.name + "\n"
        output += " " * n + "Arguments:\n"
        for parameter in self.parameters:
            output += " " * (n + 2) + str(parameter) + "\n"
        output += " " * n + "Body:\n"
        output += self.body.tostring(n + 2)
        return output

@dataclass
class Number(Primary):
    tok: Token

    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)
        return output


@dataclass
class String(Primary):
    tok: Token

    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)
        return output

@dataclass
class Call(Expression):
    pass


@dataclass
class Unary(Expression):
    op: str
    atr: Optional["Unary"] = None

    def tostring(self, n):
        output = " " * (n + 1) + "op:"+ self.op + "\n"
        for element in self.atr:
            output += element.tostring(n + 2) + "\n"
        return output



@dataclass
class Program:
    declarations: List["Declaration"]

    def tostring(self, n=0):
        indent = " " * n
        lines = [f"{indent}Program:"]
        for declaration in self.declarations:
            lines.append(declaration.tostring(n + 2))

        return "\n".join(lines) + "\n"


@dataclass
class CallAtribute(Call):
    base: Primary
    name: str
    others: Call

    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += self.base.tostring(n + 2)
        if self.others:
            output += self.others.tostring(n + 2)
        return output


@dataclass
class CallFunction(Call):
    base: Primary
    arguments: List[Expression]
    others: Call

    def tostring(self, n):
        output = " " * n + "Call\n"
        output += self.base.tostring(n + 2)
        for arg in self.arguments:
            output += arg.tostring(n + 2)
        if self.others:
            output += self.others.tostring(n + 2)
        return output


@dataclass
class ClassDecl(Declaration):
    name: str
    father: any
    methods: List[Function]

    def tostring(self, n):
        output = " " * n + "ClassDecl:" + self.name + "\n"
        if self.father:
            output += " " * (n + 2) + "Father:" + self.father.name + "\n"
            for method in self.father.methods:
                output += method.tostring(n + 4)
        else:
            output += " " * (n + 2) + "Father object\n"
        for method in self.methods:
            output += method.tostring(n + 2)
        return output


@dataclass
class FunDecl(Declaration):
    fun: Function

    def tostring(self, n):
        output = " " * n + "FunDecl:" + self.fun.name + "\n"
        output += self.fun.tostring(n + 2)
        return output


@dataclass
class VarDecl(Declaration):
    name: str
    expr: Expression

    def tostring(self, n):
        output = " " * n + "VarDecl:" + self.name + "\n"
        output += self.expr.tostring(n + 2)
        return output



@dataclass
class ExprStmt(Statement):
    expr: Expression

    def tostring(self, n):
        output = " " * n + "ExprStmt:" + self.expr.tostring(n + 2)
        return output


@dataclass
class ForStmt(Statement):
    init: any
    condition: Expression
    increment: Expression
    body: Block

    def tostring(self, n):
        output = " " * n + "ForStmt: \n"
        if self.init:
            output += " " * (n + 2) + "Init:\n" + self.init.tostring(n + 4) + "\n"
        if self.condition:
            output += " " * (n + 2) + "Condition:\n" + self.condition.tostring(n + 4) + "\n"
        if self.increment:
            output += " " * (n + 2) + "Increment:\n" + self.increment.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "body\n" + self.body.tostring(n + 4) + "\n"
        return output


@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: Block
    else_branch: any

    def tostring(self, n):
        output = " " * n + "IfStmt: \n"
        output += " " * (n + 2) + "Condition:\n" + self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "then_branch:\n" + self.then_branch.tostring(n + 4) + "\n"
        if self.else_branch:
            output += " " * (n + 2) + "else_branch:\n" + self.else_branch.tostring(n + 4)
        return output


@dataclass
class PrintStmt(Statement):
    expr: Expression

    def tostring(self, n):
        output = " " * n + "PrintStmt: \n"
        output += self.expr.tostring(n + 2) + "\n"
        return output


@dataclass
class ReturnStmt(Statement):
    value: Expression

    def tostring(self, n):
        output = " " * n + "ReturnStmt: \n"
        output += self.value.tostring(n + 2)
        return output


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Block

    def tostring(self, n):
        output = " " * n + "WhileStmt: \n"
        output += " " * (n + 2) + "Condition:\n" + self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "body\n" + self.body.tostring(n + 4) + "\n"
        return output


@dataclass
class Assignment(Expression):
    name: str
    expr: any

    def tostring(self, n):
        output = " " * n + self.name + "\n" + self.expr.tostring(n + 2)
        return output


@dataclass
class Logic_or(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Logic_or:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Logic_and(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Logic_and:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Equality(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Equality:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Comparison(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Comparison:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Term(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Term:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Factor(Expression):
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Factor:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output


@dataclass
class Parameters(Expression):
    name: str
    parameters: List[any]

    def tostring(self, n):
        output = " " * n + "Parameters:\n"
        output += self.name + "\n"
        if self.parameters:
            output += self.parameters.tostring(n + 2)
        return output


@dataclass
class Arguments(Expression):
    name: str
    parameters: List[any]

    def tostring(self, n):
        output = " " * n + "Argument\n"
        output += self.name + ", "
        if self.parameters:
            output += self.parameters.tostring(n + 2)
        return output


@dataclass
class Factor:
    left: Expression
    right: Expression

    def tostring(self, n):
        output = " " * n + "Factor:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output

# Número entero simple
print("9876")
valor = Primary(Token(1, 9876, "NUMBER"))
print(valor.tostring(0))


# Número decimal
print("98.76")
valor = Primary(Token(1, 98.76, "NUMBER"))
print(valor.tostring(0))


# Cadena básica
print("Hello there!")
texto = Primary(Token(1, "Hello there!", "STRING"))
print(texto.tostring(0))


# Cadena vacía
print("Cadena vacía")
texto = Primary(Token(1, "", "STRING"))
print(texto.tostring(0))


# Cadena que parece número
print("999 como texto")
texto = Primary(Token(1, "999", "STRING"))
print(texto.tostring(0))


# Suma
print("operación suma")
op = Term(Unary("+", [Primary(Token(1, 10, "NUMBER")), Primary(Token(1, 5, "NUMBER"))]), None)
print(op.tostring(0))


# Resta
print("operación resta")
op = Term(Unary("-", [Primary(Token(1, 10, "NUMBER")), Primary(Token(1, 5, "NUMBER"))]), None)
print(op.tostring(0))


# Multiplicación
print("producto")
op = Factor(Unary("*", [Primary(Token(1, 4, "NUMBER")), Primary(Token(1, 3, "NUMBER"))]), None)
print(op.tostring(0))


# División
print("división")
op = Factor(Unary("/", [Primary(Token(1, 8, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]), None)
print(op.tostring(0))


# Negativo
print("negativo")
op = Unary("-", [Primary(Token(1, 100, "NUMBER"))])
print(op.tostring(0))


# Comparaciones
print("menor que")
cmp = Comparison(Term(Unary("<", [Primary(Token(1, 3, "NUMBER")), Primary(Token(1, 7, "NUMBER"))]), None), None)
print(cmp.tostring(0))


print("menor o igual que")
cmp = Comparison(Term(Unary("<=", [Primary(Token(1, 3, "NUMBER")), Primary(Token(1, 7, "NUMBER"))]), None), None)
print(cmp.tostring(0))


print("mayor que")
cmp = Comparison(Term(Unary(">", [Primary(Token(1, 3, "NUMBER")), Primary(Token(1, 7, "NUMBER"))]), None), None)
print(cmp.tostring(0))


print("mayor o igual que")
cmp = Comparison(Term(Unary(">=", [Primary(Token(1, 3, "NUMBER")), Primary(Token(1, 7, "NUMBER"))]), None), None)
print(cmp.tostring(0))


# Igualdades
print("¿son iguales?")
igual = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 42, "NUMBER")), Primary(Token(1, 42, "NUMBER"))]), None), None), None)
print(igual.tostring(0))


print("gato es diferente de tigre")
igual = Equality(Comparison(Term(Unary("!=", [Primary(Token(1, "cat", "STRING")), Primary(Token(1, "tiger", "STRING"))]), None), None), None)
print(igual.tostring(0))


print("321 == \"pi\"")
igual = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 321, "NUMBER")), Primary(Token(1, "pi", "STRING"))]), None), None), None)
print(igual.tostring(0))


print("456 == \"456\"")
igual = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 456, "NUMBER")), Primary(Token(1, "456", "STRING"))]), None), None), None)
print(igual.tostring(0))


# Lógicos
print("¡no verdadero!")
neg = Unary("!", [Primary(Token(1, True, "BOOLEAN"))])
print(neg.tostring(0))


print("¡no falso!")
neg = Unary("!", [Primary(Token(1, False, "BOOLEAN"))])
print(neg.tostring(0))


print("y lógico falso")
log = Logic_and(Equality(Comparison(Term(Factor(Unary("and", [Primary(Token(1, False, "BOOLEAN")), Primary(Token(1, False, "BOOLEAN"))]), None), None), None), None), None)
print(log.tostring(0))


print("y lógico verdadero")
log = Logic_and(Equality(Comparison(Term(Factor(Unary("and", [Primary(Token(1, True, "BOOLEAN")), Primary(Token(1, True, "BOOLEAN"))]), None), None), None), None), None)
print(log.tostring(0))


print("o lógico falso")
log = Logic_or(Logic_and(Equality(Comparison(Term(Factor(Unary("or", [Primary(Token(1, False, "BOOLEAN")), Primary(Token(1, False, "BOOLEAN"))]), None), None), None), None), None), None)
print(log.tostring(0))


print("o lógico verdadero")
log = Logic_or(Logic_and(Equality(Comparison(Term(Factor(Unary("or", [Primary(Token(1, True, "BOOLEAN")), Primary(Token(1, False, "BOOLEAN"))]), None), None), None), None), None), None)
print(log.tostring(0))


# Operación anidada
print("cálculo complejo")
comp = Unary("*", [Unary("+", [Primary(Token(1, 5, "NUMBER")), Primary(Token(1, 3, "NUMBER"))]), Primary(Token(1, 10, "NUMBER"))])
print(comp.tostring(0))


# Media
print("Calculo media")
media = Assignment("promedio", Unary("/", [Unary("+", [Primary(Token(1, "inicio", "STRING")), Primary(Token(1, "fin", "STRING"))]), Primary(Token(1, 2, "NUMBER"))]))
print(media.tostring(0))


# Imprimir mensaje
print("Imprimir saludo")
saludo = PrintStmt(Primary(Token(1, "¡Hola!", "STRING")))
print(saludo.tostring(0))


# Bloque de impresión
print("Bloque múltiple")
stmt1 = PrintStmt(Primary(Token(1, "Primera línea", "STRING")))
stmt2 = PrintStmt(Primary(Token(1, "Segunda línea", "STRING")))
bloque = Block([stmt1, stmt2])
print(bloque.tostring(0))


# Condicional simple
print("Condicional básico")
stmt_if = IfStmt(Primary(Token(1, "cond", "STRING")), Block([PrintStmt(Primary(Token(1, "Sí", "STRING")))]), Block([PrintStmt(Primary(Token(1, "No", "STRING")))]))
print(stmt_if.tostring(0))


# Condicional múltiple
print("Condicional múltiple")
stmt_if = IfStmt(Primary(Token(1, "cond", "STRING")),
    Block([PrintStmt(Primary(Token(1, "Positivo", "STRING")))]),
    IfStmt(Primary(Token(1, "otraCond", "STRING")),
        Block([PrintStmt(Primary(Token(1, "Negativo", "STRING")))]),
        Block([PrintStmt(Primary(Token(1, "Neutro", "STRING")))])))
print(stmt_if.tostring(0))


# While loop
print("Bucle while")
decl = VarDecl("contador", Primary(Token(1, 0, "NUMBER")))
stmt1 = PrintStmt(Primary(Token(1, "contador", "NUMBER")))
stmt2 = Assignment("contador", Unary("+", [Primary(Token(1, "contador", "NUMBER")), Primary(Token(1, 1, "NUMBER"))]))
cuerpo = Block([stmt1, stmt2])
bucle = WhileStmt(Comparison(Term(Factor(Unary("<", [Primary(Token(1, "contador", "NUMBER")), Primary(Token(1, 5, "NUMBER"))]), None), None), None), cuerpo)
print(Program([decl, bucle]).tostring(0))


# Bucle for
print("Bucle for")
decl = VarDecl("i", Primary(Token(1, 1, "NUMBER")))
actualiza = Assignment("i", Unary("+", [Primary(Token(1, "i", "NUMBER")), Primary(Token(1, 1, "NUMBER"))]))
bloque = Block([PrintStmt(Primary(Token(1, "i", "NUMBER")))])
bucle = ForStmt(decl, Comparison(Term(Factor(Unary("<", [Primary(Token(1, "i", "NUMBER")), Primary(Token(1, 6, "NUMBER"))]), None), None), None), actualiza, bloque)
print(bucle.tostring(0))


# Función sin retorno
print("Función suma")
cuerpo = Block([PrintStmt(Unary("+", [Primary(Token(1, "x", "NUMBER")), Primary(Token(1, "y", "NUMBER"))]))])
funcion = Function("suma", ["x", "y"], cuerpo)
print(FunDecl(funcion).tostring(0))


# Función con retorno
print("Función retorna suma")
retorno = ReturnStmt(Unary("+", [Primary(Token(1, "x", "NUMBER")), Primary(Token(1, "y", "NUMBER"))]))
funcion = Function("retornaSuma", ["x", "y"], Block([retorno]))
print(FunDecl(funcion).tostring(0))


# Clase
print("Clase Vehículo")
metodo1 = Function("arrancar", [], Block([PrintStmt(Primary(Token(1, "Motor encendido", "STRING")))]))
metodo2 = Function("conducir", ["destino"], Block([PrintStmt(Unary("+", [Primary(Token(1, "Rumbo a ", "STRING")), Primary(Token(1, "destino", "STRING"))]))]))
clase = ClassDecl("Vehiculo", None, [metodo1, metodo2])
print(clase.tostring(0))


# Instancia de clase
print("Instancia de Vehículo")
inst = VarDecl("miAuto", CallAtribute(Primary(Token(1, "Vehiculo", "CLASS")), "Vehiculo()", None))
print(Program([inst, PrintStmt(inst)]).tostring(0))


# Herencia
print("Herencia Vehículo -> Coche")
metodo = Function("tocarBocina", [], Block([PrintStmt(Primary(Token(1, "¡Beep beep!", "STRING")))]))
heredada = ClassDecl("Coche", clase, [metodo])
print(heredada.tostring(0))
