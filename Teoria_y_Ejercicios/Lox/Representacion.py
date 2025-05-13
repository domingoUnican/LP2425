from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional


class ExprVisitor:
    def visit_assign_expr(self, expr: "Assign"):
        pass
    def visit_binary_expr(self, expr: "Binary"):
        pass
    def visit_call_expr(self, expr: "Call"):
        pass
    def visit_get_expr(self, expr: "Get"):
        pass
    def visit_grouping_expr(self, expr: "Grouping"):
        pass
    def visit_literal_expr(self, expr: "Literal"):
        pass
    def visit_logical_expr(self, expr: "Logical"):
        pass
    def visit_set_expr(self, expr: "Set"):
        pass
    def visit_super_expr(self, expr: "Super"):
        pass
    def visit_this_expr(self, expr: "This"):
        pass
    def visit_unary_expr(self, expr: "Unary"):
        pass    
    def visit_variable_expr(self, expr: "Variable"):
        pass


class Expr:
    def acept(self, visitor: ExprVisitor):
        pass

    def tostring(self, n):
        pass



class Assign(Expr): 
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def acept(self, visitor):
        return visitor.visit_assign_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Assign\n"
        output += " " * (n + 2) + self.name.tipo + "\n"
        output += self.value.tostring(n + 2)
        return output


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.op = operator
        self.right = right

    def acept(self, visitor):
        return visitor.visit_binary_expr(self)
    
    def tostring(self, n):
        output = " " * n + self.op.tipo + "\n"
        output += self.left.tostring(n + 2)
        output += self.right.tostring(n + 2)
        return output
    

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, args: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.args = args

    def acept(self, visitor):
        return visitor.visit_call_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Call\n"
        output += self.callee.tostring(n + 2)
        for arg in self.args:
            output += arg.tostring(n + 2)
        return output
    

class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object = object
        self.name = name

    def acept(self, visitor):
        return visitor.visit_get_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Get\n"
        output += self.object.tostring(n + 2)
        output += " " * (n + 2) + self.name.tipo + "\n"
        return output
    

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def acept(self, visitor):
        return visitor.visit_grouping_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Grouping\n"
        output += self.expression.tostring(n + 2)
        return output
    

class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def acept(self, visitor):
        return visitor.visit_literal_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Literal\n"
        output += " " * (n + 2) + self.value.tipo + "\n"
        return output
    

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.op = operator
        self.right = right

    def acept(self, visitor):
        return visitor.visit_logical_expr(self)
    
    def tostring(self, n):
        output = " " * n + self.op.tipo + "\n"
        output += self.left.tostring(n + 2)
        output += self.right.tostring(n + 2)
        return output
    

class Set(Expr):
    def __init__(self, keyword: Token, mothod: Token):
        self.keyword = keyword
        self.mothod = mothod

    def acept(self, visitor):
        return visitor.visit_set_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Set\n"
        output += " " * (n + 2) + self.keyword.tipo + "\n"
        output += " " * (n + 2) + self.mothod.tipo + "\n"
        return output
    

class Super(Expr):
    def __init__(self, keyword: Token, method: Token):
        self.keyword = keyword
        self.method = method

    def acept(self, visitor):
        return visitor.visit_super_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Super\n"
        output += " " * (n + 2) + self.keyword.tipo + "\n"
        output += " " * (n + 2) + self.method.tipo + "\n"
        return output
    

class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

    def acept(self, visitor):
        return visitor.visit_this_expr(self)
    
    def tostring(self, n):
        output = " " * n + "This\n"
        output += " " * (n + 2) + self.keyword.tipo + "\n"
        return output
    

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.op = operator
        self.right = right

    def acept(self, visitor):
        return visitor.visit_unary_expr(self)
    
    def tostring(self, n):
        output = " " * n + self.op.tipo + "\n"
        output += self.right.tostring(n + 2)
        return output
    

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def acept(self, visitor):
        return visitor.visit_variable_expr(self)
    
    def tostring(self, n):
        output = " " * n + "Variable\n"
        output += " " * (n + 2) + self.name.tipo + "\n"
        return output
    

class StmtVisitor:
    def visit_block_stmt(self, stmt: "Block"):
        pass
    def visit_class_stmt(self, stmt: "Class"):
        pass
    def visit_expression_stmt(self, stmt: "Expression"):
        pass
    def visit_function_stmt(self, stmt: "Function"):
        pass
    def visit_if_stmt(self, stmt: "If"):
        pass
    def visit_print_stmt(self, stmt: "Print"):
        pass
    def visit_return_stmt(self, stmt: "Return"):
        pass
    def visit_var_stmt(self, stmt: "Var"):
        pass
    def visit_while_stmt(self, stmt: "While"):
        pass


class Stmt:
    def acept(self, visitor: StmtVisitor):
        pass

    def tostring(self, n):
        pass


class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def acept(self, visitor):
        return visitor.visit_block_stmt(self)

    def tostring(self, n):
        output = " " * n + "Block\n"
        for stmt in self.statements:
            output += stmt.tostring(n + 2)
        return output
    

class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def acept(self, visitor):
        return visitor.visit_expression_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Expression\n"
        output += self.expression.tostring(n + 2)
        return output
    

class Function(Stmt):
    def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def acept(self, visitor):
        return visitor.visit_function_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Function: " + self.name.tipo + "\n"
        for param in self.params:
            output += " " * (n + 2) + param.tipo + "\n"
        output += " " * n + ")\n"
        for stmt in self.body:
            output += stmt.tostring(n + 2)
        return output
    

class Class(Stmt):
    def __init__(self, name: Token, superclass: Variable, methods: List[Function]):
        self.name = name
        self.superclass = superclass
        self.methods = methods
        
    def acept(self, visitor):
        return visitor.visit_class_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Class: " + self.name.tipo + "\n"
        if self.superclass:
            output += " " * (n + 2) + "Extends: " + self.superclass.name.tipo + "\n"
        for method in self.methods:
            output += method.tostring(n + 2)
        return output
    

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def acept(self, visitor):
        return visitor.visit_if_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "If\n"
        output += self.condition.tostring(n + 2)
        output += self.then_branch.tostring(n + 2)
        if self.else_branch:
            output += self.else_branch.tostring(n + 2)
        return output
    

class Print(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def acept(self, visitor):
        return visitor.visit_print_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Print\n"
        output += self.value.tostring(n + 2)
        return output
    

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def acept(self, visitor):
        return visitor.visit_return_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Return\n"
        output += self.value.tostring(n + 2)
        return output
    

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def acept(self, visitor):
        return visitor.visit_var_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "Var: " + self.name.tipo + "\n"
        output += self.initializer.tostring(n + 2)
        return output
    

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def acept(self, visitor):
        return visitor.visit_while_stmt(self)
    
    def tostring(self, n):
        output = " " * n + "While\n"
        output += self.condition.tostring(n + 2)
        output += self.body.tostring(n + 2)
        return output