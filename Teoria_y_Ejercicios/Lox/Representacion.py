from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

@dataclass
<<<<<<< HEAD
class Expression:
    pass

@dataclass
class Primary(Expression):
    tok: Token

    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)  # Aquí ponemos el valor un poco más indentado
        return output
    pass

@dataclass
class Unary(Expression):
    op: str
    atr: List['Primary'] = None  # Esto es para representar call o otro Unary
    
    def tostring(self, n):
        output = " " * n + self.op + "\n"
        for element in self.atr:
            output += element.tostring(n + 2) + "\n"
        return output
=======
class Declaration:
    pass

@dataclass
class Primary:
    pass




@dataclass
class Unary:
    op: str
    atr: Optional["Unary"]=None  # Esto es para representar call o otro Unary

@dataclass
class Call:
    base: Primary
>>>>>>> 4a3593908ba31089da9436bfc305b91f4786bc70

@dataclass
class Number(Primary):
    tok: Token
<<<<<<< HEAD
    
    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)  # Aquí ponemos el valor un poco más indentado
        return output

@dataclass    
class String(Primary):
    tok: Token
    
    def tostring(self, n):
        output = " " * n + str(self.tok.tipo) + "\n"
        output += " " * (n + 2) + str(self.tok.value)  # Aquí ponemos el valor un poco más indentado
        return output

@dataclass
class Call(Expression):
    pass

@dataclass
class CallAtribute(Call):
    base: Primary
    name: str
    others: Call

    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += self.base.tostring(n + 2)
        if self.others:
            output += self.others.tostring(n + 2)
        return output

@dataclass
class CallFunction(Call):
    base: Primary
    arguments: List[Expression]
    others: Call

    def tostring(self, n):
        output = " " * n + "Call\n"
        output += self.base.tostring(n + 2)
        for arg in self.arguments:
            output += arg.tostring(n + 2)
        if self.others:
            output += self.others.tostring(n + 2)
        return output

@dataclass
class Factor(Expression):
    unary: Unary
    other: any

    def tostring(self, n):
        output = self.unary.tostring(n)
        if self.other:
            output += self.other.tostring(n)
        return output

@dataclass
class Term(Expression):
    factor: Factor
    other: any
    
    def tostring(self, n):
        output = self.factor.tostring(n)
        if self.other:
            output += self.other.tostring(n)
        return output

@dataclass
class Comparison(Expression):
    addition: Term
    other: any
    
    def tostring(self, n):
        output = self.addition.tostring(n) + "\n"
        if self.other:
            output += self.other.tostring(n) + "n"
        return output

@dataclass
class Equality(Expression):
    comparison: Comparison
    other: any

    def tostring(self, n):
        output = self.comparison.tostring(n)
        if self.other:
            output += self.other.tostring(n)
        return output

@dataclass
class Logic_and(Expression):
    equality: Equality
    other: any
    
    def tostring(self, n):
        output = self.equality.tostring(n)
        if self.other:
            output += self.other.tostring(n)
        return output

@dataclass
class Logic_or(Expression):
    logic_and: Logic_and
    other: any
    
    def tostring(self, n):
        output = self.logic_and.tostring(n)
        if self.other:
            output += self.other.tostring(n)
        return output

@dataclass
class Assignment(Expression):
    name: str
    expr: any
    
    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += self.expr.tostring(n + 2)
        return output

@dataclass
class Statement:
    pass

@dataclass
class Declaration(Statement):
    pass

@dataclass
class Block(Statement):
    blockDeclarations: List[Declaration]
    
    def tostring(self, n):
        output = " " * n + "Block\n"
        for decl in self.blockDeclarations:
            output += decl.tostring(n + 2)
        return output

@dataclass
class ExprStmt(Statement):
    expr: Expression
    
    def tostring(self, n):
        output = " " * n + "Expression\n"
        output += self.expr.tostring(n + 2)
        return output

@dataclass
class ForStmt(Statement):
    initializer: any
    condition: Expression
    increment: Expression
    body: Block
    
    def tostring(self, n):
        output = " " * n + "For\n"
        if self.initializer:
            output += self.initializer.tostring(n + 2) + "\n"
        output += " " * (n+2) + "CONDITION\n"
        output += self.condition.tostring(n + 2) + "\n"
        output += "\n" + " " * (n+2) + "INCREMENT\n"
        output += self.increment.tostring(n + 2) + "\n"
        output += self.body.tostring(n + 4) + "\n"
        return output

@dataclass
class IfStmt(Statement):
    condition: Expression
    thenBranch: Block
    elseBranch: any

    def tostring(self, n):
        output = " " * n + "If\n"
        output += self.condition.tostring(n + 2) + "\n"
        output += self.thenBranch.tostring(n + 2) + "\n"
        if self.elseBranch:
            output += "Else" +" " * n + "\n"
            output += self.elseBranch.tostring(n + 2)
        return output

@dataclass
class PrintStmt(Statement):
    expr: Expression
    
    def tostring(self, n):
        output = " " * n + "Print\n"
        output += self.expr.tostring(n + 2) + "\n"
        return output

@dataclass
class ReturnStmt(Statement):
    value: Expression
    
    def tostring(self, n):
        output = " " * n + "Return\n"
        output += self.value.tostring(n + 2)
        return output

@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Block
    
    def tostring(self, n):
        output = " " * n + "While\n"
        output += self.condition.tostring(n + 2)  + "\n"
        output += self.body.tostring(n + 2) + "\n"
        return output

@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: Expression

    def tostring(self, n):
        output = " " * n + self.name + "\n"
        output += self.expr.tostring(n + 2) + "\n"
        return output
    
@dataclass
class Function:
    name: str
    params: List[any]  # Se mantiene any como solicitado
    body: Block

    def tostring(self, n):
        output = " " * n + "Function " + self.name + "\n"
        output += "\n" + " " * n + "Arguments" + "\n"
        for param in self.params:
            output += " " * (n + 2) + param + "\n"
        output +=  "\n" + " " * n  + "Body" + "\n"
        output += self.body.tostring(n + 2)
        return output

@dataclass
class FunctionDeclaration(Declaration):
    fun: Function
    
    def tostring(self, n):
        return self.fun.tostring(n)
=======
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
>>>>>>> 4a3593908ba31089da9436bfc305b91f4786bc70

@dataclass
class ClassDeclaration(Declaration):
    name: str
<<<<<<< HEAD
    father: any
    methods: List[Function]

    def tostring(self, n):
        output = " " * n + "NAME " + self.name + "\n"
        if self.father:
            output += " " * (n + 2) + "FATHER " + self.father.name + "\n"
            for method in self.father.methods:
                output += method.tostring(n + 4)
        else:
            output += " " * (n + 2) + "FATHER Object\n"
        for method in self.methods:
            output += method.tostring(n + 2)
        return output
=======
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
>>>>>>> 4a3593908ba31089da9436bfc305b91f4786bc70

@dataclass
class Program:
    declarations: List[Declaration]
<<<<<<< HEAD
    
    def tostring(self, n):
        output = "Program\n"
        for decl in self.declarations:
            output += decl.tostring(n + 2)
        return output



#1234;

print("1234")
num = Primary(Token(1, 1234, "NUMBER"))
print(num.tostring(0))
print("------------------------------------------------")

#12.34;

print("12.34")
num = Primary(Token(1, 12.34, "NUMBER"))
print(num.tostring(0))
print("------------------------------------------------")

#"I am a string"
print("I am a string")
string = Primary(Token(1, "I am a string", "STRING"))
print(string.tostring(0))
print("------------------------------------------------")

#"";    // The empty string.
print("")
string = Primary(Token(1, "", "STRING"))
print(string.tostring(0))
print("------------------------------------------------")

#"123"; // This is a string, not a number.
print("123 is a string not a number")
string = Primary(Token(1, "123", "STRING"))
print(string.tostring(0))
print("------------------------------------------------")

#add + me;
print("suma")
operation = Term(Unary("+", [Primary(Token(1, 31, "NUMBER")), Primary(Token(1, 21, "NUMBER"))]), None)
print(operation.tostring(0))
print("------------------------------------------------")

#subtract - me;
print("resta")
operation = Term(Unary("-", [Primary(Token(1, 31, "NUMBER")), Primary(Token(1, 21, "NUMBER"))]), None)  
print(operation.tostring(0))
print("------------------------------------------------")

#multiply * me;
print("multiplicacion")
operation = Factor(Unary("*", [Primary(Token(1, 31, "NUMBER")), Primary(Token(1, 21, "NUMBER"))]), None)
print(operation.tostring(0))
print("------------------------------------------------")

#divide / me;
print("division")
operation = Factor(Unary("/", [Primary(Token(1, 31, "NUMBER")), Primary(Token(1, 21, "NUMBER"))]), None)
print(operation.tostring(0))
print("------------------------------------------------")

#-negateMe;
print("negate")
operation = Unary("-", [Primary(Token(1, 31, "NUMBER"))])
print(operation.tostring(0))
print("------------------------------------------------")

#less < than;
print("less than")
lessThan = Comparison(Term(Unary("<", [Primary(Token(1, 1, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]), None), None)
print(lessThan.tostring(0))
print("------------------------------------------------")

#lessThan <= orEqual;
print("less than or equal")
lessThanEqual = Comparison(Term(Unary("<=", [Primary(Token(1, 1, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]),None),None)
print(lessThanEqual.tostring(0))
print("------------------------------------------------")

#greater > than;
print("greater than")
greaterThan = Comparison(Term(Unary(">", [Primary(Token(1, 1, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]), None), None)
print(greaterThan.tostring(0))
print("------------------------------------------------")

#greaterThan >= orEqual;
print("greater than or equal")
greaterThanEqual = Comparison(Term(Unary(">=", [Primary(Token(1, 1, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]), None), None)
print(greaterThanEqual.tostring(0))
print("------------------------------------------------")

#1 == 2;         // false
print("1 == 2")
equality = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 1, "NUMBER")), Primary(Token(1, 2, "NUMBER"))]), None), None), None)
print(equality.tostring(0))
print("------------------------------------------------")

#"cat" != "dog"; // true.
print("cat != dog")
equality = Equality(Comparison(Term(Unary("!=", [Primary(Token(1, "cat", "STRING")), Primary(Token(1, "dog", "STRING"))]), None), None), None)
print(equality.tostring(0))
print("------------------------------------------------")

#314 == "pi"; // false.
print("314 == pi")
equality = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 314, "NUMBER")), Primary(Token(1, "pi", "STRING"))]), None), None), None)
print(equality.tostring(0))
print("------------------------------------------------")

#123 == "123"; // false.
print("123 == 123")
equality = Equality(Comparison(Term(Unary("==", [Primary(Token(1, 123, "NUMBER")), Primary(Token(1, "123", "STRING"))]), None), None), None)
print(equality.tostring(0))
print("------------------------------------------------")

#!true;  // false.
print("not true")
notTrue = Unary("!", [Primary(Token(1, True, "BOOLEAN"))])
print(notTrue.tostring(0))
print("------------------------------------------------")

#!false; // true.
print("not false")
notFalse = Unary("!", [Primary(Token(1, False, "BOOLEAN"))])
print(notFalse.tostring(0))
print("------------------------------------------------")

#true and false; // false.
print("true and false")
trueAndFalse = Logic_and(Equality(Comparison(Term(
    Factor(Unary("and", [Primary(Token(1, True, "BOOLEAN")), 
                         Primary(Token(1, False, "BOOLEAN"))]),None),None),None),None),None)
print(trueAndFalse.tostring(0))
print("------------------------------------------------")

#true and true;  // true.
print("true and true")
trueAndTrue = Logic_and(Equality(Comparison(Term(
    Factor(Unary("and", [Primary(Token(1, True, "BOOLEAN")), 
                         Primary(Token(1, True, "BOOLEAN"))]),None),None),None),None),None)
print(trueAndTrue.tostring(0))
print("------------------------------------------------")

#false or false; // false.
print("false or false")
falseOrFalse = Logic_or(Logic_and(Equality(Comparison(Term(
                Factor(Unary("or", [Primary(Token(1, False, "BOOLEAN")), 
                         Primary(Token(1, False, "BOOLEAN"))]),None),None),None),None),None),None)
print(falseOrFalse.tostring(0))
print("------------------------------------------------")
#true or false;  // true.
print("true or false")
trueOrFalse = Logic_or(Logic_and(Equality(Comparison(Term(
                Factor(Unary("or", [Primary(Token(1, True, "BOOLEAN")), 
                         Primary(Token(1, False, "BOOLEAN"))]),None),None),None),None),None),None)
print(trueOrFalse.tostring(0))
print("------------------------------------------------")

#double operation (33 + 11) * 2
print("double operation")
dobleOp = Unary("*", [Unary("+", [Primary(Token(1, 33, "NUMBER")), Primary(Token(1, 11, "NUMBER"))]), Primary(Token(1, 2, "NUMBER"))])
print(dobleOp.tostring(0))
print("------------------------------------------------")

#var average = (min + max) / 2;
print("Asignacion de la media")
average = Assignment("average", Unary("/", [Unary("+", [Primary(Token(1, "min", "STRING")), Primary(Token(1, "max", "STRING"))]), Primary(Token(1, 2, "NUMBER"))]))
print(average.tostring(0))
print("------------------------------------------------")

#print "Hello, world!";
print("Print Hello, world!")
funcionPrint = PrintStmt(Primary(Token(1, "Hello, world!", "STRING")))
print(funcionPrint.tostring(0))
print("------------------------------------------------")

#print bloque 
# {
#   print "One statement.";
#   print "Two statements.";
# }
print("Print bloque")
funcionPrint = PrintStmt(Primary(Token(1, "One statement.", "STRING")))
funcionPrint2 = PrintStmt(Primary(Token(1, "Two statements.", "STRING")))
block = Block([funcionPrint, funcionPrint2])
print(block.tostring(0))
print("------------------------------------------------")

#If timidin
# if (condition) {
#   print "yes";
# } else {
#   print "no";
# }
print("If timidin")
funcionPrint = PrintStmt(Primary(Token(1, "yes", "STRING")))
funcionPrint2 = PrintStmt(Primary(Token(1, "no", "STRING")))
block = Block([funcionPrint])
block2 = Block([funcionPrint2])
ifStmt = IfStmt(Primary(Token(1, "condition", "STRING")), block, block2)
print(ifStmt.tostring(0))
print("------------------------------------------------")

#ElIf timidin
# if (condition) {
#   print "yes";
# } elif(condition2) {
#   print "no";
# } else {
#   print "puede";
# }
print("ElIf timidin")
funcionPrint = PrintStmt(Primary(Token(1, "yes", "STRING")))
funcionPrint2 = PrintStmt(Primary(Token(1, "no", "STRING")))
funcionPrint3 = PrintStmt(Primary(Token(1, "puede", "STRING")))
block = Block([funcionPrint])
block2 = Block([funcionPrint2])
block3 = Block([funcionPrint3])
ifStmt = IfStmt(Primary(Token(1, "condition", "STRING")), block, IfStmt(Primary(Token(1, "condition2", "STRING")), block2, block3))
print(ifStmt.tostring(0))
print("------------------------------------------------")

#While timidin
# var a = 1;
# while (a < 10) {
#   print a;
#   a = a + 1;
# }
print("While timidin")
var = VarDeclaration("a", Primary(Token(1, 1, "NUMBER")))
funcionPrint = PrintStmt(Primary(Token(1, "a", "NUMBER")))
funcionPrint2 = Assignment("a", Unary("+", [Primary(Token(1, "a", "NUMBER")), Primary(Token(1, 1, "NUMBER"))]))
block = Block([funcionPrint, funcionPrint2])
whileStmt = WhileStmt(Comparison(Term(Factor(
            Unary("<", [Primary(Token(1, 'a', "NUMBER")), Primary(Token(1, 10, "NUMBER"))]), 
            None), None), None), block)
programEntero = Program([var, whileStmt])
print(programEntero.tostring(0))
print("------------------------------------------------")

#For timidin
# for (var a = 1; a < 10; a = a + 1) {
#   print a;
# }
print("For timidin")
var = VarDeclaration("a", Primary(Token(1, 1, "NUMBER")))
funcionPrint = PrintStmt(Primary(Token(1, "a", "NUMBER")))
funcionPrint2 = Assignment("a", Unary("+", [Primary(Token(1, "a", "NUMBER")), Primary(Token(1, 1, "NUMBER"))]))
block = Block([funcionPrint])
forStmt = ForStmt(var, Comparison(Term(Factor(
            Unary("<", [Primary(Token(1, 'a', "NUMBER")), Primary(Token(1, 10, "NUMBER"))]), 
            None), None), None), funcionPrint2, block)
print(forStmt.tostring(0))
print("------------------------------------------------")

#Funciones
# fun printSum(a, b) {
#   print a + b;
# }
print("Funciones")
funcionPrint = PrintStmt(Unary("+", [Primary(Token(1, "a", "NUMBER")), Primary(Token(1, "b", "NUMBER"))]))
funcion = Function("printSum", ["a", "b"], Block([funcionPrint]))
funcionDeclaration = FunctionDeclaration(funcion)
print(funcionDeclaration.tostring(0))
print("------------------------------------------------")

#Return
# fun returnSum(a, b) {
#   return a + b;
# }
print("Return")
funcionPrint = Unary("+", [Primary(Token(1, "a", "NUMBER")), Primary(Token(1, "b", "NUMBER"))])
funcion = Function("returnSum", ["a", "b"], Block([ReturnStmt(funcionPrint)]))
funcionDeclaration = FunctionDeclaration(funcion)
print(funcionDeclaration.tostring(0))
print("------------------------------------------------")

#Closures
# fun addPair(a, b) {
#   return a + b;
# }

# fun identity(a) {
#   return a;
# }

# print identity(addPair)(1, 2);
# print("Closures")
# funcionPrint = Unary("+", [Primary(Token(1, "a", "NUMBER")), Primary(Token(1, "b", "NUMBER"))])
# funcion = Function("addPair", ["a", "b"], Block([ReturnStmt(funcionPrint)]))
# funcionDeclaration = FunctionDeclaration(funcion)

#Clases
# class Breakfast {
#   cook() {
#     print "Eggs a-fryin'!";
#   }

#   serve(who) {
#     print "Enjoy your breakfast, " + who + ".";
#   }
# }
print("Clases")
funcionPrint = PrintStmt(Primary(Token(1, "Eggs a-fryin'!", "STRING")))
funcion = Function("cook", [], Block([funcionPrint]))
funcionPrint2 = PrintStmt(Unary("+", [Unary("+", [Primary(Token(1, "Enjoy your breakfast, ", "STRING")), 
                                                  Primary(Token(1, "who", "STRING"))]), Primary(Token(1, ".", "STRING"))]))
funcion2 = Function("serve", ["who"], Block([funcionPrint2]))
claseBF = ClassDeclaration("Breakfast", None, [funcion, funcion2])
print(claseBF.tostring(0))
print("------------------------------------------------")

#Instancia Breakfast
# var breakfast = Breakfast();
# print breakfast; // "Breakfast instance".
print("Instancia Breakfast")
var = VarDeclaration("breakfast", CallAtribute(Primary(Token(1, "Breakfast", "CLASS")), "Breakfast()", None))
printStmt = PrintStmt(var)
programEntero = Program([var, printStmt])
print(programEntero.tostring(0))
print("------------------------------------------------")

#Herencia Breakfast
# class Brunch < Breakfast {
#   drink() {
#     print "How about a Bloody Mary?";
#   }
# }
print("Herencia Breakfast")
funcionPrint = PrintStmt(Primary(Token(1, "How about a Bloody Mary?", "STRING")))
funcion = Function("drink", [], Block([funcionPrint]))
clase = ClassDeclaration("Brunch", claseBF, [funcion])
print(clase.tostring(0))
print("------------------------------------------------")
=======
>>>>>>> 4a3593908ba31089da9436bfc305b91f4786bc70
