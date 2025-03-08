from dataclasses import dataclass
from typing import List, Optional
from Lexer import Token

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
class Statement(Declaration):
    """
    Clase base para las declaraciones que son sentencias.
    """

    pass


@dataclass
class Expression:
    """
    Clase base para todas las expresiones en Lox.
    """

    pass


# -------------------------------------------------
# Representación de Expresiones
# -------------------------------------------------


@dataclass
class Primary(Expression):
    """
    Representa una expresión primaria (números, literales, etc.).
    """

    pass


@dataclass
class Unary(Expression):
    """
    Representa una operación unaria (-, !, etc.).
    """

    op: str
    atr: Optional[Expression] = None  # Puede ser otra expresión (unaria o llamada)


@dataclass
class Call(Expression):
    """
    Representa una llamada a función.
    """

    base: Primary


@dataclass
class Factor(Expression):
    """
    Representa una operación binaria de multiplicación o división.
    """

    op: str
    first_un: Unary
    second_un: Unary

    def tostring(self, n: int) -> str:
        output = " " * n + self.op + "\n"
        output += self.first_un.tostring(n + 2) + "\n"
        output += self.second_un.tostring(n + 2) + "\n"
        return output


# -------------------------------------------------
# Lexical Grammar
# -------------------------------------------------


@dataclass
class Number(Primary):
    """
    Representa un número en el lenguaje Lox.
    """

    tok: Token

    def tostring(self, n: int) -> str:
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  # Indentación adicional para el valor
        return output


# -------------------------------------------------
# Statements
# -------------------------------------------------


@dataclass
class ExpressionStatement(Statement):
    """
    Representa una sentencia de expresión (expr;).
    """

    expression: Expression


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

    keyword: Token
    value: Optional[Expression]


@dataclass
class IfStatement(Statement):
    """
    Representa una sentencia if-else.
    """

    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]


@dataclass
class WhileStatement(Statement):
    """
    Representa una sentencia while.
    """

    condition: Expression
    body: Statement


@dataclass
class ForStatement(Statement):
    """
    Representa una sentencia for.
    """

    initializer: Optional[Statement]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: Statement


@dataclass
class Block(Statement):
    """
    Representa un bloque de sentencias dentro de llaves { ... }.
    """

    statements: List[Statement]


# -------------------------------------------------
# Declaraciones (Funciones, Clases y Variables)
# -------------------------------------------------


@dataclass
class Function:
    """
    Representa una función en Lox.
    """

    name: str
    params: List["Parameter"]
    body: "Block"


@dataclass
class FunctionDeclaration(Declaration):
    """
    Declaración de una función.
    """

    fun: Function


@dataclass
class ClassDeclaration(Declaration):
    """
    Representa una declaración de clase en Lox.
    """

    name: str
    father: str
    methods: List[Function]


@dataclass
class VarDeclaration(Declaration):
    """
    Representa la declaración de una variable con su expresión asignada.
    """

    name: str
    expr: "Expression"


# -------------------------------------------------
# Programa principal
# -------------------------------------------------


@dataclass
class Program:
    """
    Representa un programa completo en Lox, compuesto por múltiples declaraciones.
    """

    declarations: List[Declaration]
