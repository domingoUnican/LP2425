from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional, Any

@dataclass
class Declaration:
    pass

@dataclass
class Primary:
    value: Any
    pass


@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary

@dataclass
class Call:
    pass

@dataclass
class CallAtribute(Call):
    base: Primary
    name_atribute = str
    otras: Call

@dataclass
class callFunction(Call):
    base: Primary
    args: List
    otras: Call

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
class Parameter:
    name: str
    body: Optional[str]    

@dataclass
class Function:
    name: str
    params: List['Parameter']
    body: 'Block'


@dataclass
class Statement(Declaration):
    pass

@dataclass
class ClassDeclaration(Declaration):
    name: str
    father: str
    methods: List[Function]

@dataclass
class FunctionDeclaration(Declaration):
    fun: Function

@dataclass
class Assignment:
    name: str
    atr: Optional["Assignment"]


@dataclass
class Expression(Primary):
    assgn: Assignment

@dataclass
class ExprStmt(Statement):
    expr: Expression


@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: 'Expression'

@dataclass
class Program:
    declarations: List[Declaration]
