# AstPrinter.py
# Este código es una implementación en Python del intérprete Lox,
# basada en el libro "Crafting Interpreters" de Robert Nystrom:
# https://craftinginterpreters.com/
__author__ = "Rubén Martínez Amodia"
__version__ = "2025"

from Representacion import *
from Scanner import Token, TokenType


class AstPrinter(ExprVisitor, StmtVisitor):
    """
    Permite visualizar el árbol que representa el código Lox de dos maneras:

      (1) como se pide en la práctica;
      (2) como se define en el libro "crafting interpreters".

    Ambas representaciones se ilustran en el main() de este módulo.
    """

    def print(self, expr_or_stmt: Expr | Stmt) -> str:
        return expr_or_stmt.accept(self)

    def visit_block_stmt(self, stmt: Block) -> str:
        return "(block " + "".join(s.accept(self) for s in stmt.statements) + ")"

    def visit_expression_stmt(self, stmt: Expression) -> str:
        return self.parenthesize(";", stmt.expression)

    def visit_function_stmt(self, stmt: Function) -> str:
        params = " ".join(param.lexeme for param in stmt.params)
        body = "".join(s.accept(self) for s in stmt.body)
        return f"(fun {stmt.name.lexeme}({params}) {body})"

    def visit_if_stmt(self, stmt: If) -> str:
        if stmt.else_branch is None:
            return self.parenthesize2("if", stmt.condition, stmt.then_branch)
        return self.parenthesize2(
            "if-else", stmt.condition, stmt.then_branch, stmt.else_branch
        )

    def visit_print_stmt(self, stmt: Print) -> str:
        return self.parenthesize("print", stmt.expression)

    def visit_return_stmt(self, stmt: Return) -> str:
        if stmt.value is None:
            return "(return)"
        return self.parenthesize("return", stmt.value)

    def visit_var_stmt(self, stmt: Var) -> str:
        if stmt.initializer is None:
            return self.parenthesize2("var", stmt.name)
        return self.parenthesize2("var", stmt.name, "=", stmt.initializer)

    def visit_while_stmt(self, stmt: While) -> str:
        return self.parenthesize2("while", stmt.condition, stmt.body)

    def visit_assign_expr(self, expr: Assign) -> str:
        return self.parenthesize2("=", expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr: Call) -> str:
        return self.parenthesize2("call", expr.callee, expr.arguments)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_logical_expr(self, expr: Logical) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: Variable) -> str:
        return expr.name.lexeme

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        return f"({name} {' '.join(expr.accept(self) for expr in exprs)})"

    def parenthesize2(self, name: str, *parts) -> str:
        builder = [f"({name}"]
        builder += self.transform(*parts)
        builder.append(")")
        return " ".join(builder)

    def transform(self, *parts) -> list[str]:
        result = []
        for part in parts:
            if isinstance(part, Expr):
                result.append(part.accept(self))
            elif isinstance(part, Stmt):
                result.append(part.accept(self))
            elif isinstance(part, Token):
                result.append(part.lexeme)
            elif isinstance(part, list):
                result += self.transform(*part)
            else:
                result.append(str(part))
        return result


if __name__ == "__main__":
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    print("Como en la práctica:")
    print(expression.tostring(2))
    print("____________________")
    print("Como en el libro:")
    print(AstPrinter().print(expression))
