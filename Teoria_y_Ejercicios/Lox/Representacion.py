from dataclasses import dataclass
from Lexer import Token
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
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary
    

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
class Statement(Declaration):
    pass

@dataclass
class Program:
    declarations: List[Declaration]
