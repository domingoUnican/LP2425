from dataclasses import dataclass, field
from Lexer import Token
from typing import List, Optional, Tuple

"""
Clases padre para la gestios de varias declaraciones
simultanea de tipos en la representacion.
"""
@dataclass
class Declaration():
    pass

@dataclass
class Statement(Declaration):
    pass

@dataclass
class Assignment():
    pass

"""
true | talse | nil | this | NUMBER | STRING | IDENTIFIER
"""
@dataclass
class Primary():
    token: Token

    def tostring(self, n=0):
        indent = "  " * n
        if self.token.value == "super":
            return f"super\n.\n{self.token.value}"
        return f"{indent}{self.token.tipo}\n    {indent}{self.token.value}"

"""
primary ( '(' arguments?')' | '.' IDENTIFIER )*
"""
@dataclass
class Call():
    primary: Primary
    args: List['Arguments'] = field(default_factory=list)
    idents: List[Token] = field(default_factory=list)  # tokens IDENTIFIER tras puntos

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{self.primary.tostring(n+1)}\n"
        if self.args or self.idents:
            if self.args:
                output += f"(\n"
                for arg in self.args:
                    output += f"{arg.tostring(n+1)}\n"
                output += f")\n"
            if self.idents:
                n += 1
                indent = indent + "  " * n
                for ident in self.idents:
                    if ident.tipo == "TIdentifier":
                        output += f".\n{indent}{ident.value} \n"
            
        return output

"""
( ! | - ) unary | call 
"""
@dataclass
class Unary():
    op: Token = None
    unary: Optional['Unary'] = None
    call: Optional['Call'] = None

    def tostring(self, n=0):
        indent = "  " * n
        if self.op is not None and self.op.value not in ["!", "-"]:
            return f"ERROR no se esperava {self.op.value} para un unary"
        if self.call is not None:
            output = self.call.tostring(n + 1)
        if self.unary:
            output = f"{indent}{self.op.tipo.name}\n{indent}  {self.op.value}"
            output += "\n" + self.unary.tostring(n + 1)
        
        
        return output

@dataclass
class AssignmentWithAsigment(Assignment):
    call: Optional['Call']
    ident: Token
    expresion: Assignment

    def tostring(self, n=0):
        indent = "  " * n
        output = indent + f"=\n"
        if self.call:
            output += self.call.tostring(n)
        if self.ident.tipo == "TIdentifier":
            output += f".\n{self.ident.value} \n"
        output += indent + self.expresion.tostring(n + 1)
        return output

@dataclass
class Assignment(Assignment):
    logic: 'Logic_or'

    def tostring(self, n=0):
        return self.logic.tostring(n)

@dataclass
class Expresion:
    assig: Assignment

    def tostring(self, n=0):
        return self.assig.tostring(n)


@dataclass
class Arguments():
    expression1: Expresion
    expressions: List[Expresion] = field(default_factory=list)

    def tostring(self, n=0):
        output = self.expression1.tostring(n + 1)
        if self.expressions is not []:
            for expresion in self.expressions:
                output += "\n,\n" + expresion.tostring(n + 1)
        return output

@dataclass
class Parameters():
    ident1: Token
    idents: list[Token] = field(default_factory=list)

    def tostring(self, n=0):
        indent = "  " * n
        output = indent
        if self.ident1.tipo == "TIdentifier":
            output += f"{indent}{self.ident1.value}\n"
        else:
            return f"ERROR no se esperava {self.ident1.tipo.name} para un parametro"
        if self.idents:
            for ident in self.idents:
                if self.ident1.tipo == "TIdentifier":
                    output += f"{indent},\n{indent}{ident.value}\n"
                else:
                    return f"ERROR no se esperava {ident.tipo.name} para un parametro"
        return output

@dataclass
class Factor:
    left: Unary
    right: List[Tuple[Token, Unary]] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.left.tostring(n)
        indent = "  " * n
        output = self.left.tostring(n + 2)
        for token, unary in self.right:
            if token.value not in ["/", "*"]:
                return f"ERROR no se esperava {token.value} para un factor"
            output = f"{indent}{token.value}\n" + output + "\n" + unary.tostring(n + 2)
        return output

@dataclass
class Term:
    first: Factor
    right: List[Tuple[Token, Factor]] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.first.tostring(n)
        indent = "  " * n
        output = self.first.tostring(n + 2)
        for token, factor in self.right:
            if token.value not in ["-", "+"]:
                return f"ERROR no se esperava {token.value} para un tem"
            output = f"{indent}{token.value}\n" + output + "\n" + factor.tostring(n + 2)
        return output

@dataclass
class Comparison:
    left: Term
    right: List[Tuple[Token, Term]] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.left.tostring(n)
        indent = "  " * n
        output = self.left.tostring(n + 2)
        for token, term in self.right:
            if token.value not in [">", ">=", "<", "<="]:
                return f"EORR no se esperava {token.value} para un comparison"
            output = f"{indent}{token.value}\n" + output + "\n" + term.tostring(n + 2)
        return output

@dataclass
class Equality():
    left: Comparison
    right: List[Tuple[Token, Comparison]] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.left.tostring(n)
        indent = "  " * n
        output = self.left.tostring(n + 2)
        for token, comp in self.right:
            output = f"{indent}{token.value}\n" + output + "\n" + comp.tostring(n + 2)
        return output

@dataclass
class Logic_and():
    left: Equality
    right: List[Tuple[Token, Equality]] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.left.tostring(n)
        indent = "  " * n
        output = self.left.tostring(n + 2)
        for token, eq in self.right:
            output = f"{indent}{token.value}\n" + output + "\n" + eq.tostring(n + 2)
        return output

@dataclass
class Logic_or():
    left: Logic_and
    right: List[Logic_and] = field(default_factory=list)

    def tostring(self, n=0):
        if not self.right:
            return self.left.tostring(n)
        
        indent = "  " * n
        output = self.left.tostring(n + 1)  
        for and_expr in self.right:
            output = f"{indent}and\n" + output + "\n" + and_expr.tostring(n + 1)
        return output


@dataclass
class Function():
    ident: Token
    body: 'Block'
    param: Parameters = None

    def tostring(self, n=0):
        indent = "  " * n
        output = indent
        if self.ident.tipo == "TIdentifier":
            output += f"{self.ident.value}\n"
        else:
            return f"EORR no se esperava {self.ident.tipo.name} para un factor"
        if self.param:
            output += f"(\n{self.param.tostring(n+1)}\n)\n"
        output += "\n" + self.body.tostring(n + 1)
        return output

@dataclass
class ClassDeclaration(Declaration):
    left_ident: Token
    right_ident: Token = None
    funts: List[Function] = field(default_factory=list)

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}class\n{indent}{self.left_ident.value}\n"
        if self.right_ident:
            indent = "  " * (n + 1)
            output += f"{indent}<\n{indent}{self.right_ident.value}\n"
        if self.funts:
          for fun in self.funts:
              output += indent + "{\n"
              output += fun.tostring(n + 2)
              output += "\n"
          output += indent + "}"
        return output


@dataclass
class FunctionDeclaration(Declaration):
    fun: Function

    def tostring(self, n=0):
        indent = "  " * n
        output = indent + "{\n"
        output += f"{indent}{self.fun.tostring(n+1)}\n"
        output += indent + "}\n"
        return output

@dataclass
class VarDeclaration(Declaration):
    ident: Token
    expr: Expresion = None

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}var\n{indent}{self.ident.value}\n"
        if self.expr:
            output += f"{indent}=\n"
            output += self.expr.tostring(n + 2)
        output += "\n;"
        return output + "\n"

@dataclass
class ExprStmt(Statement):
    expr: Expresion

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}{self.expr.tostring(n+1)}\n;"
        return output + "\n"
    
@dataclass
class PrintStmt(Statement):
    expr: Expresion

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}print\n"
        output += f"{indent}{self.expr.tostring(n+1)}\n;"
        return output + "\n"

@dataclass
class ForStmt(Statement):
    # statement: Statement OBLIGATORIO PERO PRINTA AL FINAL

    decl: VarDeclaration = None
    expr_Stmt: ExprStmt = None

    expression1: Expresion = None
    expression2: Expresion = None

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}for\n"
        output += f"(\n"
        if self.decl:
            output += f"{indent}{self.decl.tostring(n+1)}\n"
        elif self.expr_Stmt: 
            output += f"{indent}{self.expr_Stmt.tostring(n+1)}\n"
        else: 
            output += f"{indent};\n"
        if self.expression1:
            output += f"{indent}{self.expression1.tostring(n+1)}\n"
            output += f"{indent};\n"
        if self.expression2:
            output += f"{indent}{self.expression2.tostring(n+1)}\n"
        output += f")\n"

        # output += f"{indent}{self.statement.tostring(n+1)}\n"

        return output + "\n"
    
@dataclass
class IfStmt(Statement):
    
    condition: Expresion
    statement: Statement

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}if\n"
        output += f"(\n"
        output += f"{indent}{self.condition.tostring(n+1)}\n"
        output += f")\n"
        output += f"{indent}{self.statement.tostring(n+1)}\n"
        return output
    
@dataclass
class ReturnStmt(Statement):
    expression: Expresion = None

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}return\n"
        if self.expression:
            output += f"{indent}{self.expression.tostring(n+1)}\n;\n"
        return output + "\n"
    
@dataclass
class WhileStmt(Statement):
    condition: Expresion
    statement: Statement

    def tostring(self, n=0):
        indent = "  " * n
        output = f"{indent}while\n"
        output += f"(\n"
        output += f"{indent}{self.condition.tostring(n+1)}\n"
        output += f")\n"
        output += f"{indent}{self.statement.tostring(n+1)}\n"
        return output


@dataclass
class Block(Statement):
    declarations: list[Declaration] = field(default_factory=list)

    def tostring(self, n=0):
        indent = "  " * n
        output = indent + "{\n"
        for declaration in self.declarations:
            output += f"{indent}{declaration.tostring(n+1)}\n"
        output = indent + "}\n"
        return output


@dataclass
class Program:
    declarations: List[Declaration]

    def tostring(self):
        output = ""
        for declaration in self.declarations:
            output += declaration.tostring()
        return output
