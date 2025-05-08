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
    class Number(Primary):
        def tostring(self, n):
            output = " " * n + self.value.tipo + "\n"
            output += " " * (n + 2) + self.value.value + "\n"
            return output


@dataclass
class String(Primary):
    def tostring(self, n):
        output  = " " * n     + self.value.tipo + "\n"
        output += " " * (n+2) + self.value.value + "\n"
        return output

@dataclass
class Call(Expression):
    pass


@dataclass
class Unary(Expression):
    op: str
    atr: Optional["Unary"] = None

    def tostring(self, n):
        output = " " * (n + 2) + "op: " + self.op + "\n"
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
        output += self.name + "\n"
        if self.parameters:
            output += self.parameters.tostring(n + 2)
        return output


@dataclass
class Factor:
    op: str
    first_un: Unary
    second_un: Unary

    def tostring(self, n):
        output = ""
        output += " " * n + self.op + "\n"
        output += self.first_un.tostring(n + 2) + "\n"
        output += self.second_un.tostring(n + 2) + "\n"
        return output


# Test Primary, Number, String
print("# Primary Test:")
primary_token = Token(1, "I am a string", "STRING")
primary = Primary(primary_token)
print(primary.tostring(0))

print("# Number Test:")
number_token = Token(2, "42", "NUMBER")
number = Number(number_token)
print(number.tostring(2))

print("# String Test:")
string_token = Token(3, "hello", "STRING")
string_node = String(string_token)
print(string_node.tostring(4))

# Test VarDecl containing a Number
print("# VarDecl Test:")
var_decl = VarDecl(name="x", expr=Number(Token(4, "100", "NUMBER")))
print(var_decl.tostring(0))

# Test PrintStmt
print("# PrintStmt Test:")
print_stmt = PrintStmt(expr=String(Token(5, "A message", "STRING")))
print(print_stmt.tostring(1))

# Test Block with multiple statements
declarations = [
    var_decl,
    FunDecl(fun=Function(name="foo", parameters=[], body=Block([])))
]
block = Block(declarations=declarations)
print("# Block Test:")
print(block.tostring(0))

# Test Function
print("# Function Test:")
func = Function(
    name="add",
    parameters=["a", "b"],
    body=Block([VarDecl("sum", Number(Token(6, "a + b", "EXPR")))])
)
print(func.tostring(0))

# Test IfStmt
print("# IfStmt Test:")
if_stmt = IfStmt(
    condition=Primary(Token(7, "true", "BOOLEAN")),
    then_branch=Block([PrintStmt(Primary(Token(8, "then branch", "STRING")))]),
    else_branch=Block([PrintStmt(Primary(Token(9, "else branch", "STRING")))])
)
print(if_stmt.tostring(0))

# Test ForStmt
print("# ForStmt Test:")
for_stmt = ForStmt(
    init=VarDecl("i", Number(Token(10, "0", "NUMBER"))),
    condition=Comparison(left=Primary(Token(11, "i < 3", "EXPR")), right=None),
    increment=Assignment(name="i", expr=Primary(Token(12, "i + 1", "EXPR"))),
    body=Block([PrintStmt(Primary(Token(13, "loop", "STRING")))])
)
print(for_stmt.tostring(0))

# Test WhileStmt
print("# WhileStmt Test:")
while_stmt = WhileStmt(
    condition=Primary(Token(14, "cond", "EXPR")),
    body=Block([ExprStmt(Primary(Token(15, "body expr", "EXPR")))])
)
print(while_stmt.tostring(0))

# Test ReturnStmt
print("# ReturnStmt Test:")
return_stmt = ReturnStmt(value=Primary(Token(16, "result", "EXPR")))
print(return_stmt.tostring(0))

# Test Program
print("# Program Test:")
program = Program(declarations=[
    VarDecl("x", Number(Token(17, "5", "NUMBER"))),
    FunDecl(fun=func),
    ExprStmt(Primary(Token(18, "end", "STRING")))
])
print(program.tostring())