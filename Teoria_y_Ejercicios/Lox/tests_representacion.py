from Representacion import (
    Unary, Term, Factor, Comparison, Equality,
    Logic_and, Logic_or, Assignment, PrintStmt, ExprStmt,
    ReturnStmt, VarDecl, ForStmt, IfStmt, WhileStmt,
    Function, FunDecl, Program, CallAtribute, CallFunction, ClassDecl,
    Block, Number, String, Identifier, Primary
)
from Lexer import Token, TokenType

# ----- Primarios -----
print("\033[92m# Primarios básicos\033[0m")
print("9876")
print(Number(9876).tostring(0))
print("98.76")
print(Number(98.76).tostring(0))

def print_string(s):
    print(f"\"{s}\"")
    print(String(s).tostring(0))

print_string("Hello there!")
print_string("")
print_string("999 como texto")
print("true boolean")
print(String(True).tostring(0))
print("false boolean")
print(String(False).tostring(0))

# ----- Unarios -----
print("\033[92m# Operaciones unarias\033[0m")
print("negativo")
op = Unary(Token(1, "-", TokenType.TLess), Number(100))
print(op.tostring(0))
print("!true")
op = Unary(Token(1, "!", "BANG"), String("Hola"))
print(op.tostring(0))

# ----- Binarios -----
print("\033[92m# Operaciones binarias\033[0m")
op = Term(
    Number(10),
    Token(1, "+", TokenType.TPlus),
    Number(5)
)
print(op.tostring(0))

op = Factor(
    Number(4),
    Token(1, "*", TokenType.TStar),
    Number(3)
)
print(op.tostring(0))


# Operacion Aritmetica grande
# Representación de la operación (8 + 1 - (9 * 8)) / 10

print("\033[92m# Operacion Aritmetica Grande\033[0m")
op = Factor(
    left=Term(
        left=Term(
            left=Number(8),
            operator=Token(1, "+", TokenType.TPlus),
            right=Number(1)
        ),
        operator=Token(1, "-", TokenType.TMinus),
        right=Factor(
            left=Number(9),
            operator=Token(1, "*", TokenType.TStar),
            right=Number(8)
        )
    ),
    operator=Token(1, "/", TokenType.TSlash),
    right=Number(10)
)

# Imprimir el resultado del toString de la operación compleja
print(op.tostring(0))
# ----- Comparaciones -----
print("\033[92m# Comparaciones\033[0m")
def test_cmp(symbol, lex):
    # Definir los términos
    left_term = Term(
        Number(3),
        Token(1, "+", TokenType.TPlus),
        Number(7)
    )

    cmp = Comparison(left_term, Token(1, symbol, lex), Number(8))
    print(cmp.tostring(0))

for sym, lex in [
    ("<", "LESS"),
    ("<=", "LESS_EQUAL"),
    (">", "GREATER"),
    (">=", "GREATER_EQUAL")
]:
    test_cmp(sym, lex)

# ----- Igualdades -----
print("\033[92m# Igualdades\033[0m")
# Creamos la expresión de la operación (5 + 5 == 10) sin evaluarla
equality_expr = Equality(
    left=Comparison(
        left=Term(
            left=Number(5),
            operator=Token(1, "+", TokenType.TPlus),
            right=Number(5)
        ),
        operator=Token(1, "==", TokenType.TEqual),
        right=Number(10)
    ),
    operator=Token(1, "==", TokenType.TEqual),
    right=Number(10)
)

# Imprimimos el toString de la expresión
print(equality_expr.tostring(0))

# ----- Asignaciones y impresión -----
print("\033[92m# Asignación y print\033[0m")
assign = Assignment(
    "x",
    Term(Number(1), Token(1, "+", TokenType.TPlus), Number(2))
)
print(assign.tostring(0))

print_stmt = PrintStmt(String("¡Hola!"))
print(print_stmt.tostring(0))

expr_stmt = ExprStmt(Number(100))
print(expr_stmt.tostring(0))

# ----- Bloques -----
print("\033[92m# Bloques\033[0m")
block = Block([
    PrintStmt(String("Línea 1")),
    PrintStmt(String("Línea 2"))
])
print(block.tostring(0))

# ----- Control de flujo -----
print("\033[92m# Control de flujo\033[0m")
stmt_if = IfStmt(
    String(True),
    Block([PrintStmt(String("Sí"))]),
    Block([PrintStmt(String("No"))])
)
print(stmt_if.tostring(0))

nested = IfStmt(
    String(True),
    Block([PrintStmt(String("A"))]),
    IfStmt(
        String(False),
        Block([PrintStmt(String("B"))]),
        Block([PrintStmt(String("C"))])
    )
)
print(nested.tostring(0))

decl = VarDecl("i", Number(0))
stmt1 = PrintStmt(Identifier("i"))
stmt2 = Assignment("i", Term(Identifier("i"), Token(1, "+", TokenType.TPlus), Number(1)))
loop_body = Block([stmt1, stmt2])
bucle = WhileStmt(
    Comparison(
        Term(Identifier("i"), Token(1, "<", TokenType.TLess), Number(3)),
        Token(1, "<", TokenType.TLess),
        Number(3)
    ),
    loop_body
)
print(Program([decl, bucle]).tostring(0))

for_stmt = ForStmt(
    VarDecl("j", Number(1)),
    Comparison(
        Term(Identifier("j"), Token(1, "<", TokenType.TLess), Number(4)),
        None,
        None
    ),
    Assignment("j", Term(Identifier("j"), Token(1, "+", TokenType.TPlus), Number(1))),
    Block([PrintStmt(Identifier("j"))])
)
print(for_stmt.tostring(0))

# ----- Funciones -----
print("\033[92m# Funciones\033[0m")
fn_body = Block([PrintStmt(Term(Identifier("x"), Token(1, "+", TokenType.TPlus), Identifier("y")))])
fn = Function("suma", None, fn_body)
print(FunDecl(fn).tostring(0))

ret_stmt = ReturnStmt(Term(Identifier("a"), Token(1, "+", TokenType.TPlus), Identifier("b")))
fn2 = Function("retornaSuma", None, Block([ret_stmt]))
print(FunDecl(fn2).tostring(0))

call_fn = CallFunction(Identifier("suma"), [Number(1), Number(2)], None)
print(call_fn.tostring(0))

# ----- Clases -----
print("\033[92m# Clases e instancias\033[0m")

# Método m1 dentro de la clase C
m1 = Function("m1", None, Block([
    PrintStmt(String("M1"))
]))
cls = ClassDecl("C", None, [m1])
print(cls.tostring(0))

# Instanciación de la clase C
inst = VarDecl("instC", CallAtribute(Identifier("C"), "C()", None))
print(Program([inst]).tostring(0))

# Subclase D que hereda de C y tiene un método m2
m2 = Function("m2", None, Block([
    PrintStmt(String("M2"))
]))
sub = ClassDecl("D", cls, [m2])
print(sub.tostring(0))

