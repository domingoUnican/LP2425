from Representacion import (
    Token, Unary, Factor, Term, Comparison, Equality, LogicAnd, LogicOr,
    AssignmentLogicOr, AssignmentExpression, Assignment, Primary, Call, Arguments,
    Parameters, Function, Block, ReturnStatement, PrintStatement, IfStatement,
    WhileStatement, ForStatement, ExpressionStatement, VariableDeclaration,
    FunctionDeclaration, ClassDeclaration, Program
)

def test_unary_tostring():
    print("=== test_unary_tostring ===")
    unary = Unary(Token(1, "42", "TNumber"))
    print(unary.tostring(0))

def test_factor_tostring():
    print("=== test_factor_tostring ===")
    unary1 = Unary(Token(1, "5", "TNumber"))
    unary2 = Unary(Token(1, "3", "TNumber"))
    factor = Factor(unary1, [(Token(1, "/", "Operator"), unary2)])
    print(factor.tostring(0))

def test_term_tostring():
    print("=== test_term_tostring ===")
    u1 = Unary(Token(1, "1", "TNumber"))
    u2 = Unary(Token(1, "2", "TNumber"))
    f1 = Factor(u1, [])
    f2 = Factor(u2, [])
    term = Term(f1, [(Token(1, "+", "Operator"), f2)])
    print(term.tostring(0))

def test_comparison_tostring():
    print("=== test_comparison_tostring ===")
    u1 = Unary(Token(1, "1", "TNumber"))
    u2 = Unary(Token(1, "2", "TNumber"))
    f1 = Factor(u1, [])
    f2 = Factor(u2, [])
    t1 = Term(f1, [])
    t2 = Term(f2, [])
    comp = Comparison(t1, [(Token(1, "<", "Operator"), t2)])
    print(comp.tostring(0))

def test_equality_tostring():
    print("=== test_equality_tostring ===")
    u1 = Unary(Token(1, "1", "TNumber"))
    u2 = Unary(Token(1, "2", "TNumber"))
    f1 = Factor(u1, [])
    f2 = Factor(u2, [])
    t1 = Term(f1, [])
    t2 = Term(f2, [])
    c1 = Comparison(t1, [])
    c2 = Comparison(t2, [])
    eq = Equality(c1, [(Token(1, "==", "Operator"), c2)])
    print(eq.tostring(0))

def test_logicand_tostring():
    print("=== test_logicand_tostring ===")
    u1 = Unary(Token(1, "1", "TNumber"))
    u2 = Unary(Token(1, "2", "TNumber"))
    f1 = Factor(u1, [])
    f2 = Factor(u2, [])
    t1 = Term(f1, [])
    t2 = Term(f2, [])
    c1 = Comparison(t1, [])
    c2 = Comparison(t2, [])
    eq1 = Equality(c1, [])
    eq2 = Equality(c2, [])
    land = LogicAnd(eq1, [(Token(1, "&&", "Operator"), eq2)])
    print(land.tostring(0))

def test_logicor_tostring():
    print("=== test_logicor_tostring ===")
    u1 = Unary(Token(1, "1", "TNumber"))
    u2 = Unary(Token(1, "2", "TNumber"))
    f1 = Factor(u1, [])
    f2 = Factor(u2, [])
    t1 = Term(f1, [])
    t2 = Term(f2, [])
    c1 = Comparison(t1, [])
    c2 = Comparison(t2, [])
    eq1 = Equality(c1, [])
    eq2 = Equality(c2, [])
    land1 = LogicAnd(eq1, [])
    land2 = LogicAnd(eq2, [])
    lor = LogicOr(land1, [(Token(1, "||", "Operator"), land2)])
    print(lor.tostring(0))

def test_assignmentlogicor_tostring():
    print("=== test_assignmentlogicor_tostring ===")
    u = Unary(Token(1, "1", "TNumber"))
    f = Factor(u, [])
    t = Term(f, [])
    c = Comparison(t, [])
    eq = Equality(c, [])
    land = LogicAnd(eq, [])
    lor = LogicOr(land, [])
    assignlor = AssignmentLogicOr(lor)
    print(assignlor.tostring(0))

def test_assignmentexpression_tostring():
    print("=== test_assignmentexpression_tostring ===")
    class DummyAssignment(Assignment):
        def tostring(self, n=0):
            return " " * n + "DummyAssignment\n"
    assign = AssignmentExpression(
        llamada=None,
        identifier=Token(1, "x", "TIdentifier"),
        value=DummyAssignment()
    )
    print(assign.tostring(0))

def test_primary_tostring_token():
    print("=== test_primary_tostring_token ===")
    tok = Token(1, "42", "TNumber")
    prim = Primary(tok)
    print(prim.tostring(0))

def test_primary_tostring_expression():
    print("=== test_primary_tostring_expression ===")
    expr = Unary(Token(1, "99", "TNumber"))
    prim = Primary(expr)
    print(prim.tostring(0))

def test_call_tostring():
    print("=== test_call_tostring ===")
    prim = Primary(Token(1, "foo", "TIdentifier"))
    args = [Arguments(Unary(Token(1, "1", "TNumber")), [Unary(Token(1, "2", "TNumber"))])]
    call = Call(prim, args)
    print(call.tostring(0))

def test_parameters_tostring():
    print("=== test_parameters_tostring ===")
    params = Parameters(Token(1, "a", "TIdentifier"), [Token(1, "b", "TIdentifier")])
    print(params.tostring(0))

def test_function_tostring():
    print("=== test_function_tostring ===")
    params = Parameters(Token(1, "a", "TIdentifier"), [])
    block = Block([])
    func = Function(Token(1, "foo", "TIdentifier"), params, block)
    print(func.tostring(0))

def test_block_tostring():
    print("=== test_block_tostring ===")
    var_decl = VariableDeclaration(Token(1, "x", "TIdentifier"), Token(1, "int", "TType"), None)
    block = Block([var_decl])
    print(block.tostring(0))

def test_returnstatement_tostring():
    print("=== test_returnstatement_tostring ===")
    ret = ReturnStatement(Unary(Token(1, "1", "TNumber")))
    print(ret.tostring(0))

def test_printstatement_tostring():
    print("=== test_printstatement_tostring ===")
    ps = PrintStatement(Unary(Token(1, "1", "TNumber")))
    print(ps.tostring(0))

def test_ifstatement_tostring():
    print("=== test_ifstatement_tostring ===")
    cond = Unary(Token(1, "cond", "TIdentifier"))
    body = Block([])
    else_body = Block([])
    ifstmt = IfStatement(cond, body, else_body)
    print(ifstmt.tostring(0))

def test_whilestatement_tostring():
    print("=== test_whilestatement_tostring ===")
    cond = Unary(Token(1, "cond", "TIdentifier"))
    body = Block([])
    ws = WhileStatement(cond, body)
    print(ws.tostring(0))

def test_forstatement_tostring():
    print("=== test_forstatement_tostring ===")
    init = VariableDeclaration(Token(1, "i", "TIdentifier"), Token(1, "int", "TType"), None)
    cond = Unary(Token(1, "cond", "TIdentifier"))
    step = Unary(Token(1, "step", "TIdentifier"))
    body = Block([])
    fs = ForStatement(init, cond, step, body)
    print(fs.tostring(0))

def test_expressionstatement_tostring():
    print("=== test_expressionstatement_tostring ===")
    expr = Unary(Token(1, "x", "TIdentifier"))
    es = ExpressionStatement(expr)
    print(es.tostring(0))

def test_variabledeclaration_tostring():
    print("=== test_variabledeclaration_tostring ===")
    var_decl = VariableDeclaration(Token(1, "x", "TIdentifier"), Token(1, "int", "TType"), None)
    print(var_decl.tostring(0))

def test_functiondeclaration_tostring():
    print("=== test_functiondeclaration_tostring ===")
    params = Parameters(Token(1, "a", "TIdentifier"), [])
    block = Block([])
    func = Function(Token(1, "foo", "TIdentifier"), params, block)
    func_decl = FunctionDeclaration(Token(1, "foo", "TIdentifier"), func)
    print(func_decl.tostring(0))

def test_classdeclaration_tostring():
    print("=== test_classdeclaration_tostring ===")
    func = Function(Token(1, "foo", "TIdentifier"), None, Block([]))
    class_decl = ClassDeclaration(Token(1, "C", "TIdentifier"), Token(1, "Base", "TIdentifier"), [func])
    print(class_decl.tostring(0))

def test_program_tostring():
    print("=== test_program_tostring ===")
    var_decl = VariableDeclaration(Token(1, "x", "TIdentifier"), Token(1, "int", "TType"), None)
    prog = Program([var_decl])
    print(prog.tostring(0))

# Run all tests
if __name__ == "__main__":
    test_unary_tostring()
    test_factor_tostring()
    test_term_tostring()
    test_comparison_tostring()
    test_equality_tostring()
    test_logicand_tostring()
    test_logicor_tostring()
    test_assignmentlogicor_tostring()
    test_assignmentexpression_tostring()
    test_primary_tostring_token()
    test_primary_tostring_expression()
    test_call_tostring()
    test_parameters_tostring()
    test_function_tostring()
    test_block_tostring()
    test_returnstatement_tostring()
    test_printstatement_tostring()
    test_ifstatement_tostring()
    test_whilestatement_tostring()
    test_forstatement_tostring()
    test_expressionstatement_tostring()
    test_variabledeclaration_tostring()
    test_functiondeclaration_tostring()
    test_classdeclaration_tostring()
    test_program_tostring()
