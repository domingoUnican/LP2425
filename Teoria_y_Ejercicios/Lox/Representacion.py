from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional, Tuple

# Clases base para expresiones y declaraciones

@dataclass
class Declaration:
    """
    Corresponde a 'declaration' en la gramática:
        declaration → classDecl
                    | funDecl
                    | varDecl
                    | statement
    """
    def tostring(self, n: int) -> str:
        return " " * n + "Declaration"

@dataclass
class Primary:
    """
    Clase base para todas las expresiones primarias en Lox.
    Las expresiones primarias incluyen:
      - Literales (números, cadenas, true, false, nil)
      - Variables (IDENTIFIER)
      - 'this' y 'super'
      - Agrupamientos: ( expression )
    """
    def tostring(self, n: int = 0) -> str:
        return " " * n + "Primary"

# Expresiones
@dataclass
class Expression:
    """
    Clase base para todas las expresiones de Lox.
    """
    def tostring(self, n: int = 0) -> str:
        return " " * n + "<Expression>"
    
@dataclass
class Literal(Primary):
    """
    Representa un literal (true, false, nil, números, cadenas).
    Almacena el token para saber su tipo y valor (p.ej. TNumber, TString, etc.).
    """
    token: Token

    def tostring(self, n: int = 0) -> str:
        output = " " * n + f"Literal ({self.token.tipo}): {self.token.value}"
        return output
    
@dataclass
class Variable(Primary):
    """
    Representa una variable (un IDENTIFIER).
    """
    name: Token  # IDENTIFIER

    def tostring(self, n: int = 0) -> str:
        return " " * n + f"Variable: {self.name.value}"
    
@dataclass
class This(Expression):
    keyword: Token  # El token 'this'

    def tostring(self, n: int = 0) -> str:
        return " " * n + "This"
    
@dataclass
class Super(Expression):
    keyword: Token  # El token 'super'
    method: Token   # El IDENTIFIER que sigue a 'super.'

    def tostring(self, n: int = 0) -> str:
        return (
            " " * n + "Super\n" +
            " " * (n + 2) + f"Method: {self.method.value}"
        )
@dataclass
class Grouping(Expression):
    """
    Representa un grupo: ( expression )
    """
    expression: Expression

    def tostring(self, n: int = 0) -> str:
        output = " " * n + "Grouping:\n"
        output += self.expression.tostring(n + 2)
        return output
@dataclass
class Unary(Expression):
    """
    unary → ( "!" | "-" ) unary
          | primary
    """
    operator: Token   # p.ej. '!' o '-'
    right: Expression # la subexpresión

    def tostring(self, n: int = 0) -> str:
        output = " " * n + f"Unary: {self.operator.value}\n"
        output += self.right.tostring(n + 2)
        return output


@dataclass
class Binary(Expression):
    """
    Para expresiones con operador binario, p.ej. a + b, a == b, etc.
    Se usa en factor, term, comparison, equality, etc. con distinta precedencia.
    """
    left: Expression
    operator: Token   # p.ej. '+', '-', '==', etc.
    right: Expression

    def tostring(self, n: int = 0) -> str:
        output = " " * n + f"Binary: {self.operator.value}\n"
        output += self.left.tostring(n + 2) + "\n"
        output += self.right.tostring(n + 2)
        return output
@dataclass
class Logical(Expression):
    """
    Para manejar 'logic_or' y 'logic_and' (operadores 'or' y 'and').
    """
    left: Expression
    operator: Token  # 'or' o 'and'
    right: Expression

    def tostring(self, n: int = 0) -> str:
        output = " " * n + f"Logical: {self.operator.value}\n"
        output += self.left.tostring(n + 2) + "\n"
        output += self.right.tostring(n + 2)
        return output
@dataclass
class Assign(Expression):
    """
    assignment → IDENTIFIER "=" assignment
               | ...
    name: El token IDENTIFIER
    value: La expresión a asignar
    """
    name: Token
    value: Expression

    def tostring(self, n: int = 0) -> str:
        output = " " * n + f"Assign to: {self.name.value}\n"
        output += " " * (n + 2) + "Value:\n"
        output += self.value.tostring(n + 4)
        return output



@dataclass
class Call(Expression):
    """
    call → primary ( "(" arguments? ")" | "." IDENTIFIER )*
    Este nodo representa una llamada a función con argumentos.
    """
    callee: Expression         # lo que se llama, p.ej. una Variable o una expresión
    paren: Token               # el token ')' para referencia
    arguments: List[Expression]

    def tostring(self, n: int = 0) -> str:
        output = " " * n + "Call:\n"
        output += " " * (n + 2) + "Callee:\n"
        output += self.callee.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "Arguments:\n"
        for arg in self.arguments:
            output += arg.tostring(n + 4) + "\n"
        return output.rstrip()

@dataclass
class Get(Expression):
    """
    Acceso a una propiedad de un objeto: object.name
    """
    object: Expression
    name: Token  # El IDENTIFIER

    def tostring(self, n: int = 0) -> str:
        output = " " * n + "Get:\n"
        output += " " * (n + 2) + "Object:\n"
        output += self.object.tostring(n + 4) + "\n"
        output += " " * (n + 2) + f"Name: {self.name.value}"
        return output

@dataclass
class Set(Expression):
    """
    Asignación a una propiedad de un objeto: object.name = value
    """
    object: Expression
    name: Token
    value: Expression

    def tostring(self, n: int = 0) -> str:
        output = " " * n + "Set:\n"
        output += " " * (n + 2) + "Object:\n"
        output += self.object.tostring(n + 4) + "\n"
        output += " " * (n + 2) + f"Name: {self.name.value}\n"
        output += " " * (n + 2) + "Value:\n"
        output += self.value.tostring(n + 4)
        return output


@dataclass
class Number(Primary):
    tok: Token
    def tostring(self, n):
        output = " " * n + self.tok.tipo + "\n"
        output += " " * (n + 2) + self.tok.value  # Aquí ponemos el valor un poco más indentado
        return output

# Clase Factor (corregida para seguir la gramática)
# La gramática de Lox para factor es: factor → unary ( ( "/" | "*" ) unary )*
# Por ello representamos un factor como un primer operando y una lista (posiblemente vacía)
# de pares (operador, siguiente operando).
@dataclass
class Factor(Primary):
    first: Unary
    # Cada tupla es (operador: str, siguiente operando: Unary)
    rest: List[Tuple[str, Unary]]
    
    def tostring(self, n: int) -> str:
        # Imprime el primer operando
        output = self.first.tostring(n)
        # Recorre la lista de operaciones adicionales
        for op, operand in self.rest:
            output += "\n" + " " * n + f"Operator: {op}"
            output += "\n" + operand.tostring(n + 2)
        return output

# Clases auxiliares para funciones

@dataclass
class Parameter:
    name: str
    
    def tostring(self, n: int) -> str:
        return " " * n + f"Parameter: {self.name}"

@dataclass
class Block:
    """
    Representa un bloque de sentencias, por ejemplo:
        "{" declaration* "}"
    Se utiliza dentro de funciones, sentencias compuestas, etc.
    """
    declarations: List[Declaration]

    def tostring(self, n: int) -> str:
        output = " " * n + "Block:\n"
        for decl in self.declarations:
            output += decl.tostring(n + 2) + "\n"
        return output.rstrip()

@dataclass
class Function:
    """
    Representa la parte de 'function' en la gramática.
    (funDecl → "fun" function)
    name: Nombre de la función
    params: Parámetros formales
    body: Cuerpo de la función (un bloque de sentencias)
    """
    name: str
    params: List[str]
    body: "Block"

    def tostring(self, n: int) -> str:
        output = " " * n + f"Function: {self.name}\n"
        output += " " * (n + 2) + "Parameters:\n"
        for param in self.params:
            output += " " * (n + 4) + f"{param}\n"
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4)
        return output

# Declaraciones

@dataclass
class ClassDeclaration(Declaration):
    """
    Corresponde a 'classDecl → "class" IDENTIFIER ( "<" IDENTIFIER )? "{" function* "}" ;'
    name: Nombre de la clase
    father: Nombre de la superclase (opcional)
    methods: Lista de funciones (métodos) que van dentro de la clase
    """
    name: str
    father: Optional[str]  # None si no hay ' < IDENTIFIER'
    methods: List["Function"]  # Lista de métodos (definidos como Function)

    def tostring(self, n: int) -> str:
        output = " " * n + f"ClassDeclaration: {self.name}\n"
        if self.father:
            output += " " * (n + 2) + f"SuperClass: {self.father}\n"
        output += " " * (n + 2) + "Methods:\n"
        for method in self.methods:
            output += method.tostring(n + 4) + "\n"
        return output.rstrip()

@dataclass
class FunctionDeclaration(Declaration):
    """
    Corresponde a 'funDecl → "fun" function ;'
    """
    fun: Function

    def tostring(self, n: int) -> str:
        output = " " * n + "FunctionDeclaration:\n"
        output += self.fun.tostring(n + 2)
        return output
@dataclass
class VarDeclaration(Declaration):
    name: str
    expr: Optional[Primary]  # Se usa Primary o Expression según convenga
    
    def tostring(self, n: int) -> str:
        output = " " * n + f"VarDeclaration: {self.name}\n"
        if self.expr:
            output += self.expr.tostring(n + 2)
        return output

@dataclass
class Statement(Declaration):
    def tostring(self, n: int) -> str:
        return " " * n + "Statement"

@dataclass
class Program:
    """
    Corresponde a 'program → declaration* EOF;'
    Contiene una lista de declaraciones (class, fun, var, statement).
    """
    declarations: List[Declaration]

    def tostring(self, n: int = 0) -> str:
        output = " " * n + "Program:\n"
        for decl in self.declarations:
            output += decl.tostring(n + 2) + "\n"
        output += " " * n + "EOF"
        return output.rstrip()

#
# 1. Sentencia de expresión: exprStmt → expression ";"
#
@dataclass
class ExpressionStmt(Statement):
    expr: "Expression"  # Referencia a un nodo de expresión

    def tostring(self, n: int) -> str:
        output = " " * n + "ExpressionStmt:\n"
        output += self.expr.tostring(n + 2)
        return output

#
# 2. Sentencia if: ifStmt → "if" "(" expression ")" statement ( "else" statement )?
#
@dataclass
class IfStatement(Statement):
    condition: "Expression"
    thenBranch: Statement
    elseBranch: Optional[Statement]  # Puede ser None si no existe 'else'

    def tostring(self, n: int) -> str:
        output = " " * n + "IfStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "Then:\n"
        output += self.thenBranch.tostring(n + 4)
        if self.elseBranch:
            output += "\n" + " " * (n + 2) + "Else:\n"
            output += self.elseBranch.tostring(n + 4)
        return output
    
#
# 3. Sentencia print: printStmt → "print" expression ";"
#
@dataclass
class PrintStatement(Statement):
    expr: "Expression"

    def tostring(self, n: int) -> str:
        output = " " * n + "PrintStatement:\n"
        output += self.expr.tostring(n + 2)
        return output

#
# 4. Sentencia return: returnStmt → "return" expression? ";"
#
@dataclass
class ReturnStatement(Statement):
    expr: Optional["Expression"]  # Puede ser None si no hay expresión tras 'return'

    def tostring(self, n: int) -> str:
        output = " " * n + "ReturnStatement:\n"
        if self.expr:
            output += self.expr.tostring(n + 2)
        else:
            output += " " * (n + 2) + "No expression"
        return output

#
# 5. Sentencia while: whileStmt → "while" "(" expression ")" statement
#
@dataclass
class WhileStatement(Statement):
    condition: "Expression"
    body: Statement

    def tostring(self, n: int) -> str:
        output = " " * n + "WhileStatement:\n"
        output += " " * (n + 2) + "Condition:\n"
        output += self.condition.tostring(n + 4) + "\n"
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4)
        return output

#
# 6. Sentencia for: forStmt → "for" "(" ( varDecl | exprStmt | ";" )
#                                 expression? ";"
#                                 expression? ")" statement
#
# En Lox, el for se "desazuca" (desazúcar sintáctico) a un while con
# inicializador, condición, e incremento, pero podemos representarlo
# directamente en el AST si queremos.
#
@dataclass
class ForStatement(Statement):
    initializer: Optional[Declaration]   # Puede ser un VarDeclaration, ExpressionStmt o None
    condition: Optional["Expression"]
    increment: Optional["Expression"]
    body: Statement

    def tostring(self, n: int) -> str:
        output = " " * n + "ForStatement:\n"
        # Initializer
        output += " " * (n + 2) + "Initializer:\n"
        if self.initializer:
            output += self.initializer.tostring(n + 4) + "\n"
        else:
            output += " " * (n + 4) + "None\n"
        # Condition
        output += " " * (n + 2) + "Condition:\n"
        if self.condition:
            output += self.condition.tostring(n + 4) + "\n"
        else:
            output += " " * (n + 4) + "None\n"
        # Increment
        output += " " * (n + 2) + "Increment:\n"
        if self.increment:
            output += self.increment.tostring(n + 4) + "\n"
        else:
            output += " " * (n + 4) + "None\n"
        # Body
        output += " " * (n + 2) + "Body:\n"
        output += self.body.tostring(n + 4)
        return output

# ---------------------------
# Bloque main para probar la representación
# ---------------------------
if __name__ == "__main__":
    # Crear algunos tokens de ejemplo
    token_42         = Token(lineno=1, value="42", tipo="Int")
    token_1          = Token(lineno=1, value="1", tipo="Int")
    token_1          = Token(lineno=1, value="1", tipo="Int")
    token_x          = Token(lineno=1, value="x", tipo="TIdentifier")
    token_plus       = Token(lineno=1, value="+", tipo="TPlus")
    token_minus      = Token(lineno=1, value="-", tipo="TMinus")
    token_lt         = Token(lineno=1, value="<", tipo="TLess")
    token_rightParen = Token(lineno=1, value=")", tipo="TRightParen")
    token_foo        = Token(lineno=1, value="foo", tipo="TIdentifier")
    
    # Probar nodos de expresiones
    literal_42 = Literal(token=token_42)
    print("Literal:")
    print(literal_42.tostring(2))
    
    variable_x = Variable(name=token_x)
    print("\nVariable:")
    print(variable_x.tostring(2))
    
    unary_expr = Unary(operator=token_minus, right=literal_42)
    print("\nUnary Expression:")
    print(unary_expr.tostring(2))
    
    # Expresión de condición: x < 42 (más natural que "x + 42")
    condition_expr = Binary(left=variable_x, operator=token_lt, right=literal_42)
    print("\nCondition Expression:")
    print(condition_expr.tostring(2))
    
    # Expresión para incremento: x + 1
    literal_1 = Literal(token=token_1)
    increment_expr = Binary(left=variable_x, operator=token_plus, right=literal_1)
    print("\nIncrement Expression:")
    print(increment_expr.tostring(2))
    
    # Ejemplo de expresión de llamada: foo(42)
    variable_foo = Variable(name=token_foo)
    call_expr = Call(
        callee=variable_foo,
        paren=token_rightParen,
        arguments=[literal_42]
    )
    print("\nCall Expression:")
    print(call_expr.tostring(2))
    
    # Probar nodos de sentencias
    expr_stmt = ExpressionStmt(expr=condition_expr)
    print("\nExpression Statement:")
    print(expr_stmt.tostring(2))
    
    print_stmt = PrintStatement(expr=condition_expr)
    print("\nPrint Statement:")
    print(print_stmt.tostring(2))
    
    return_stmt = ReturnStatement(expr=condition_expr)
    print("\nReturn Statement:")
    print(return_stmt.tostring(2))
    
    block_stmt = Block(declarations=[print_stmt])
    while_stmt = WhileStatement(
        condition=condition_expr,
        body=block_stmt
    )
    print("\nWhile Statement:")
    print(while_stmt.tostring(2))
    
    var_decl = VarDeclaration(name="x", expr=Binary(left=literal_42, operator=token_plus, right=literal_1))
    for_stmt = ForStatement(
        initializer=var_decl,
        condition=condition_expr,
        increment=increment_expr,
        body=block_stmt
    )
    print("\nFor Statement:")
    print(for_stmt.tostring(2))
    
    func_body = Block(declarations=[var_decl])
    function = Function(name="foo", params=["a", "b"], body=func_body)
    func_decl = FunctionDeclaration(fun=function)
    print("\nFunction Declaration:")
    print(func_decl.tostring(2))
    
    class_decl = ClassDeclaration(name="MyClass", father=None, methods=[function])
    print("\nClass Declaration:")
    print(class_decl.tostring(2))
    
    program = Program(declarations=[var_decl, func_decl, class_decl])
    print("\nProgram:")
    print(program.tostring(0))

