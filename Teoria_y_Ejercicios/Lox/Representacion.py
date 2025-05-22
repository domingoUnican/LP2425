from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional, Union

#Autores: Hugo Martinez, Jorge Garcia

# --- PRINCIPALES ---
@dataclass
class Declaration:
    pass
@dataclass
class Statement(Declaration):
    def tostring(self, n=0):
        return " " * n + "Statement:\n"
@dataclass
class Expression(Statement):
    pass

@dataclass
class ExprStmt(Statement):
    expr: Expression
    def tostring(self, n):
        output = " " * n + "ExprStmt:" + self.expr.tostring(n + 2)
        return output

@dataclass
class Primary(Expression):
    value: Token

    def tostring(self, n):
        lines = [" " * n + str(self.value.tipo),
                 " " * (n + 2) + str(self.value.value)]
        return "\n".join(lines)

@dataclass
class Assignment(Expression):
    name: str
    expr: Expression

    def tostring(self, n):
        output = " " * n + self.name + "\n" + self.expr.tostring(n + 2)
        return output

@dataclass
class Logic_or(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n):
        output = " " * n + "Logic_or:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output

@dataclass
class Logic_and(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n):
        output = " " * n + "Logic_and:\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output

@dataclass
class Term(Expression):
    left: "Factor"
    operator: Optional[Token]
    right: Optional["Factor"]

    def tostring(self, n):
        if self.operator:
            output = " " * (n + 2) + f"Operator: {self.operator.value}\n"

        if self.left:
            output += self.left.tostring(n + 3) + "\n"

        if self.right:
            output += self.right.tostring(n + 3) + "\n"

        return output.rstrip()

@dataclass
class Comparison(Expression):
    left: Term
    operator: Optional[Token]
    right: Optional[Term]

    def tostring(self, n):
        indent = " " * n
        if self.operator:
            output = indent + f"Comparison: {self.operator.value}\n"
        else:
            output = indent + "Comparison:\n"
        output += self.left.tostring(n + 2) + "\n"
        if self.right:
            output += self.right.tostring(n + 2) + "\n"

        return output.rstrip()
@dataclass
class Equality(Expression):
    left: Comparison
    operator: Optional[Token]
    right: Optional[Comparison]

    def tostring(self, n):
        output = " " * n + f"Equality: {self.operator.value}\n" + self.left.tostring(n + 2)
        if self.right:
            output += " " + self.right.tostring(n + 4)
        return output

@dataclass
class Call(Expression):
    pass

@dataclass
class CallFunction(Call):
    base: Primary
    arguments: List["Arguments"]
    others: Call

    def tostring(self, n):
        output = " " * n + "Call\n"
        output += self.base.tostring(n + 2) + "\n"
        if self.arguments:
            for arg in self.arguments:
                output += arg.tostring(n + 5) + "\n"
        if self.others:
            output += self.others.tostring(n + 2)
        return output.rstrip()

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
class Unary(Expression):
    op: Token
    right: Union[Token, "Unary"]

    def tostring(self, n):
        output = " " * n + f"Unary: {self.op.value}\n"
        output += self.right.tostring(n + 2)
        return output

@dataclass
class Factor(Expression):
    left: Unary
    operator: Optional[Token]
    right: Optional[Unary]

    def tostring(self, n):
        output = " " * n
        if self.operator:
            output += f"Factor: {self.operator.value}\n"
            output += self.left.tostring(n + 2) + "\n"
        if self.right:
            output += self.right.tostring(n + 2)
        return output

@dataclass
class Comparison(Expression):
    left: Term
    operator: Optional[Token]
    right: Optional[Term]

    def tostring(self, n):
        output = ""  # Inicializamos la variable 'output'

        if self.operator:
            output = " " * (n + 2) + f"Operator: {self.operator.value}\n"

        if self.left:
            output += self.left.tostring(n + 3) + "\n"

        if self.right:
            output += self.right.tostring(n + 3) + "\n"

        return output.rstrip()

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
    parameters: List[Expression]

    def tostring(self, n):
        output = " " * n + "Argument\n"
        output += self.name + ", "
        if self.parameters:
            output += self.parameters.tostring(n + 2)
        return output

@dataclass
class Number(Expression):
    value: float

    def tostring(self, n=0):
        return " " * n + f"Number: {self.value}"

@dataclass
class String(Expression):
    value: str

    def tostring(self, n=0):
        return " " * n + f"String: {self.value}"

@dataclass
class Identifier(Expression):
    name: str
    def tostring(self, n=0):
        return " " * n + f"Identifier: {self.name}"

@dataclass
class Alpha(Expression):
    value: str
    def tostring(self, n=0):
        return " " * n + f"Alpha: {self.value}"

@dataclass
class Digit(Expression):
    value: str
    def tostring(self, n=0):
        return " " * n + f"Digit: {self.value}"

# --- SENTENCIAS ---

@dataclass
class PrintStmt(Statement):
    expr: Expression
    def tostring(self, n):
        output = " " * n + "PrintStmt: \n"
        output += self.expr.tostring(n + 2) + "\n"
        return output

@dataclass
class ReturnStmt(Statement):
    value: Optional[Expression]

    def tostring(self, n):
        output = " " * n + "ReturnStmt: \n"
        output += self.value.tostring(n + 2)
        return output

@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]

    def tostring(self, n):
        output = " " * n + "IfStmt: \n"
        output += " " * (n + 2) + "Condition:\n" + self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "then_branch:\n" + self.then_branch.tostring(n + 4) + "\n"
        if self.else_branch:
            output += " " * (n + 2) + "else_branch:\n" + self.else_branch.tostring(n + 4)
        return output

@dataclass
class ForStmt(Statement):
    init: Optional[Statement]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement

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
class WhileStmt(Statement):
    condition: Expression
    body: Statement

    def tostring(self, n):
        output = " " * n + "WhileStmt: \n"
        output += " " * (n + 2) + "Condition:\n" + self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "body\n" + self.body.tostring(n + 4) + "\n"
        return output

# --- BLOQUE ---

@dataclass
class Block(Statement):
    declarations: Optional[Declaration]

    def tostring(self, n):
        output = " " * n + "BlockStmt: \n"
        for declaration in self.declarations:
            if declaration:
                output += declaration.tostring(n + 2)
        return output
# --- DECLARACIONES ---
@dataclass
class VarDecl(Declaration):
    name: str
    expr: Optional[Expression]

    def tostring(self, n):
        output = " " * n + "VarDecl:" + self.name + "\n"
        output += self.expr.tostring(n + 2)
        return output

@dataclass
class Function:
    name: str
    parameters: Optional['Parameters']
    body: Block

    def tostring(self, n):
        output = " " * n + "Function:" + self.name + "\n"
        output += " " * n + "Arguments:\n"
        if self.parameters:
            for parameter in self.parameters:
                if parameter:
                    output += " " * (n + 2) + str(parameter) + "\n"
        else:
            output += " " * (n + 2) + "No Parameters" + "\n"
        output += " " * n + "Body:\n"
        output += self.body.tostring(n + 2)
        return output

@dataclass
class FunDecl(Declaration):
    fun: Function

    def tostring(self, n):
        output = " " * n + "FunDecl:" + self.fun.name + "\n"
        output += self.fun.tostring(n + 2)
        return output

@dataclass
class ClassDecl(Declaration):
    name: str
    father: Optional["ClassDecl"]
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

# ---PROGRAMA---
@dataclass
class Program:
    declarations: List["Declaration"]

    def tostring(self, n=0):
        indent = " " * n
        lines = [f"{indent}Program:"]
        for declaration in self.declarations:
            lines.append(declaration.tostring(n + 2))
        return "\n".join(lines) + "\n"
