from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

@dataclass
class Declaration:
    classDecl: Optional["ClassDeclaration"]=None
    funDecl: Optional["FunctionDeclaration"]=None
    varDecl: Optional["VarDeclaration"]=None
    statement: Optional["Statement"]=None


@dataclass
class Primary:
    number: Optional["Number"]=None
    string: Optional["String"]=None
    id: Optional["Identifier"]=None

@dataclass
class Logic_OR:
    logic_and:Logic_AND
    logic_and:Logic_AND
    
@dataclass
class Assignment:
    pass

@dataclass
class AssignmentWithAssignment:
    call: Optional["Call"]=None
    identificator: str
    assignment: Assignment

@dataclass
class AssignmentWithLogicOR:
    logicOR: Logic_OR

@dataclass
class Expression:
    assignment: Assignment

@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary

@dataclass
class Call:
    primary: Primary

@dataclass
class CallAtribute(Call):
    identificator: str
    additional_call: Call

@dataclass
class CallMethod(Call):
    arguments: List
    additional_call: Call


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

@dataclass
class Statement(Declaration):
    exprStmt: Optional['ExpressionStatement']=None
    blockStmt: Optional['Block']=None
    ifStmt: Optional['IfStatement']=None
    whileStmt: Optional['WhileStatement']=None
    returnStmt: Optional['ReturnStatement']=None


@dataclass
class Program:
    declarations: List[Declaration]
