from Representacion import *
from Lexer import Token

def test_simple_expression():
    # Create a simple binary expression: 10 + 5
    num1 = Number(Token(lineno=1, tipo="NUMBER", value="10"))
    num2 = Number(Token(lineno=1, tipo="NUMBER", value="5"))
    plus_token = Token(lineno=1, tipo="+", value="+")
    binary_expr = Binary(left=num1, operator=plus_token, right=num2)
    
    print("Test Binary Expression:")
    print(binary_expr.tostring())
    print("\n" + "="*50 + "\n")

def test_variable_declaration():
    # Create a variable declaration: var x = 42;
    num = Number(Token(lineno=1, tipo="NUMBER", value="42"))
    var_decl = VarDeclaration(name="x", expr=num)
    
    print("Test Variable Declaration:")
    print(var_decl.tostring())
    print("\n" + "="*50 + "\n")

def test_if_statement():
    # Create an if statement: if (true) print "yes"; else print "no";
    true_literal = Literal(value="true")
    yes_string = Literal(value="yes")
    no_string = Literal(value="no")
    
    then_branch = PrintStmt(expression=yes_string)
    else_branch = PrintStmt(expression=no_string)
    
    if_stmt = IfStmt(condition=true_literal, then_branch=then_branch, else_branch=else_branch)
    
    print("Test If Statement:")
    print(if_stmt.tostring())
    print("\n" + "="*50 + "\n")

def test_function_declaration():
    # Create a function: fun add(a, b) { return a + b; }
    param_a = Parameter(name="a")
    param_b = Parameter(name="b")
    
    # Variable references for a and b
    a_ref = Literal(value="a")
    b_ref = Literal(value="b")
    
    # a + b expression
    plus_token = Token(lineno=1, tipo="+", value="+")
    sum_expr = Binary(left=a_ref, operator=plus_token, right=b_ref)
    
    # return statement
    return_stmt = ReturnStmt(keyword=Token(lineno=1, tipo="return", value="return"), value=sum_expr)
    
    # function body
    body = Block(statements=[return_stmt])
    
    # function declaration
    func = Function(name="add", params=[param_a, param_b], body=body)
    func_decl = FunctionDeclaration(fun=func)
    
    print("Test Function Declaration:")
    print(func_decl.tostring())
    print("\n" + "="*50 + "\n")

def test_complete_program():
    # Create a small program with multiple elements
    
    # 1. Variable declaration
    num = Number(Token(lineno=1, tipo="NUMBER", value="42"))
    var_decl = VarDeclaration(name="x", expr=num)
    
    # 2. If statement
    x_ref = Literal(value="x")
    zero = Number(Token(lineno=2, tipo="NUMBER", value="0"))
    gt_token = Token(lineno=2, tipo=">", value=">")
    condition = Binary(left=x_ref, operator=gt_token, right=zero)
    
    msg1 = Literal(value="Positive")
    msg2 = Literal(value="Not positive")
    
    then_branch = PrintStmt(expression=msg1)
    else_branch = PrintStmt(expression=msg2)
    
    if_stmt = IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)
    
    # Create program
    program = Program(declarations=[var_decl, if_stmt])
    
    print("Test Complete Program:")
    print(program.tostring())
    print("\n" + "="*50 + "\n")


from Representacion import Number, Binary
from Lexer import Token

def test_nested_operations():
    # Expression: (1+2*3)-4
    n1 = Number(Token(lineno=1, tipo="NUMBER", value="1"))
    n2 = Number(Token(lineno=1, tipo="NUMBER", value="2"))
    n3 = Number(Token(lineno=1, tipo="NUMBER", value="3"))
    n4 = Number(Token(lineno=1, tipo="NUMBER", value="4"))
    
    plus_token = Token(lineno=1, tipo="+", value="+")
    mul_token = Token(lineno=1, tipo="*", value="*")
    sub_token = Token(lineno=1, tipo="-", value="-")
    
    # 2 * 3
    mult_expr = Binary(left=n2, operator=mul_token, right=n3)
    # 1 + (2*3)
    add_expr = Binary(left=n1, operator=plus_token, right=mult_expr)
    # (1+2*3) - 4
    expr = Binary(left=add_expr, operator=sub_token, right=n4)
    
    print("Nested Operations Expression:")
    print(expr.tostring())



if __name__ == "__main__":
    test_simple_expression()
    test_variable_declaration()
    test_if_statement()
    test_function_declaration()
    test_complete_program()
    test_nested_operations()
