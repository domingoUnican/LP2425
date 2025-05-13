from Representacion import *
from Lexer import Token

# Crear algunos tokens de prueba
tok1 = Token(lineno=1, value="10", tipo="Int")
tok2 = Token(lineno=2, value="20", tipo="Int")

# Crear expresiones básicas
num1 = Number(tok=tok1)
num2 = Number(tok=tok2)

# Crear operaciones unarias
unary_minus = Unary(op="-", atr=num1)
unary_plus = Unary(op="+", atr=num2)

# Crear una operación de Factor
factor_expr = Factor(op="/", first_un=unary_minus, second_un=unary_plus)

# Crear una declaración de variable
var_decl = VarDeclaration(name="x", expr=factor_expr)

# Crear un programa con una sola declaración
program = Program(declarations=[var_decl])

# Imprimir la representación del programa
print(program.tostring(0))
