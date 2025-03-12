from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional, Any

@dataclass
class Declaration:
    pass

@dataclass
class Primary:
    pass

@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary
    def toString(self, n):
        output = " " * n + str(self.atr) + "\n"
        output += " " * (n + 2) + str(self.atr)  # Aquí ponemos el valor un poco más indentado
        return output

    
@dataclass
class Call:
    base: Primary

@dataclass
class CallMethod(Call):
    primary: Primary
    args: List
    additionalCalls: Call | None

@dataclass
class CallMethod(Call):
    primary: Primary
    identifier: str
    additionalCalls: Call | None 


@dataclass
class Number(Primary):
    tok: Token
    def toString(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)  # Aquí ponemos el valor un poco más indentado
        return output

@dataclass
class Factor:
    op: str
    first_un: Unary
    second_un: Unary

    def toString(self, n):
        output =""
        output += " "*n + self.op + "\n"
        output += self.first_un.toString(n+2) + "\n"
        output += self.second_un.toString(n+2) + "\n"
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

@dataclass
class Statement(Declaration):
    pass

@dataclass
class Program:
    declarations: List[Declaration]

