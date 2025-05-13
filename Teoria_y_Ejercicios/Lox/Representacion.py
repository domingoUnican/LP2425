from dataclasses import dataclass
from Lexer import tokenize, Token, TokenType
from typing import List, Optional

@dataclass
class Declaration:
    pass

@dataclass
class Primary:
    arg : str
    def tostring(self, n):
        return " " * n + self.arg + "\n"




@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None 
    

@dataclass
class Call:
    base: Primary
    args: List["Expression"]
    identifier: str
    
    def tostring(self, n):
        output = " " * n + self.base + "\n"
        for arg in self.args:
            output += arg.tostring(n+2) + "\n"
        output += " " * (n+2) + self.identifier + "\n"
        return output

@dataclass
class Number(Primary):
    tok: Token
    def tostring(self, n):
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  
        return output


            

@dataclass
class Function:
    name: str
    params: List['Parameter']
    body: 'Block'

    
@dataclass
class ClassDeclaration(Declaration):
    name: str
    father: str
    methods: List[Function]

@dataclass
class FunctionDeclaration(Declaration):
    fun: Function

@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: 'Expression'
    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += self.expr.tostring(n+2) + "\n"
        return output

@dataclass
class Expression:
    pass

@dataclass
class Parameter:
    name: str
    type_annotation: Optional[str] = None

@dataclass
class Block:
    statements: List[Declaration]

    def tostring(self, n):
        output = " " * n + "Block:\n"
        for stmt in self.statements:
            output += stmt.tostring(n+2)
        return output
    
@dataclass
class Factor:
    left: Expression 
    operator: Token   
    right: Expression
    

    def tostring(self, n):
        output = " " * n + f"Factor ({self.operator.value}):\n"
        output += " " * (n+2) + "Left:\n"
        output += self.left.tostring(n+4)
        output += " " * (n+2) + "Right:\n"
        output += self.right.tostring(n+4)
        return output

@dataclass
class Statement(Declaration):
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: Expression
    
    def tostring(self, n):
        output = " " * n + "Expression Statement:\n"
        output += self.expression.tostring(n+2)
        return output

@dataclass
class PrintStatement(Statement):
    expression: Expression
    
    def tostring(self, n):
        output = " " * n + "Print Statement:\n"
        output += self.expression.tostring(n+2)
        return output

@dataclass
class ReturnStatement(Statement):
    keyword: Token
    value: Optional[Expression] = None
    
    def tostring(self, n):
        output = " " * n + "Return Statement:\n"
        if self.value:
            output += self.value.tostring(n+2)
        return output

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement] = None
    
    def tostring(self, n):
        output = " " * n + "If Statement:\n"
        output += " " * (n+2) + "Condition:\n"
        output += self.condition.tostring(n+4)
        output += " " * (n+2) + "Then:\n"
        output += self.then_branch.tostring(n+4)
        if self.else_branch:
            output += " " * (n+2) + "Else:\n"
            output += self.else_branch.tostring(n+4)
        return output

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Statement
    
    def tostring(self, n):
        output = " " * n + "While Statement:\n"
        output += " " * (n+2) + "Condition:\n"
        output += self.condition.tostring(n+4)
        output += " " * (n+2) + "Body:\n"
        output += self.body.tostring(n+4)
        return output

@dataclass
class BlockStatement(Statement):
    block: Block
    
    def tostring(self, n):
        output = " " * n + "Block Statement:\n"
        output += self.block.tostring(n+2)
        return output

@dataclass
class Program:
    declarations: List[Declaration]
    
    def tostring(self):
        output = "Program:\n"
        for declaration in self.declarations:
            output += declaration.tostring(2)
        return output
    
# --- EXPRESIONES ---
@dataclass
class LiteralExpression(Expression):
    value: object  
    
    def tostring(self, n):
        return " " * n + f"Literal: {self.value}\n"

@dataclass
class VariableExpression(Expression):
    name: Token
    
    def tostring(self, n):
        return " " * n + f"Variable: {self.name.value}\n"

@dataclass
class GroupingExpression(Expression):
    expression: Expression
    
    def tostring(self, n):
        output = " " * n + "Grouping Expression:\n"
        output += self.expression.tostring(n+2)
        return output

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token  
    right: Expression
    
    def tostring(self, n):
        output = " " * n + f"Binary: {self.operator.value}\n"
        output += " " * (n+2) + "Left:\n"
        output += self.left.tostring(n+4)
        output += " " * (n+2) + "Right:\n"
        output += self.right.tostring(n+4)
        return output

@dataclass
class LogicalExpression(Expression):
    left: Expression
    operator: Token 
    right: Expression
    
    def tostring(self, n):
        output = " " * n + f"Logical: {self.operator.value}\n"
        output += " " * (n+2) + "Left:\n"
        output += self.left.tostring(n+4)
        output += " " * (n+2) + "Right:\n"
        output += self.right.tostring(n+4)
        return output

@dataclass
class UnaryExpression(Expression):
    operator: Token  # !, -
    right: Expression
    
    def tostring(self, n):
        output = " " * n + f"Unary: {self.operator.value}\n"
        output += " " * (n+2) + "Expression:\n"
        output += self.right.tostring(n+4)
        return output

@dataclass
class AssignExpression(Expression):
    name: Token
    value: Expression
    
    def tostring(self, n):
        output = " " * n + f"Assign: {self.name.value}\n"
        output += " " * (n+2) + "Value:\n"
        output += self.value.tostring(n+4)
        return output

@dataclass
class CallExpression(Expression):
    callee: Expression
    paren: Token  
    arguments: List[Expression]
    
    def tostring(self, n):
        output = " " * n + "Call Expression:\n"
        output += " " * (n+2) + "Call:\n"
        output += self.callee.tostring(n+4)
        output += " " * (n+2) + "Arguments:\n"
        for arg in self.arguments:
            output += arg.tostring(n+4)
        return output


@dataclass
class SetExpression(Expression):
    object: Expression
    name: Token  
    value: Expression
    
    def tostring(self, n):
        output = " " * n + f"Set Property: {self.name.value}\n"
        output += " " * (n+2) + "Object:\n"
        output += self.object.tostring(n+4)
        output += " " * (n+2) + "Value:\n"
        output += self.value.tostring(n+4)
        return output

@dataclass
class ThisExpression(Expression):
    keyword: Token
    
    def tostring(self, n):
        return " " * n + "This\n"

@dataclass
class SuperExpression(Expression):
    keyword: Token
    method: Token
    
    def tostring(self, n):
        return " " * n + f"Super.{self.method.value}\n"


@dataclass
class ForStatement(Statement):
    initializer: Optional[Declaration]  
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement
    
    def tostring(self, n):
        output = " " * n + "For Statement:\n"
        if self.initializer:
            output += " " * (n+2) + "Initializer:\n"
            output += self.initializer.tostring(n+4)
        if self.condition:
            output += " " * (n+2) + "Condition:\n"
            output += self.condition.tostring(n+4)
        if self.increment:
            output += " " * (n+2) + "Increment:\n"
            output += self.increment.tostring(n+4)
        output += " " * (n+2) + "Body:\n"
        output += self.body.tostring(n+4)
        return output

@dataclass
class ClassDeclaration(Declaration):
    name: str
    father: str
    methods: List[Function]
    
    def tostring(self, n):
        output = " " * n + f"Class {self.name}:\n"
        if self.father:
            output += " " * (n+2) + f"Inherits from: {self.father}\n"
        output += " " * (n+2) + "Methods:\n"
        for method in self.methods:
            output += " " * (n+4) + f"Method {method.name}:\n"
            output += " " * (n+6) + "Parameters:\n"
            for param in method.params:
                output += " " * (n+8) + f"{param.name}\n"
            output += " " * (n+6) + "Body:\n"
            output += method.body.tostring(n+8)
        return output


        