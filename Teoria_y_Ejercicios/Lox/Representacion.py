from dataclasses import dataclass
from typing import List, Optional
from Lexer import Token


@dataclass
class ASTNode:
    """Base class for AST nodes."""
    def tostring(self, n=0) -> str:
        return " " * n + self.__class__.__name__

#######################################################################################
"""Syntax grammar"""
#######################################################################################

# program        → declaration* EOF ;
class Program:
    def __init__(self, declarations: List['Declaration']):
        self.declarations = declarations
        
        
#######################################################################################
"""Declarations"""
#######################################################################################

# declaration    → classDecl
#                | funDecl
#                | varDecl
#                | statement ;
@dataclass
class Declaration(ASTNode):
    """Represents a declaration in the Lox language."""
    pass


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

#######################################################################################
"""Statements"""
#######################################################################################

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


# exprStmt       → expression ";" ;
@dataclass
class ExpressionStmt(Statement):
    expression: Expression

    def tostring(self, n=0) -> str:
        return " " * n + "ExpressionStmt\n" + self.expression.tostring(n+2)


# forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
#                  expression? ";"
#                  expression? ")" statement ;
@dataclass
class ForStmt(Statement):
    initializer: Optional[Declaration]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement

    def tostring(self, n=0) -> str:
        output = " " * n + "ForStmt\n"
        if self.initializer:
            output += self.initializer.tostring(n+2) + "\n"
        if self.condition:
            output += self.condition.tostring(n+2) + "\n"
        if self.increment:
            output += self.increment.tostring(n+2) + "\n"
        output += self.body.tostring(n+2)


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




#######################################################################################
"""Expressions"""
#######################################################################################



# expression     → assignment ;
@dataclass
class Expression(ASTNode):
    """Base class for expressions."""
    pass


# assignment     → ( call "." )? IDENTIFIER "=" assignment
#                | logic_or ;
@dataclass
class Assignment(Expression):
    name: Token
    value: Expression

    def tostring(self, n=0) -> str:
        output = " " * n + f"Assign to {self.name.value}\n"
        output += self.value.tostring(n+2)
        return output
    

# logic_or       → logic_and ( "or" logic_and )* ;
@dataclass
class LogicalOr(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "LogicalOr\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output


# logic_and      → equality ( "and" equality )* ;
@dataclass
class LogicalAnd(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "LogicalAnd\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output


# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
@dataclass
class Equality(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + f"Equality op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    

# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
@dataclass
class Comparison(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + f"Comparison op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    

# term           → factor ( ( "-" | "+" ) factor )* ;
@dataclass
class Term(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + f"Term op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    
# factor         → unary ( ( "/" | "*" ) unary )* ;
@dataclass
class Factor(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + f"Factor op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    

# unary          → ( "!" | "-" ) unary | call ;
@dataclass
class Unary(Expression):
    operator: Token
    right: Expression

    def tostring(self, n=0) -> str:
        return " " * n + f"Unary op={self.operator.tipo}\n" + self.right.tostring(n+2)
    
    
# call           → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
@dataclass
class Call(Expression):
    callee: Expression
    paren: Token
    arguments: List[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "Call\n"
        output += self.callee.tostring(n+2)
        for arg in self.arguments:
            output += "\n" + arg.tostring(n+2)
        return output
    
    
# primary        → "true" | "false" | "nil" | "this" |
#                         | NUMBER | STRING | IDENTIFIER | "(" expression ")" 
#                         | "super" "." IDENTIFIER ;
@dataclass
class Literal(Expression):
    value: object

    def tostring(self, n=0) -> str:
        return " " * n + f"Literal: {self.value}"
    

#######################################################################################
"""Utility Rules"""
#######################################################################################

# function       → IDENTIFIER "(" parameters? ")" block ;
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


# parameters     → IDENTIFIER ( "," IDENTIFIER )* ;
@dataclass
class Parameter:
    name: str

    def tostring(self, n=0) -> str:
        return " " * n + f"Parameter: {self.name}"
    
    
# arguments      → expression ( "," expression )* ;
@dataclass
class Arguments:
    arguments: List[Expression]

    def tostring(self, n=0) -> str:
        output = " " * n + "Arguments:\n"
        for arg in self.arguments:
            output += arg.tostring(n+2) + "\n"
        return output
    

#######################################################################################
"""Lexical grammar"""
#######################################################################################


# NUMBER         → DIGIT+ ( "." DIGIT+ )? ;
@dataclass
class Number(Expression):
    value: float

    def tostring(self, n=0) -> str:
        return " " * n + f"Number: {self.value}"


# STRING         → "\"" <any char except "\"">* "\"" ;
@dataclass
class String(Expression):
    value: str
    def tostring(self, n=0) -> str:
        return " " * n + f"String: {self.value}"
    

# IDENTIFIER     → ALPHA ( ALPHA | DIGIT )* ;
@dataclass
class Identifier(Expression):
    name: str

    def tostring(self, n=0) -> str:
        return " " * n + f"Identifier: {self.name}"

# ALPHA          → "a" ... "z" | "A" ... "Z" | "_" ;
@dataclass
class Alpha(Expression):
    value: str

    def tostring(self, n=0) -> str:
        return " " * n + f"Alpha: {self.value}"


# DIGIT          → "0" ... "9" ;
@dataclass
class Digit(Expression):
    value: str

    def tostring(self, n=0) -> str:
        return " " * n + f"Digit: {self.value}"

