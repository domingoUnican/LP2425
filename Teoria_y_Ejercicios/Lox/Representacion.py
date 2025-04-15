# Import necessary modules
from ast import expr
from dataclasses import dataclass
import token
from Lexer import Token, TokenType
from typing import List, Optional, Union, Tuple

import Lexer


# -------------------------------------------------
# Programa principal
# -------------------------------------------------


@dataclass
class Program:
    """
    Representa un programa completo en Lox, compuesto por múltiples declaraciones.
    """

    declarations: List["Declaration"]

    def tostring(self, n=0):
        output = " " * n + "Program:\n"
        for declaration in self.declarations:
            output += declaration.tostring(n + 2)
        return output


# -------------------------------------------------
# Clases base
# -------------------------------------------------


@dataclass
class Declaration:
    """
    Clase base para todas las declaraciones en Lox.
    """

    def tostring(self, n=0):
        return " " * n + "Declaration (base class)\n"


@dataclass
class Expression:
    """
    Clase base para todas las expresiones en Lox.
    """

    def tostring(self, n=0):
        return " " * n + "Expression (base class)\n"


# -------------------------------------------------
# Tipos de declaraciones
# -------------------------------------------------


@dataclass
class ClassDeclaration(Declaration):
    """
    Representa una declaración de clase en Lox.
    """

    identifier: "Token"  # Nombre de la clase
    superclass: Optional["Token"]  # Nombre de la clase padre (opcional)
    methods: List["Function"]  # Lista de funciones dentro de la clase

    def tostring(self, n=0):
        output = " " * n + f"ClassDeclaration: {self.identifier.value}\n"
        if self.superclass:
            output += " " * (n + 2) + f"Superclass: {self.superclass.value}\n"
        for method in self.methods:
            output += method.tostring(n + 2)
        return output


@dataclass
class FunctionDeclaration(Declaration):
    """
    Representa la declaración de una función.
    """

    function: "Function"  # Función definida en la declaración

    def tostring(self, n=0):
        output = " " * n + f"FunctionDeclaration: {self.function.identifier.value}\n"
        output += self.function.tostring(n + 2)
        return output


@dataclass
class VarDeclaration(Declaration):
    """
    Representa la declaración de una variable con su expresión asignada.
    """

    identifier: "Token"  # Nombre de la variable
    value: Optional["Expression"]  # Expresión opcional asignada a la variable

    def tostring(self, n=0):
        output = " " * n + f"VarDeclaration: {self.identifier.value}\n"
        if self.value:
            output += self.value.tostring(n + 2)
        return output


@dataclass
class Statement(Declaration):
    """
    Clase base para las declaraciones que son sentencias.
    """

    def tostring(self, n=0):
        return " " * n + "Statement (base class)\n"


# -------------------------------------------------
# Tipos de statements
# -------------------------------------------------


@dataclass
class ExpressionStatement(Statement):
    """
    Representa una sentencia de expresión (expr;).
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

    # Puede ser una declaración de variable o una expresión o None
    initializer: Optional[Union["VarDeclaration", "ExpressionStatement"]]
    condition: Optional["Expression"]  # Puede ser None
    increment: Optional["Expression"]  # Puede ser None
    body: "Statement"  # Cuerpo del bucle

    def tostring(self, n=0):
        output = " " * n + "ForStatement:\n"
        if self.initializer:
            output += " " * (n + 2) + "Initializer:\n"
            output += self.initializer.tostring(n + 4)
        if self.condition:
            output += " " * (n + 2) + "Condition:\n"
            output += self.condition.tostring(n + 4)
        if self.increment:
            output += " " * (n + 2) + "Increment:\n"
            output += self.increment.tostring(n + 4)
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4)
        return output


@dataclass
class IfStatement(Statement):
    """
    Representa una sentencia if-else.
    """

    condition: "Expression"  # Expresión de condición
    then_branch: "Statement"  # Rama del if
    else_branch: Optional["Statement"]  # Rama opcional del else

    def tostring(self, n=0):
        output = " " * n + "IfStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condition.tostring(n + 4)
        output += " " * (n + 2) + "Then Branch:\n"
        output += self.then_branch.tostring(n + 4)
        if self.else_branch:
            output += " " * (n + 2) + "Else Branch:\n"
            output += self.else_branch.tostring(n + 4)
        return output


@dataclass
class PrintStatement(Statement):
    """
    Representa una sentencia print.
    """

    expression: "Expression"  # Expresión a imprimir

    def tostring(self, n=0):
        output = " " * n + "PrintStatement:\n"
        output += self.expression.tostring(n + 2)
        return output


@dataclass
class ReturnStatement(Statement):
    """
    Representa una sentencia return.
    """

    value: Optional["Expression"]  # Puede ser None si es un return vacío

    def tostring(self, n=0):
        output = " " * n + "ReturnStatement:\n"
        if self.value:
            output += self.value.tostring(n + 2)
        return output


@dataclass
class WhileStatement(Statement):
    """
    Representa una sentencia while.
    """

    condition: "Expression"  # Expresión de condición
    body: "Statement"  # Cuerpo del bucle

    def tostring(self, n=0):
        output = " " * n + "WhileStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condition.tostring(n + 4)
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4)
        return output


@dataclass
class Block(Statement):
    """
    Representa un bloque de código.
    """

    statements: List["Declaration"]  # Puede contener múltiples declaraciones

    def tostring(self, n=0):
        output = " " * n + "Block:\n"
        for statement in self.statements:
            output += statement.tostring(n + 2)
        return output


# -------------------------------------------------
# Expresiones
# -------------------------------------------------


@dataclass
class Assignment(Expression):
    """
    Representa una expresión de asignación.
    """

    def tostring(self, n=0):
        return " " * n + "Assignment:\n"


@dataclass
class AssignmentExpression(Assignment):
    """
    Representa una expresión de asignación.
    """

    target: Optional["Call"]  # Llamada a método opcional
    identifier: "Token"  # Nombre de la variable o propiedad
    value: "Assignment"  # La asignación puede anidarse (por la gramática)

    def tostring(self, n=0):
        output = " " * n + "AssignmentExpression:\n"
        output += " " * (n + 2) + "Identifier: " + self.identifier.value + "\n"
        if self.target:
            output += " " * (n + 2) + "Target:\n"
            output += self.target.tostring(n + 4)
        output += " " * (n + 2) + "Value:\n"
        output += self.value.tostring(n + 4)
        return output


@dataclass
class AssignmentLogic(Assignment):
    """
    Representa una expresión de asignación lógica.
    """

    logic: "LogicOr"

    def tostring(self, n=0):
        output = " " * n + "AssignmentLogic:\n"
        output += " " * (n + 2) + "LogicOr:\n"
        output += self.logic.tostring(n + 4)
        return output


# Logical Expressions
@dataclass
class LogicOr(Expression):
    """
    Representa una operación lógica con 'or'.
    """

    left: "LogicAnd"  # La primera expresión lógica
    right: List[Tuple["Token", "LogicAnd"]]  # Lista de pares (operador 'or', expresión)

    def tostring(self, n=0):
        output = " " * n + "LogicOr:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class LogicAnd(Expression):
    """
    Representa una operación lógica con 'and'.
    """

    left: "Equality"  # La primera expresión de comparación
    right: List[
        Tuple["Token", "Equality"]
    ]  # Lista de pares (operador 'and', expresión)

    def tostring(self, n=0):
        output = " " * n + "LogicAnd:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class Equality(Expression):
    """
    Representa una comparación de igualdad ('==' o '!=').
    """

    left: "Comparison"  # Expresión a la izquierda
    right: List[Tuple["Token", "Comparison"]]  # Lista de pares (operador, expresión)

    def tostring(self, n=0):
        output = " " * n + "Equality:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class Comparison(Expression):
    """
    Representa una comparación ('>', '>=', '<', '<=').
    """

    left: "Term"  # Expresión a la izquierda
    right: List[Tuple["Token", "Term"]]  # Lista de pares (operador, expresión)

    def tostring(self, n=0):
        output = " " * n + "Comparison:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class Term(Expression):
    """
    Representa una operación aritmética con suma o resta ('+' o '-').
    """

    left: "Factor"  # Expresión a la izquierda
    right: List[Tuple["Token", "Factor"]]  # Lista de pares (operador, expresión)

    def tostring(self, n=0):
        output = " " * n + "Term:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class Factor(Expression):
    """
    Representa una operación aritmética con multiplicación o división ('*' o '/').
    """

    left: "Unary"  # Expresión a la izquierda
    right: List[Tuple["Token", "Unary"]]  # Lista de pares (operador, expresión)

    def tostring(self, n=0):
        output = " " * n + "Factor:\n"
        output += " " * (n + 2) + "Left:\n"
        output += self.left.tostring(n + 4)
        for operator, right in self.right:
            output += " " * (n + 2) + f"Operator: {operator.value}\n"
            output += " " * (n + 2) + "Right:\n"
            output += right.tostring(n + 4)
        return output


@dataclass
class Unary(Expression):
    """
    Representa una operación unaria como negación lógica o aritmética.
    """

    operator: "Token"  # El operador, "!" o "-"
    operand: Union["Unary", "Call"]  # Puede ser otra expresión unaria o una llamada

    def tostring(self, n=0):
        output = " " * n + "Unary:\n"
        output += " " * (n + 2) + f"Operator: {self.operator.value}\n"
        output += " " * (n + 2) + "Operand:\n"
        output += self.operand.tostring(n + 4)
        return output


@dataclass
class Call(Expression):
    """
    Representa una llamada a función o método.
    """

    callee: "Primary"  # Expresión primaria (función o objeto)
    arguments: List[Union["Argument", "Token"]]  # Argumentos para la llamada o nombres

    def tostring(self, n=0):
        output = " " * n + "Call:\n"
        output += " " * (n + 2) + "Callee:\n"
        output += self.callee.tostring(n + 4)
        for arg in self.arguments:
            output += " " * (n + 2) + "Argument:\n"
            if isinstance(arg, Argument):
                output += arg.tostring(n + 4)
            else:
                output += " " * (n + 4) + f"Token: {arg.value}\n"
        return output


@dataclass
class Primary(Expression):
    """
    Representa una expresión primaria (números, literales, etc.).
    """

    value: Token

    def tostring(self, n=0):
        return " " * n + f"Primary: {self.value.value}\n"


# -------------------------------------------------
# Utility Classes
# -------------------------------------------------


@dataclass
class Argument:
    """
    Representa una lista de argumentos de una función.
    """

    identifier: "Expression"  # Identificador que representa el valor del argumento
    next: Optional["Expression"]  # Argumento siguiente en la lista (opcional)

    def tostring(self, n=0):
        output = " " * n + "Argument:\n"
        output += self.identifier.tostring(n + 2) + "\n"
        if self.next:
            output += self.next.tostring(n + 2)
        return output


@dataclass
class Parameter:
    """
    Representa una lista de parámetros.
    """

    identifier: "Token"  # Identificador que representa el nombre del parámetro
    next: Optional["Parameter"] = None  # Parámetro siguiente en la lista (opcional)

    def tostring(self, n=0):
        output = " " * n + "Parameter: " + str(self.identifier.value) + "\n"
        if self.next:
            output += self.next.tostring(n + 2)
        return output


@dataclass
class Function(Expression):
    """
    Representa una función.
    """

    identifier: "Token"  # Nombre de la función
    parameters: Optional["Parameter"]  # Lista de parámetros de la función o no
    body: "Block"  # Cuerpo de la función, representado como un bloque de código

    def tostring(self, n=0):
        output = " " * n + f"Function: {self.identifier.value}\n"
        if self.parameters:
            output += self.parameters.tostring(n + 2)
        output += self.body.tostring(n + 2)
        return output


# -------------------------------------------------
# PRUEBAS COMPLETAS
# -------------------------------------------------

def separador():
    print("\033[94m" + "-" * 50 + "\033[0m")

def test_program():
    print("Prueba para Program")
    program = Program(declarations=[
        VarDeclaration(
            identifier=Token(lineno=1, value="x", tipo=TokenType.TIdentifier),
            value=Primary(value=Token(lineno=1, value="10", tipo=TokenType.TNumber))
        ),
        FunctionDeclaration(
            function=Function(
                identifier=Token(lineno=1, value="myFunction", tipo=TokenType.TIdentifier),
                parameters=Parameter(
                    identifier=Token(lineno=1, value="param1", tipo=TokenType.TIdentifier)
                ),
                body=Block(statements=[
                    PrintStatement(
                        expression=Primary(value=Token(lineno=1, value="Hello, World!", tipo=TokenType.TString))
                    )
                ])
            )
        )
    ])
    print(program.tostring())
    separador()

def test_class_declaration():
    print("Prueba para ClassDeclaration con métodos")
    class_decl = ClassDeclaration(
        identifier=Token(lineno=1, value="MyClass", tipo=TokenType.TIdentifier),
        superclass=Token(lineno=1, value="SuperClass", tipo=TokenType.TIdentifier),
        methods=[
            Function(
                identifier=Token(lineno=1, value="method1", tipo=TokenType.TIdentifier),
                parameters=None,
                body=Block(statements=[])
            ),
            Function(
                identifier=Token(lineno=1, value="method2", tipo=TokenType.TIdentifier),
                parameters=Parameter(
                    identifier=Token(lineno=1, value="param1", tipo=TokenType.TIdentifier)
                ),
                body=Block(statements=[
                    ReturnStatement(
                        value=Primary(value=Token(lineno=1, value="42", tipo=TokenType.TNumber))
                    )
                ])
            )
        ]
    )
    print(class_decl.tostring())
    separador()

def test_if_statement():
    print("Prueba para IfStatement con else")
    if_stmt = IfStatement(
        condition=Primary(value=Token(lineno=1, value="true", tipo=TokenType.TTrue)),
        then_branch=Block(statements=[
            PrintStatement(
                expression=Primary(value=Token(lineno=1, value="Then branch", tipo=TokenType.TString))
            )
        ]),
        else_branch=Block(statements=[
            PrintStatement(
                expression=Primary(value=Token(lineno=1, value="Else branch", tipo=TokenType.TString))
            )
        ])
    )
    print(if_stmt.tostring())
    separador()

def test_for_statement():
    print("Prueba para ForStatement con todas las partes")
    for_stmt = ForStatement(
        initializer=VarDeclaration(
            identifier=Token(lineno=1, value="i", tipo=TokenType.TIdentifier),
            value=Primary(value=Token(lineno=1, value="0", tipo=TokenType.TNumber))
        ),
        condition=Comparison(
            left=Primary(value=Token(lineno=1, value="i", tipo=TokenType.TIdentifier)),
            right=[(Token(lineno=1, value="<", tipo=TokenType.TLess), Primary(value=Token(lineno=1, value="10", tipo=TokenType.TNumber)))]
        ),
        increment=AssignmentExpression(
            target=None,
            identifier=Token(lineno=1, value="i", tipo=TokenType.TIdentifier),
            value=Primary(value=Token(lineno=1, value="i + 1", tipo=TokenType.TIdentifier))
        ),
        body=Block(statements=[
            PrintStatement(
                expression=Primary(value=Token(lineno=1, value="i", tipo=TokenType.TIdentifier))
            )
        ])
    )
    print(for_stmt.tostring())
    separador()

def test_while_statement():
    print("Prueba para WhileStatement con cuerpo")
    while_stmt = WhileStatement(
        condition=Primary(value=Token(lineno=1, value="false", tipo=TokenType.TFalse)),
        body=Block(statements=[
            PrintStatement(
                expression=Primary(value=Token(lineno=1, value="Looping", tipo=TokenType.TString))
            )
        ])
    )
    print(while_stmt.tostring())
    separador()

def test_call():
    print("Prueba para Call con argumentos")
    call = Call(
        callee=Primary(value=Token(lineno=1, value="myFunc", tipo=TokenType.TIdentifier)),
        arguments=[
            Primary(value=Token(lineno=1, value="arg1", tipo=TokenType.TIdentifier)),
            Primary(value=Token(lineno=1, value="arg2", tipo=TokenType.TIdentifier))
        ]
    )
    print(call.tostring())
    separador()

def test_assignment_logic():
    print("Prueba para AssignmentLogic con lógica compleja")
    assign_logic = AssignmentLogic(
        logic=LogicOr(
            left=LogicAnd(
                left=Equality(
                    left=Comparison(
                        left=Term(
                            left=Factor(
                                left=Unary(
                                    operator=Token(lineno=1, value="-", tipo=TokenType.TMinus),
                                    operand=Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber))
                                ),
                                right=[]
                            ),
                            right=[]
                        ),
                        right=[]
                    ),
                    right=[]
                ),
                right=[]
            ),
            right=[(Token(lineno=1, value="or", tipo=TokenType.TOr), LogicAnd(
                left=Equality(
                    left=Comparison(
                        left=Term(
                            left=Factor(
                                left=Unary(
                                    operator=Token(lineno=1, value="!", tipo=TokenType.TBang),
                                    operand=Primary(value=Token(lineno=1, value="true", tipo=TokenType.TTrue))
                                ),
                                right=[]
                            ),
                            right=[]
                        ),
                        right=[]
                    ),
                    right=[]
                ),
                right=[]
            ))]
        )
    )
    print(assign_logic.tostring())
    separador()

def test_complex_expr():
    print("Prueba para expresión aritmética compleja: 2 + 3 + 4 * 6 / 2 + 4")
    complex_expr = Term(
        left=Factor(
            left=Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)),
            right=[
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber))),
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Factor(
                    left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
                    right=[
                        (Token(lineno=1, value="*", tipo=TokenType.TStar), Primary(value=Token(lineno=1, value="6", tipo=TokenType.TNumber))),
                        (Token(lineno=1, value="/", tipo=TokenType.TSlash), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))
                    ]
                )),
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)))
            ]
        ),
        right=[]
    )
    print(complex_expr.tostring())
    separador()

def test_complex_expr_2():
    print("Prueba para expresión aritmética compleja: (2 + 3) * (4 - 1)")
    complex_expr_2 = Factor(
        left=Term(
            left=Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber)))]
        ),
        right=[(Token(lineno=1, value="*", tipo=TokenType.TStar), Term(
            left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="-", tipo=TokenType.TMinus), Primary(value=Token(lineno=1, value="1", tipo=TokenType.TNumber)))]
        ))]
    )
    print(complex_expr_2.tostring())
    separador()

def test_complex_expr_3():
    print("Prueba para expresión aritmética compleja: 5 + (3 * 2) - 4 / 2")
    complex_expr_3 = Term(
        left=Factor(
            left=Primary(value=Token(lineno=1, value="5", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="+", tipo=TokenType.TPlus), Factor(
                left=Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber)),
                right=[(Token(lineno=1, value="*", tipo=TokenType.TStar), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))])
            )]
        ),
        right=[(Token(lineno=1, value="-", tipo=TokenType.TMinus), Factor(
            left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="/", tipo=TokenType.TSlash), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))])
        )]
    )
    print(complex_expr_3.tostring())
    separador()

def test_complex_program():
    print("Programa que incluye expresiones complejas")
    complex_expr = Term(
        left=Factor(
            left=Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)),
            right=[
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber))),
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Factor(
                    left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
                    right=[
                        (Token(lineno=1, value="*", tipo=TokenType.TStar), Primary(value=Token(lineno=1, value="6", tipo=TokenType.TNumber))),
                        (Token(lineno=1, value="/", tipo=TokenType.TSlash), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))
                    ]
                )),
                (Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)))
            ]
        ),
        right=[]
    )
    complex_expr_2 = Factor(
        left=Term(
            left=Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="+", tipo=TokenType.TPlus), Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber)))]
        ),
        right=[(Token(lineno=1, value="*", tipo=TokenType.TStar), Term(
            left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="-", tipo=TokenType.TMinus), Primary(value=Token(lineno=1, value="1", tipo=TokenType.TNumber)))]
        ))]
    )
    complex_expr_3 = Term(
        left=Factor(
            left=Primary(value=Token(lineno=1, value="5", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="+", tipo=TokenType.TPlus), Factor(
                left=Primary(value=Token(lineno=1, value="3", tipo=TokenType.TNumber)),
                right=[(Token(lineno=1, value="*", tipo=TokenType.TStar), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))])
            )]
        ),
        right=[(Token(lineno=1, value="-", tipo=TokenType.TMinus), Factor(
            left=Primary(value=Token(lineno=1, value="4", tipo=TokenType.TNumber)),
            right=[(Token(lineno=1, value="/", tipo=TokenType.TSlash), Primary(value=Token(lineno=1, value="2", tipo=TokenType.TNumber)))])
        )]
    )
    complex_program = Program(declarations=[
        VarDeclaration(
            identifier=Token(lineno=1, value="a", tipo=TokenType.TIdentifier),
            value=complex_expr
        ),
        VarDeclaration(
            identifier=Token(lineno=1, value="b", tipo=TokenType.TIdentifier),
            value=complex_expr_2
        ),
        VarDeclaration(
            identifier=Token(lineno=1, value="c", tipo=TokenType.TIdentifier),
            value=complex_expr_3
        ),
        PrintStatement(
            expression=Primary(value=Token(lineno=1, value="a", tipo=TokenType.TIdentifier))
        ),
        PrintStatement(
            expression=Primary(value=Token(lineno=1, value="b", tipo=TokenType.TIdentifier))
        ),
        PrintStatement(
            expression=Primary(value=Token(lineno=1, value="c", tipo=TokenType.TIdentifier))
        )
    ])
    print(complex_program.tostring())
    separador()

def run_tests():
    test_program()
    test_class_declaration()
    test_if_statement()
    test_for_statement()
    test_while_statement()
    test_call()
    test_assignment_logic()
    test_complex_expr()
    test_complex_expr_2()
    test_complex_expr_3()
    test_complex_program()

if __name__ == "__main__":
    run_tests()