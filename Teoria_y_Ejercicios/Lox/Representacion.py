# Representacion.py
# Este código es una implementación en Python del intérprete Lox,
# basada en el libro "Crafting Interpreters" de Robert Nystrom:
# https://craftinginterpreters.com/
__author__ = "Rubén Martínez Amodia"
__version__ = "2025"

from abc import ABC, abstractmethod

from Scanner import Token


class ExprVisitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: "Assign"):
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: "Binary"):
        pass

    @abstractmethod
    def visit_call_expr(self, expr: "Call"):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping"):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal"):
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: "Logical"):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary"):
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: "Variable"):
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        pass

    @abstractmethod
    def tostring(self, n):
        pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign_expr(self)

    def tostring(self, n):
        output = " " * n + f"assign {self.name.lexeme}\n"
        output += self.value.tostring(n + 2)
        return output


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)

    def tostring(self, n):
        output = " " * n + f"binary {self.operator.lexeme}\n"
        output += self.left.tostring(n + 2) + "\n"
        output += self.right.tostring(n + 2)
        return output


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call_expr(self)

    def tostring(self, n):
        output = " " * n + "call\n"
        output += self.callee.tostring(n + 2) + "\n"
        for arg in self.arguments:
            output += arg.tostring(n + 2) + "\n"
        return output.strip()


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)

    def tostring(self, n):
        output = " " * n + "grouping\n"
        output += self.expression.tostring(n + 2)
        return output


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)

    def tostring(self, n):
        return " " * n + f"literal {self.value}"


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical_expr(self)

    def tostring(self, n):
        output = " " * n + f"logical {self.operator.lexeme}\n"
        output += self.left.tostring(n + 2) + "\n"
        output += self.right.tostring(n + 2)
        return output


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)

    def tostring(self, n):
        output = " " * n + f"unary {self.operator.lexeme}\n"
        output += self.right.tostring(n + 2)
        return output


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)

    def tostring(self, n):
        return " " * n + f"variable {self.name.lexeme}"


class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: "Block"):
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression"):
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt: "Function"):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: "If"):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print"):
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt: "Return"):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: "Var"):
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: "While"):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        pass

    @abstractmethod
    def tostring(self, n):
        pass


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_block_stmt(self)

    def tostring(self, n):
        output = " " * n + "block\n"
        for stmt in self.statements:
            output += stmt.tostring(n + 2) + "\n"
        return output.strip()


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression_stmt(self)

    def tostring(self, n):
        return " " * n + "expression\n" + self.expression.tostring(n + 2)


class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_function_stmt(self)

    def tostring(self, n):
        output = " " * n + f"function {self.name.lexeme}(\n"
        for param in self.params:
            output += " " * (n + 2) + param.lexeme + "\n"
        output += " " * n + ")\n"
        for body_stmt in self.body:
            output += body_stmt.tostring(n + 2) + "\n"
        return output


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_if_stmt(self)

    def tostring(self, n):
        output = " " * n + "if\n"
        output += self.condition.tostring(n + 2) + "\n"
        output += self.then_branch.tostring(n + 2) + "\n"
        if self.else_branch:
            output += self.else_branch.tostring(n + 2) + "\n"
        return output.strip()


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)

    def tostring(self, n):
        return " " * n + "print\n" + self.expression.tostring(n + 2)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr | None):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_return_stmt(self)

    def tostring(self, n):
        output = " " * n + "return\n"
        if self.value:
            output += self.value.tostring(n + 2) + "\n"
        return output


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_var_stmt(self)

    def tostring(self, n):
        output = " " * n + f"var {self.name.lexeme}\n"
        if self.initializer:
            output += " " * (n + 2) + "= \n" + self.initializer.tostring(n + 2)
        return output


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_while_stmt(self)

    def tostring(self, n):
        output = " " * n + "while\n"
        output += self.condition.tostring(n + 2) + "\n"
        output += self.body.tostring(n + 2) + "\n"
        return output.strip()
