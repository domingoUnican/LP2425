from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

@dataclass
<<<<<<< HEAD
class Expression:
    def tostring(self, n=0):
        return " " * n + "Expression" 

@dataclass
class Declaration:
    def tostring(self, n=0):
        return " " * n + "Declaration " + "\n"
@dataclass
class Statement(Declaration):
    pass
    def tostring(self, n=0):
        return " " * n + "Statement " + "\n"
@dataclass
class Primary:
    tok: Token  # Argumento obligatorio
    atr: Optional["Unary"] = None  # Argumento opcional con valor predeterminado

    def tostring(self, n=0):
        if self.atr is None:
            return " " * n + f"Primary: {self.tok.value}\n"
        else:
            return " " * n + f"Primary: {self.tok.value}\n" + self.atr.tostring(n + 2)
@dataclass
class Assignment(Expression):
    name: Token
    value: Expression

    def tostring(self, n=0):
        output = " " * n + f"Assign to {self.name.value}\n"
        output += self.value.tostring(n+2)
        return output
=======
class Declaration:
    pass

@dataclass
class Primary:
    pass

>>>>>>> ac704d2b4d73596ecbbaf2a1cc3dfe1217ce59f1



@dataclass
class Unary:
    op: str
<<<<<<< HEAD
    atr: Optional["Unary"]=None 
    def tostring(self, n=0):
        return " " * n + f"Unary op={self.op}"
    

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
class Call:
    base: Primary
    args: List[Primary]
    id: str  # Asegúrate de que sea 'id' y no 'identifier'

    def tostring(self, n=0):
        output = " " * n + self.id + "\n"
        output += " " * (n + 2) + "Base:\n"
        output += self.base.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "Args:\n"
        for arg in self.args:
            output += arg.tostring(n + 4) + "\n"
        return output



@dataclass
class LogicalOr(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n=0):
        output = " " * n + "LogicalOr\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    
@dataclass
class LogicalAnd(Expression):
    left: Expression
    right: Optional[Expression]

    def tostring(self, n=0):
        output = " " * n + "LogicalAnd\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output

@dataclass
class Equality(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0):
        output = " " * n + f"Equality op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output  
    
@dataclass
class Comparison(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0):
        output = " " * n + f"Comparison op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    
@dataclass
class Term(Expression):
    left: Expression
    operator: Optional[Token]
    right: Optional[Expression]

    def tostring(self, n=0):
        output = " " * n + f"Term op={self.operator.tipo}\n"
        output += self.left.tostring(n+2)
        if self.right:
            output += "\n" + self.right.tostring(n+2)
        return output
    
@dataclass
=======
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary

@dataclass
class Call:
    base: Primary

@dataclass
class Number(Primary):
    tok: Token
    def tostring(self, n):
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  # Aquí ponemos el valor un poco más indentado
        return output

@dataclass
>>>>>>> ac704d2b4d73596ecbbaf2a1cc3dfe1217ce59f1
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
            
<<<<<<< HEAD
@dataclass
class Literal(Expression):
    value: object
    def tostring(self, n=0):
        return " " * n + f"Literal: {self.value} "+ "\n"
    
#FUNCIONES Y CLASES 
@dataclass
class Block(Statement):
    statements: List[Declaration]

    def tostring(self, n=0):
        output = " " * n + "Block:\n"
        for stmt in self.statements:
            output += stmt.tostring(n+2) + "\n"
        return output
    
@dataclass
class Parameter:
    name: str
    def tostring(self, n=0):
        return " " * n + f"Parameter: {self.name} "+ "\n"   
=======

>>>>>>> ac704d2b4d73596ecbbaf2a1cc3dfe1217ce59f1
@dataclass
class Function:
    name: str
    params: List['Parameter']
    body: 'Block'
<<<<<<< HEAD
    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += " " * (n + 2) + "Params:\n"
        for param in self.params:
            output += param.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4) + "\n"
        return output   
@dataclass
class ClassDeclaration(Declaration):
    name: str
    father: Optional[str] = None
    methods: List[Function] = None

    def tostring(self, n=0):
        if self.father is None:
            self.father = "Object"
        output = " " * n + f"Class {self.name}\n"
        output += " " * (n + 2) + f"< {self.father}\n"
        output += " " * (n + 4) + "{\n"
        if self.methods:
            for method in self.methods:
                output += method.tostring(n + 6) + "\n"
        output += " " * (n + 4) + "}\n"
        return output
@dataclass
class Statement(Declaration):
    pass
    def tostring(self, n=0):
        return " " * n + "Statement "

@dataclass
class Literal(Expression):
    value: object
    def tostring(self, n=0):
        return " " * n + f"Literal: {self.value} "+ "\n"
@dataclass
class FunctionDeclaration(Declaration):
    fun: Function
    def tostring(self, n):
        output = " " * n + f"fun {self.fun} + \n"
        return output
@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: Expression
    def tostring(self, n):
        output = " " * n + f"var {self.name}\n"
        output += "=" + self.expr.tostring(n + 2) +";" "\n"
        return output

@dataclass
class Arguments:
    arguments: List[Expression]

    def tostring(self, n=0):
        output = " " * n + "Arguments:\n"
        for arg in self.arguments:
            output += arg.tostring(n+2) + "\n"
        return output
=======

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
>>>>>>> ac704d2b4d73596ecbbaf2a1cc3dfe1217ce59f1

@dataclass
class Program:
    declarations: List[Declaration]
<<<<<<< HEAD

    def tostring(self, n=0):
        output = " " * n + "Program:\n"
        for decl in self.declarations:
            output += decl.tostring(n+2) + "\n"
        return output
    

####### GRAMATICA LEXICA #######



@dataclass
class Number(Primary):
    tok: Token
    def tostring(self, n):
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  # Aquí ponemos el valor un poco más indentado
        return output
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


################################### PRUEBAS ###################################
def test_number():
    print(f'{"-"*10} Test Number {"-"*10}')
    print(Number(tok=Token(lineno=0, value="99", tipo="Int")).tostring(2))

def test_unary():
    print(f'{"-"*10} Test Unary {"-"*10}')
    print(Unary(op="~", atr=Number(tok=Token(lineno=0, value="88", tipo="Int"))).tostring(2))

def test_primary():
    print(f'{"-"*10} Test Primary {"-"*10}')
    print(Primary(tok=Token(lineno=0, value="false", tipo="TFalse"), atr=Unary(op="@", atr=Number(tok=Token(lineno=0, value="77", tipo="TNumber")))).tostring(2))

def test_call():
    print(f'{"-"*10} Test Call {"-"*10}')
    print(Call(base=Primary(tok=Token(lineno=0, value="undefined", tipo="TUndefined")), args=[Number(tok=Token(lineno=0, value="66", tipo="Int"))], id="bar").tostring(2))

def test_function():
    print(f'{"-"*10} Test Function {"-"*10}')
    print(Function(name="anotherFunction", params=[Parameter(name="param1"), Parameter(name="param2")], body=Block(statements=[])).tostring(2))

def test_class_declaration():
    print(f'{"-"*10} Test ClassDeclaration {"-"*10}')
    print(ClassDeclaration(name="AnotherClass", father="AnotherBaseClass", methods=[
        Function(name="method1", params=[], body=Block(statements=[])),
        Function(name="method2", params=[], body=Block(statements=[]))
    ]).tostring(2))

def test_function_declaration():
    print(f'{"-"*10} Test FunctionDeclaration {"-"*10}')
    print(FunctionDeclaration(fun=Function(name="anotherMethod", params=[], body=Block(statements=[]))).tostring(2))

def test_var_declaration():
    print(f'{"-"*10} Test VarDeclaration {"-"*10}')
    print(VarDeclaration(name="anotherVar", expr=Number(tok=Token(lineno=0, value="11", tipo="Int"))).tostring(2))

def test_program():
    print(f'{"-"*10} Test Program {"-"*10}')
    declarations = [
        VarDeclaration(name="anotherVar", expr=Number(tok=Token(lineno=0, value="10", tipo="Int"))),
        FunctionDeclaration(fun=Function(name="anotherFunction", params=[], body=Block(statements=[]))),
        ClassDeclaration(name="AnotherClass", father="AnotherBaseClass", methods=[
            Function(name="method1", params=[], body=Block(statements=[]))
        ])
    ]
    print(Program(declarations=declarations).tostring(2))

def test_factor():
    print(f'{"-"*10} Test Factor {"-"*10}')
    print(Factor(op="+", first_un=Unary(op="^", atr=Number(tok=Token(lineno=0, value="15", tipo="Int"))), second_un=Number(tok=Token(lineno=0, value="25", tipo="Int"))).tostring(2))

def test_all():
    print(f'{"-"*10} Test All {"-"*10}')
    test_number()
    test_unary()
    test_primary()
    test_call()
    test_function()
    test_class_declaration()
    test_function_declaration()
    test_var_declaration()
    test_program()
    test_factor()

if __name__ == "__main__":
    test_all()


=======
>>>>>>> ac704d2b4d73596ecbbaf2a1cc3dfe1217ce59f1
