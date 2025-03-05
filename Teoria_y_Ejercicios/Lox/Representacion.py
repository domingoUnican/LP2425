from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

@dataclass
class Declaration:
    def tostring(self, n=0):
        return " " * n + "Declaration " # Esto es para que se vea bonito el output

@dataclass
class Expression:
    def tostring(self, n=0):
        return " " * n + "Expression" # Esto es para que se vea bonito el output

@dataclass
class Primary(Expression):
    def tostring(self, n=0):
        return " " * n + "Primary Expression" + "\n"

@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary
    def tostring(self, n=0):
        return " " * n + f"Unary op={self.op}"

@dataclass
class Call:
    #call   → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
    base: Primary
    def tostring(self, n=0):
        return " " * n + "Call"

@dataclass
class Number(Primary):
    tok: Token
    def tostring(self, n):
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  # Aquí ponemos el valor un poco más indentado
        return output

@dataclass
class Factor:
    op: str
    first_un: Unary
    second_un: Unary

    def tostring(self, n):
        output =""
        output += " "*n + self.op + "\n"
        output += self.first_un.tostring(n+2) + "\n"
        output += self.second_un.tostring(n+2) + "\n"
        return output
            

@dataclass
class Function:
    name: str
    params: List['Parameter']
    body: 'Block'
    def tostring(self, n=0):
        return " " * n + f"Function: {self.name} " + "\n" + self.body.tostring(n+2) # Aquí llamamos al tostring de Block

@dataclass
class Parameter:
    name: str
    def tostring(self, n=0):
        return " " * n + f"Parameter: {self.name} "

@dataclass
class ClassDeclaration(Declaration):
    name: str
    father: str
    methods: List[Function]
    def tostring(self, n=0):
        return " " * n + f"Class: {self.name} < {self.father} > " + "\n" + " " * n + "Methods:\n" + "\n".join([method.tostring(n+2) for method in self.methods])

@dataclass
class FunctionDeclaration(Declaration):
    fun: Function
    def tostring(self, n=0):
        return " " * n + "FunctionDeclaration" + "\n" + self.fun.tostring(n+2)  # Aquí llamamos al tostring de Function
    

@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: 'Expression'
    def tostring(self, n=0):
        return " " * n + f"VarDeclaration: {self.name} = {self.expr.tostring(0)} "  # Aquí llamamos al tostring de Expression

@dataclass
class Statement(Declaration):
    def tostring(self, n=0):
        return " " * n + "Statement " # Esto es para que se vea bonito el output

@dataclass
class Literal(Expression):
    value: object
    def tostring(self, n=0):
        return " " * n + f"Literal: {self.value} "

@dataclass
class Grouping(Expression):
    expression: Expression
    def tostring(self, n=0):
        return " " * n + "Grouping" + "\n" + self.expression.tostring(n+2) # Aquí llamamos al tostring de Expression

@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression
    def tostring(self, n=0):
        output = " " * n + f"Binary op={self.operator.tipo}\n"
        output += self.left.tostring(n+2) + "\n"
        output += self.right.tostring(n+2)
        return output

@dataclass
class Logical(Expression):
    left: Expression
    operator: Token
    right: Expression
    def tostring(self, n=0):
        output = " " * n + f"Logical op={self.operator.tipo}\n"
        output += self.left.tostring(n+2) + "\n"
        output += self.right.tostring(n+2)
        return output

@dataclass
class Assign(Expression):
    name: Token
    value: Expression
    def tostring(self, n=0):
        output = " " * n + f"Assign to {self.name.value}\n"
        output += self.value.tostring(n+2)
        return output

@dataclass
class ExpressionStmt(Statement):
    expression: Expression
    def tostring(self, n=0):
        return " " * n + "ExpressionStmt\n" + self.expression.tostring(n+2)

@dataclass
class PrintStmt(Statement):
    expression: Expression
    def tostring(self, n=0):
        return " " * n + "PrintStmt\n" + self.expression.tostring(n+2)

@dataclass
class ReturnStmt(Statement):
    keyword: Token
    value: Optional[Expression]
    def tostring(self, n=0):
        output = " " * n + "ReturnStmt"
        if self.value:
            output += "\n" + self.value.tostring(n+2)
        return output

@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]
    def tostring(self, n=0):
        output = " " * n + "IfStmt:\n"
        output += " " * (n+2) + "Condition:\n" + self.condition.tostring(n+4) + "\n"
        output += " " * (n+2) + "Then:\n" + self.then_branch.tostring(n+4)
        if self.else_branch:
            output += "\n" + " " * (n+2) + "Else:\n" + self.else_branch.tostring(n+4)
        return output

@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Statement
    def tostring(self, n=0):
        output = " " * n + "WhileStmt:\n"
        output += " " * (n+2) + "Condition:\n" + self.condition.tostring(n+4) + "\n"
        output += " " * (n+2) + "Body:\n" + self.body.tostring(n+4)
        return output

@dataclass
class ForStmt(Statement):
    initializer: Optional[Declaration]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement
    def tostring(self, n=0):
        output = " " * n + "ForStmt:\n"
        if self.initializer:
            output += " " * (n+2) + "Initializer:\n" + self.initializer.tostring(n+4) + "\n"
        if self.condition:
            output += " " * (n+2) + "Condition:\n" + self.condition.tostring(n+4) + "\n"
        if self.increment:
            output += " " * (n+2) + "Increment:\n" + self.increment.tostring(n+4) + "\n"
        output += " " * (n+2) + "Body:\n" + self.body.tostring(n+4)
        return output

@dataclass
class Block(Statement):
    statements: List[Declaration]
    def tostring(self, n=0):
        output = " " * n + "Block:\n"
        for stmt in self.statements:
            output += stmt.tostring(n+2) + "\n"
        return output

@dataclass
class Program:
    declarations: List[Declaration]
    def tostring(self, n=0):
        output = " " * n + "Program:\n"
        for decl in self.declarations:
            output += decl.tostring(n+2) + "\n"
        return output
