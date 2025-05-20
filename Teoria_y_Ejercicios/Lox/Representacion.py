from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

@dataclass
class Declaration:
    atr: Optional["Declaration"]=None

    def tostring(self, n):
        if self.atr is None:
            return ""
        else:
            return self.atr.tostring(n)

@dataclass
class Primary:
    atr: Optional["Unary"]=None  # Esto es para representar "true", "false", "nil", "this", number, string, "." + identifier, "(" + expression + ")", "super" + "." + identifier

    def tostring(self, n):
        if self.atr is None:
            return " "*n + "nil" + "\n"
        else:
            return self.atr.tostring(n)

@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary

    def tostring(self, n):
        if self.atr is None:
            return " "*n + self.op + "\n"
        else:
            output = " "*n + self.op + "\n"
            output += self.atr.tostring(n+2)
            return output

@dataclass
class Call:
    base: Primary
    args: List[Primary]
    identifier: str

    def tostring(self, n):
        if self.args is None:
            if self.identifier is None:
                return self.base.tostring(n+2)
            else:
                return " "*n + self.base.tostring(n+2) + "." + self.identifier + "\n"
        else:
            if self.identifier is None:
                output = " "*n + self.base.tostring(n+2) + "\n"
                output += " "*n + "(\n"
                for arg in self.args:
                    output += arg.tostring(n+2) + "\n"
                output += " "*n + ")" + "\n"
                return output
            else:
                output = self.base.tostring(n)
                output += " "*n + "(\n"
                for arg in self.args:
                    output += arg.tostring(n+2) + "\n"
                output += " "*n + ")" + "\n"
                output += " "*n + "." + self.identifier + "\n"
                return output

    
@dataclass
class Statement(Declaration):
    #atr: Optional["Declaration"]=None
    body: 'Block' = None

    def tostring(self, n):
        return self.body.tostring(n)

@dataclass
class Number(Primary):
    tok: Token = None
    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
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

    def tostring(self, n):
        #output = " "*n + "fun" + "\n"
        output = " "*n + self.name + "\n"
        output += " "*n + "(\n"
        for param in self.params:
            output += param.tostring(n+2) + "\n"
        output += " "*n + ")\n"
        output += " "*n + "{\n"
        output += self.body.tostring(n+2) + "\n"
        output += " "*n + "}\n"
        return output

@dataclass
class ClassDeclaration(Declaration):
    name: str = None
    father: str = None
    methods: List[Function] = None
    #atr: Optional["Declaration"]=None

    def tostring(self, n):
        output = " "*n + "class" + " "
        output += self.name
        if (self.father) :
            output += " < " + self.father + "\n"
        else:
            output += " < " + "Object" + "\n"
        output += " "*(n) + "{" + "\n"
        for method in self.methods:
            output += method.tostring(n+2) + "\n"
        output += " "*(n) + "}" + "\n"
        return output

@dataclass
class FunctionDeclaration(Declaration):
    fun: Function = None

    def tostring(self, n):
        output = " "*n + "fun" + "\n"
        output += self.fun.tostring(n+2) + "\n"
        return output

@dataclass
class VarDeclaration(Declaration):
    name: str = None
    expr: 'Expression' = None

    def tostring(self, n):
        if self.expr is None:
            return " "*n + "var" + "\n" + " "*n + self.name + "\n"
        output = " "*n + "var" + "\n"
        output += " "*n + self.name + " = " + "\n"
        output += self.expr.tostring(n+2)
        return output

@dataclass
class Program:
    declarations: List[Declaration]

    def tostring(self, n):
        output = ""
        for declaration in self.declarations:
            output += declaration.tostring(n) + "\n"
        return output

def test_number():
    print(f'{"-"*10} Test Number {"-"*10}')
    print(Number(tok=Token(lineno=0, value="42", tipo="Int")).tostring(2))

def test_unary():
    print(f'{"-"*10} Test Unary {"-"*10}')
    print(Unary(op="-", atr=Number(tok=Token(lineno=0, value="42", tipo="Int"))).tostring(2))

def test_primary():
    print(f'{"-"*10} Test Primary {"-"*10}')
    print(Primary(atr=Unary(op="!", atr=Number(tok=Token(lineno=0, value="true", tipo="TTrue")))).tostring(2))

def test_call():
    print(f'{"-"*10} Test Call {"-"*10}')
    print(Call(base=Primary(atr=None), args=[Number(tok=Token(lineno=0, value="42", tipo="Int"))], identifier="foo").tostring(2))

def test_function():
    print(f'{"-"*10} Test Function {"-"*10}')
    print(Function(name="myFunction", params=[Number(tok=Token(lineno=0, value="42", tipo="Int")), Number(tok=Token(lineno=0, value="24", tipo="Int"))], body=Number(tok=Token(lineno=0, value="42", tipo="Int"))).tostring(2))

def test_class_declaration():
    print(f'{"-"*10} Test ClassDeclaration {"-"*10}')
    print(ClassDeclaration(name="MyClass", father="BaseClass", methods=[]).tostring(2))

def test_function_declaration():
    print(f'{"-"*10} Test FunctionDeclaration {"-"*10}')
    print(FunctionDeclaration(fun=Function(name="myFunction", params=[], body=Number(tok=Token(lineno=0, value="42", tipo="Int")))).tostring(2))

def test_var_declaration():
    print(f'{"-"*10} Test VarDeclaration {"-"*10}')
    print(VarDeclaration(name="myVar", expr=Number(tok=Token(lineno=0, value="42", tipo="Int"))).tostring(2))

def test_program():
    print(f'{"-"*10} Test Program {"-"*10}')
    declarations = [
        VarDeclaration(name="myVar", expr=Number(tok=Token(lineno=0, value="42", tipo="Int"))),
        FunctionDeclaration(fun=Function(name="myFunction", params=[], body=Number(tok=Token(lineno=0, value="42", tipo="Int")))),
        ClassDeclaration(name="MyClass", father="BaseClass", methods=[Function(name="myFunction", params=[], body=Number(tok=Token(lineno=0, value="42", tipo="Int")))])
    ]
    print(Program(declarations=declarations).tostring(2))

def test_factor():
    print(f'{"-"*10} Test Factor {"-"*10}')
    print(Factor(op="*", first_un=Unary(op="-", atr=Number(tok=Token(lineno=0, value="42", tipo="Int"))), second_un=Number(tok=Token(lineno=0, value="5", tipo="Int"))).tostring(2))

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
    '''
    test_number()
    test_unary()
    test_primary()
    test_call()
    test_function()
    test_class_declaration()
    test_function_declaration()
    test_var_declaration()
    test_program()
    '''
    test_all()
    #print(Call(base=Primary(atr=None), args=[Number(tok=Token(lineno=0, value="42", tipo="Int"))], identifier="foo").tostring(2))
    #x = Factor(op="*", first_un=Unary(op="-", atr=Number(tok=Token(lineno=0, value="42", tipo="Int"))), second_un=Unary(op="!", atr=Number(tok=Token(lineno=0, value="true", tipo="Bool")))).tostring(2)
    #print(x)
    
