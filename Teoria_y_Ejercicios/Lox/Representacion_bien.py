# Import necessary modules
from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional

# -------------------------------------------------
# Clases base
# -------------------------------------------------


@dataclass
class Declaration:
    """
    Clase base para todas las declaraciones en Lox.
    """

    pass


@dataclass
class Expression:
    """
    Clase base para todas las expresiones en Lox.
    """

    pass


# -------------------------------------------------
# Utility Classes
# -------------------------------------------------


@dataclass
class Argument:
    """
    Representa unos argumentos de una función.
    """

    expression: List[Expression]


@dataclass
class Parameter:
    """
    Representa unos parámetros de una función.
    """

    identifier: List[str]


@dataclass
class Function:
    """
    Representa una función en Lox.
    """

    identifier: str
    parameters: Parameter
    body: "Block"


# -------------------------------------------------
# Declaraciones Base
# -------------------------------------------------


@dataclass
class ClassDeclaration(Declaration):
    """
    Representa una declaración de clase en Lox.
    """

    identifier: str
    herency: str
    methods: List[Function]


@dataclass
class FunctionDeclaration(Declaration):
    """
    Declaración de una función.
    """

    function: Function


@dataclass
class VarDeclaration(Declaration):
    """
    Representa la declaración de una variable con su expresión asignada.
    """

    itentifier: str
    expression: Expression


@dataclass
class Statement(Declaration):
    """
    Clase base para las declaraciones que son sentencias.
    """

    pass


# -------------------------------------------------
# Tipos de statements
# -------------------------------------------------


@dataclass
class ExpressionStatement(Statement):
    """
    Representa una sentencia de expresión (expr;).
    """

    expression: Expression


@dataclass
class ForStatement(Statement):
    """
    Representa una sentencia for.
    """

    initializer: Statement
    condition: Expression
    increment: Expression
    body: Statement


@dataclass
class IfStatement(Statement):
    """
    Representa una sentencia if-else.
    """

    condition: Expression
    then_branch: Statement
    else_branch: Statement


@dataclass
class PrintStatement(Statement):
    """
    Representa una sentencia print.
    """

    expression: Expression


@dataclass
class ReturnStatement(Statement):
    """
    Representa una sentencia return.
    """

    value: Expression


@dataclass
class WhileStatement(Statement):
    """
    Representa una sentencia while.
    """

    condition: Expression
    body: Statement


@dataclass
class Block(Statement):
    """
    Representa un bloque de código.
    """

    statements: List[Declaration]


# -------------------------------------------------
# Expresiones
# -------------------------------------------------


@dataclass
class Assignment(Expression):
    pass


class AssignmentExpression(Assignment):
    """
    Representa una expresión de asignación.
    """

    target: "Call"  # llamada a metodo
    itentifier: str
    value: Expression


class AssignmentLogic(Assignment):
    """
    Representa una expresión de asignación logica.
    """

    logica: "LogicOr"


# Logical Expressions
@dataclass
class LogicOr(Expression):
    left: "LogicAnd"
    right: "LogicAnd"


@dataclass
class LogicAnd(Expression):
    left: "Equality"
    right: "Equality"


# Comparison Expressions
@dataclass
class Equality(Expression):
    left: "Comparison"
    operator: str  # '!=' | '=='
    right: "Comparison"


@dataclass
class Comparison(Expression):
    left: "Term"
    operator: str  # '>' | '>=' | '<' | '<='
    right: "Term"


# Arithmetic Expressions
@dataclass
class Term(Expression):
    left: "Factor"
    operator: str  # '-' | '+'
    right: "Factor"


@dataclass
class Factor(Expression):
    left: "Unary"
    operator: str  # '/' | '*'
    right: "Unary"

    def tostring(self, n):
        output = " " * n + self.operator + "\n"
        output += self.left.tostring(n + 2) + "\n"
        output += self.right.tostring(n + 2) + "\n"
        return output


# Unary and Function Calls
@dataclass
class Unary:
    operator: str
    operand: Optional["Unary"] = None  # Esto es para representar call o otro Unary


@dataclass
class Call(Expression):
    callee: Expression
    arguments: List[Expression]


# Primary Expressions (constants, identifiers, literals)
@dataclass
class Primary(Expression):
    value: Optional[Token]  # Puede ser IDENTIFIER, NUMBER, STRING, etc.
    special: Optional[str] = None  # 'true', 'false', 'nil', 'this', 'super.IDENTIFIER'

    def tostring(self, n):
        if self.special:
            return " " * n + self.special + "\n"
        output = " " * n + self.value.tipo + "\n"
        output += " " * (n + 2) + self.value.value
        return output


# -------------------------------------------------
# Programa principal
# -------------------------------------------------


@dataclass
class Program:
    """
    Representa un programa completo en Lox, compuesto por múltiples declaraciones.
    """

    declarations: List[Declaration]


# PARA PROBAR
if __name__ == "__main__":
    token1 = Token(lineno=0, value="10", tipo="Int")
    token2 = Token(lineno=0, value="10", tipo="Int")
    factor = Factor(
        operator="/", left=Primary(value=token1), right=Primary(value=token2)
    )
    print(factor.tostring(2))
