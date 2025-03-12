from dataclasses import dataclass
from typing import List, Optional
from Lexer import Token

### 📌 Base Classes ###

@dataclass
class ASTNode:
    """Base class for AST nodes."""
    def tostring(self, n=0) -> str:
        return " " * n + self.__class__.__name__


# declaration    → classDecl
#                | funDecl
#                | varDecl
#                | statement ;
@dataclass
class Declaration(ASTNode):
    """Represents a declaration in the Lox language."""
    pass

# statement      → exprStmt
#                | forStmt
#                | ifStmt
#                | printStmt
#                | returnStmt
#                | whileStmt
#                | block ;
@dataclass
class Statement(Declaration):
    """Represents a statement in Lox."""
    pass

# expression     → assignment ;
@dataclass
class Expression(ASTNode):
    """Base class for expressions."""
    pass

### Declarations ###

# classDecl      → "class" IDENTIFIER ( "<" IDENTIFIER )?
#                  "{" function* "}" ;
@dataclass
class ClassDeclaration(Declaration):
    name: str
    superclass: Optional[str]
    methods: List['Function']

    def tostring(self, n=0) -> str:
        output = " " * n + f"Class {self.name} < {self.superclass or 'None'} >\n"
        output += "\n".join([method.tostring(n+2) for method in self.methods])
        return output

# funDecl        → "fun" function ;
@dataclass
class FunctionDeclaration(Declaration):
    function: 'Function'

    def tostring(self, n=0) -> str:
        return " " * n + "FunctionDeclaration\n" + self.function.tostring(n+2)

# varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
@dataclass
class VarDeclaration(Declaration):
    name: str
    initializer: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + f"VarDeclaration: {self.name}"
        if self.initializer:
            output += f" = {self.initializer.tostring(n+2)}"
        return output

### Statements ###

# exprStmt       → expression ";" ;
@dataclass
class ExpressionStmt(Statement):
    expression: Expression

    def tostring(self, n=0) -> str:
        return " " * n + "ExpressionStmt\n" + self.expression.tostring(n+2)

# printStmt      → "print" expression ";" ;
@dataclass
class PrintStmt(Statement):
    expression: Expression

    def tostring(self, n=0) -> str:
        return " " * n + "PrintStmt\n" + self.expression.tostring(n+2)

# returnStmt     → "return" expression? ";" ;
@dataclass
class ReturnStmt(Statement):
    keyword: Token
    value: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "ReturnStmt"
        if self.value:
            output += "\n" + self.value.tostring(n+2)
        return output

# ifStmt         → "if" "(" expression ")" statement
#                  ( "else" statement )? ;
@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]

    def tostring(self, n=0) -> str:
        output = " " * n + "IfStmt:\n"
        output += " " * (n+2) + "Condition:\n" + self.condition.tostring(n+4) + "\n"
        output += " " * (n+2) + "Then:\n" + self.then_branch.tostring(n+4)
        if self.else_branch:
            output += "\n" + " " * (n+2) + "Else:\n" + self.else_branch.tostring(n+4)
        return output

# whileStmt      → "while" "(" expression ")" statement ;
@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Statement

    def tostring(self, n=0) -> str:
        output = " " * n + "WhileStmt:\n"
        output += " " * (n+2) + "Condition:\n" + self.condition.tostring(n+4) + "\n"
        output += " " * (n+2) + "Body:\n" + self.body.tostring(n+4)
        return output

# block          → "{" declaration* "}" ;
@dataclass
class Block(Statement):
    statements: List[Declaration]

    def tostring(self, n=0) -> str:
        output = " " * n + "Block:\n"
        for stmt in self.statements:
            output += stmt.tostring(n+2) + "\n"
        return output

### Expressions ###

@dataclass
class Literal(Expression):
    value: object

    def tostring(self, n=0) -> str:
        return " " * n + f"Literal: {self.value}"

@dataclass
class Grouping(Expression):
    expression: Expression

    def tostring(self, n=0) -> str:
        return " " * n + "Grouping\n" + self.expression.tostring(n+2)

@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression

    def tostring(self, n=0) -> str:
        output = " " * n + f"Binary op={self.operator.tipo}\n"
        output += self.left.tostring(n+2) + "\n"
        output += self.right.tostring(n+2)
        return output

@dataclass
class Logical(Expression):
    left: Expression
    operator: Token
    right: Expression

    def tostring(self, n=0) -> str:
        output = " " * n + f"Logical op={self.operator.tipo}\n"
        output += self.left.tostring(n+2) + "\n"
        output += self.right.tostring(n+2)
        return output

@dataclass
class Unary(Expression):
    operator: Token
    right: Expression

    def tostring(self, n=0) -> str:
        return " " * n + f"Unary op={self.operator.tipo}\n" + self.right.tostring(n+2)

@dataclass
class Call(Expression):
    callee: Expression
    arguments: List[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "Call\n" + self.callee.tostring(n+2)
        for arg in self.arguments:
            output += "\n" + arg.tostring(n+2)
        return output

@dataclass
class Assign(Expression):
    name: Token
    value: Expression

    def tostring(self, n=0) -> str:
        output = " " * n + f"Assign to {self.name.value}\n"
        output += self.value.tostring(n+2)
        return output

### 📌 Utility Rules ###

@dataclass
class Function:
    name: str
    parameters: List['Parameter']
    body: Block

    def tostring(self, n=0) -> str:
        output = " " * n + f"Function: {self.name}\n"
        output += " " * (n+2) + "Parameters:\n" + "\n".join([param.tostring(n+4) for param in self.parameters]) + "\n"
        output += " " * (n+2) + "Body:\n" + self.body.tostring(n+4)
        return output

@dataclass
class Parameter:
    name: str

    def tostring(self, n=0) -> str:
        return " " * n + f"Parameter: {self.name}"

### 📌 Root Program Node ###

@dataclass
class Program:
    declarations: List[Declaration]

    def tostring(self, n=0) -> str:
        output = " " * n + "Program:\n"
        for decl in self.declarations:
            output += decl.tostring(n+2) + "\n"
        return output
