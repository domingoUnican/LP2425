from dataclasses import dataclass, field
from Lexer import Token
from typing import List, Optional, Tuple, Union


# Las clases en el orden en el que aparecen en la gramática

# ---------------------PROGRAM------------------------------------
@dataclass
class Program:
    """
    Representa el programa completo, que consiste en una lista de declaraciones.
    """
    declarations: List["Declaration"]

    def tostring(self, n=0):
        output = " " * n + "Program:\n"
        for declaration in self.declarations:
            output += declaration.tostring(n + 2)
        return output



# ---------------------DECLARATION--------------------------------
@dataclass
class Declaration: # De esta clase se heredan todos los tipos de declaraciones
    """
    Representa una declaración en el programa.
    """
    pass


@dataclass
class ClassDeclaration(Declaration):
    """
    Representa una declaración de clase.
    """
    name: "Token"
    father: Optional["Token"]
    methods: List["Function"]

    def tostring(self, n=0):
        output = " " * n + "ClassDeclaration:\n"
        output += " " * (n + 2) + f"Name: {self.name.value}\n"
        if self.father:
            output += " " * (n + 2) + f"Father: {self.father.value}\n"
        for method in self.methods:
            output += method.tostring(n + 4)
        return output


@dataclass
class FunctionDeclaration(Declaration):
    """
    Representa una declaración de función.
    """
    name: "Token"
    function: "Function"

    def tostring(self, n=0):
        output = " " * n + "FunctionDeclaration:\n"
        output += " " * (n + 2) + f"Name: {self.name.value}\n"
        output += self.function.tostring(n + 2)
        return output


@dataclass
class VariableDeclaration(Declaration):
    """
    Representa una declaración de variable.
    """
    name: "Token"
    type: "Token"
    value: Optional["Expression"]

    def tostring(self, n=0):
        output = " " * n + "VariableDeclaration:\n"
        output += " " * (n + 2) + f"Name: {self.name.value}\n"
        output += " " * (n + 2) + f"Type: {self.type.value}\n"
        if self.value:
            output += self.value.tostring(n + 2)
        return output


@dataclass
class Statement: # De esta clase se heredan todos los tipos de sentencias
    """
    Representa una sentencia en el programa.
    """
    pass


# ---------------------STATEMENTS---------------------------------
@dataclass
class ExpressionStatement(Statement):
    """
    Representa una sentencia de expresión.
    """
    expression: "Expression"

    def tostring(self, n=0):
        output = " " * n + "ExpressionStatement:\n"
        output += self.expression.tostring(n + 2)
        return output


@dataclass
class ForStatement(Statement):
    """
    Representa una sentencia for.
    """
    init: Optional[Union["VariableDeclaration", "ExpressionStatement"]]
    condicion: Optional["Expression"]
    step: Optional["Expression"]
    cuerpo: "Statement"

    def tostring(self, n=0):
        output = " " * n + "ForStatement:\n"
        if self.init:
            output += " " * (n + 2) + "Init:\n"
            output += self.init.tostring(n + 4)
        if self.condicion:
            output += " " * (n + 2) + "Condition:\n"
            output += self.condicion.tostring(n + 4)
        if self.step:
            output += " " * (n + 2) + "Step:\n"
            output += self.step.tostring(n + 4)
        output += " " * (n + 2) + "Body:\n"
        output += self.cuerpo.tostring(n + 4)
        return output


@dataclass
class IfStatement(Statement):
    """
    Representa una sentencia if.
    """
    condicion: "Expression"
    cuerpo: "Statement"
    else_cuerpo: Optional["Statement"]

    def tostring(self, n=0):
        output = " " * n + "IfStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condicion.tostring(n + 4)
        output += " " * (n + 2) + "Body:\n"
        output += self.cuerpo.tostring(n + 4)
        if self.else_cuerpo:
            output += " " * (n + 2) + "Else Body:\n"
            output += self.else_cuerpo.tostring(n + 4)
        return output


@dataclass
class PrintStatement(Statement):
    """
    Representa una sentencia de impresión.
    """
    expression: "Expression"

    def tostring(self, n=0):
        output = " " * n + "PrintStatement:\n"
        output += " " * (n + 2) + "Expression:\n"
        output += self.expression.tostring(n + 4)
        return output


@dataclass
class ReturnStatement(Statement):
    """
    Representa una sentencia de retorno.
    """
    expression: Optional["Expression"]

    def tostring(self, n=0):
        output = " " * n + "ReturnStatement:\n"
        if self.expression:
            output += " " * (n + 2) + "Expression:\n"
            output += self.expression.tostring(n + 4)
        return output


@dataclass
class WhileStatement(Statement):
    """
    Representa una sentencia while.
    """
    condicion: "Expression"
    cuerpo: "Statement"

    def tostring(self, n=0):
        output = " " * n + "WhileStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condicion.tostring(n + 4)
        output += " " * (n + 2) + "Body:\n"
        output += self.cuerpo.tostring(n + 4)
        return output

@dataclass
class Block(Statement):
    """
    Representa un bloque de código.
    """
    statement: List["Declaration"]

    def tostring(self, n=0):
        output = " " * n + "Block:\n"
        for statement in self.statement:
            output += statement.tostring(n + 2)
        return output



#----------------------EXPRESSIONS--------------------------------
@dataclass
class Expression:  # De esta clase se heredan todos los tipos de expresiones
    """
    Representa una expresión en el programa.
    """
    pass

class Assignment(Expression): # De esta clase se heredan todos los tipos de asignaciones
    """
    Representa una expresión de asignación.
    """
    pass

@dataclass
class AssignmentExpression(Expression):
    """
    Representa una expresión de asignación.
    """
    llamada: Optional["Call"]
    identifier: "Token"
    value: "Assignment"

    def tostring(self, n=0):
        output = " " * n + "AssignmentExpression:\n"
        if self.llamada:
            output += " " * (n + 2) + "Call:\n"
            output += self.llamada.tostring(n + 4)
        output += " " * (n + 2) + f"Identifier: {self.identifier.value}\n"
        output += self.value.tostring(n + 4)
        return output


@dataclass
class AssignmentLogicOr(Expression):
    """
    Representa una expresión de asignación lógica.
    """
    logicOr: "LogicOr"

    def tostring(self, n=0):
        output = " " * n + "AssignmentLogicOr:\n"
        output += self.logicOr.tostring(n + 2)
        return output
    

@dataclass
class LogicOr(Expression):
    """
    Representa una expresión lógica OR.
    """
    left: "LogicAnd"
    right: List[Tuple["Token", "LogicAnd"]]

    def tostring(self, n=0):
        output = " " * n + "LogicOr:\n"
        output += self.left.tostring(n + 2)
        for token, logicAnd in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += logicAnd.tostring(n + 4)
        return output


@dataclass
class LogicAnd(Expression):
    """
    Representa una expresión lógica AND.
    """
    left: "Equality"
    right: List[Tuple["Token", "Equality"]]

    def tostring(self, n=0):
        output = " " * n + "LogicAnd:\n"
        output += self.left.tostring(n + 2)
        for token, equality in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += equality.tostring(n + 4)
        return output


@dataclass
class Equality(Expression):
    """
    Representa una expresión de igualdad.
    """
    left: "Comparison"
    right: List[Tuple["Token", "Comparison"]]

    def tostring(self, n=0):
        output = " " * n + "Equality:\n"
        output += self.left.tostring(n + 2)
        for token, comparison in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += comparison.tostring(n + 4)
        return output


@dataclass
class Comparison(Expression):
    """
    Representa una expresión de comparación.
    """
    left: "Term"
    right: List[Tuple["Token", "Term"]]

    def tostring(self, n=0):
        output = " " * n + "Comparison:\n"
        output += self.left.tostring(n + 2)
        for token, term in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += term.tostring(n + 4)
        return output


@dataclass
class Term(Expression):
    """
    Representa una expresión de término.
    """
    left: "Factor"
    right: List[Tuple["Token", "Factor"]]

    def tostring(self, n=0):
        output = " " * n + "Term:\n"
        output += self.left.tostring(n + 2)
        for token, factor in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += factor.tostring(n + 4)
        return output


@dataclass
class Factor(Expression):
    """
    Representa una expresión de factor.
    """
    left: "Unary"
    right: List[Tuple["Token", "Unary"]] 

    def tostring(self, n=0):
        output = " " * n + "Factor:\n"
        output += self.left.tostring(n + 2)
        for token, unary in self.right:
            output += " " * (n + 2) + token.value + "\n"
            output += unary.tostring(n + 4)
        return output


@dataclass
class Unary(Expression):
    """
    Representa una expresión unaria.
    """
    left: "Token"
    right: Optional[Union["Unary", "Call"]] = None

    def tostring(self, n=0):
        output = " " * n + "Unary:\n"
        output += " " * (n + 2) + self.left.value + "\n"
        if self.right:
            output += self.right.tostring(n + 4)
        return output


@dataclass
class Call(Expression):
    """
    Representa una llamada a función.
    """
    primary: "Primary"
    args: List[Union["Arguments", "Token"]]

    def tostring(self, n=0):
        output = " " * n + "Call:\n"
        output += self.primary.tostring(n + 2)
        for arg in self.args:
            if isinstance(arg, Arguments):
                output += arg.tostring(n + 4)
            else:
                output += " " * (n + 4) + arg.value + "\n"
        return output


@dataclass
class Primary(Expression):
    """
    Representa una expresión primaria.
    """
    value: Union["Token", "Expression"] # Puede ser un token (muchos tipos de cosas) o una expresion

    def tostring(self, n=0):
        output = " " * n + "Primary:\n"
        if isinstance(self.value, Token):
            output += " " * (n + 2) + self.value.value + "\n"
        else:
            output += self.value.tostring(n + 2)
        return output



# ---------------------UTILITY RULES-----------------------------
@dataclass
class Function:
    """
    Representa una función.
    """
    identifier: "Token"
    parameters: Optional["Parameters"]
    cuerpo: "Block"

    def tostring(self, n=0):
        output = " " * n + "Function:\n"
        output += " " * (n + 2) + f"Identifier: {self.identifier.value}\n"
        if self.parameters:
            output += self.parameters.tostring(n + 4)
        output += self.cuerpo.tostring(n + 4)
        return output


@dataclass
class Parameters:
    """
    Representa los parámetros de una función.
    """
    left: "Token"
    right: List["Token"]

    def tostring(self, n=0):
        output = " " * n + "Parameters:\n"
        output += " " * (n + 2) + self.left.value + "\n"
        for right in self.right:
            output += " " * (n + 2) + self.left.value + "\n"
        return output


@dataclass
class Arguments:
    """
    Representa los argumentos de una llamada a función.
    """
    left: "Expression"
    right: List["Expression"]

    def tostring(self, n=0):
        output = " " * n + "Arguments:\n"
        output += " " * (n + 2) + self.left.tostring(n + 4)
        for right in self.right:
            output += right.tostring(n + 4)
        return output




