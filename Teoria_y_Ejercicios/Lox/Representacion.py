from dataclasses import dataclass
from Lexer import Token
from typing import List, Optional, Tuple, Union

#####################################################################################
                                    # Number
#####################################################################################

@dataclass
class Number():
    num: int
    def tostring(self, n):
        output = " " * n + str(self.num)  # Aquí ponemos el valor un poco más indentado
        return output
    
#####################################################################################
                                    # Term
#####################################################################################

# Clase Term
@dataclass
class Term:
    # Primer atributo de tipo Factor
    factor1:"Factor"
    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Factor
    factor2: Optional[List[Tuple[str, "Factor"]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"-","+"}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.factor2 is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.factor2:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Term
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en factor2, procesarlas recursivamente
        if self.factor2:
            # Tomar la primera operación y sus operandos
            op, factor = self.factor2[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.factor1.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.factor2) > 1:
                remaining_term = Term(factor, self.factor2[1:])
                output += remaining_term.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += factor.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.factor1.tostring(n)
        return output
#####################################################################################
                                    # Comparison
#####################################################################################

# Clase Comparison
@dataclass
class Comparison:
    # Primer atributo de tipo Term
    term1:Term
    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Term
    term2: Optional[List[Tuple[str, Term]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {">",">=", "<", "<="}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.term2 is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.term2:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Comparison
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en term2, procesarlas recursivamente
        if self.term2:
            # Tomar la primera operación y sus operandos
            op, term = self.term2[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.term1.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.term2) > 1:
                remaining_comparison = Comparison(term, self.term2[1:])
                output += remaining_comparison.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += term.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.term1.tostring(n)
        return output
    
#####################################################################################
                                    # Equality
#####################################################################################

# Clase Equality
@dataclass
class Equality:
    # Primer atributo de tipo Comparison
    comparison1:Comparison
    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Comparison
    comparison2: Optional[List[Tuple[str, Comparison]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"!=","=="}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.comparison2 is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.comparison2:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Equality
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en comparison2, procesarlas recursivamente
        if self.comparison2:
            # Tomar la primera operación y sus operandos
            op, comparison = self.comparison2[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.comparison1.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.comparison2) > 1:
                remaining_equality = Equality(comparison, self.comparison2[1:])
                output += remaining_equality.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += comparison.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.comparison1.tostring(n)
        return output

#####################################################################################
                                    # Logic AND
#####################################################################################

# Clase Logic_AND
@dataclass
class Logic_AND:
    # Primer atributo de tipo Equality
    equality1:Equality
    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Equality
    equality2: Optional[List[Tuple[str, Equality]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"and"}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.equality2 is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.equality2:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Logic_AND
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en equality2, procesarlas recursivamente
        if self.equality2:
            # Tomar la primera operación y sus operandos
            op, equality = self.equality2[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.equality1.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.equality2) > 1:
                remaining_logic_and = Logic_AND(equality, self.equality2[1:])
                output += remaining_logic_and.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += equality.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.equality1.tostring(n)
        return output
    
#####################################################################################
                                    # Logic OR
#####################################################################################

# Clase Logic_OR
@dataclass
class Logic_OR:
    # Primer atributo de tipo Logic_AND
    logic_and1:Logic_AND
    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Logic_AND
    logic_and2: Optional[List[Tuple[str, Logic_AND]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"or"}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.logic_and2 is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.logic_and2:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Factor
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en logic_and2, procesarlas recursivamente
        if self.logic_and2:
            # Tomar la primera operación y sus operandos
            op, logic_and = self.logic_and2[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.logic_and1.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.logic_and2) > 1:
                remaining_logic_or = Logic_OR(logic_and, self.logic_and2[1:])
                output += remaining_logic_or.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += logic_and.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.logic_and1.tostring(n)
        return output

#####################################################################################
                                    # Assignment
#####################################################################################

# Clase Assignment
@dataclass
class Assignment:
    pass

@dataclass
class AssignmentWithAssignment:
    identificator: str
    assignment: Assignment
    call: Optional["Call"]=None

    def tostring(self, n):
        output = ""
        output += " " * n + "=\n"

        if self.call is not None:
            output += self.call.tostring(n+2) + "\n"
            output += " " * (n + 4) + ".\n"
            output += " " * (n + 6) + f"{self.identificator}\n"
        else:
            output += " " * n + f"{self.identificator}\n"

        output += " " * n + "\n"
        output += self.assignment.tostring(n + 2)
        return output

@dataclass
class AssignmentWithLogicOR:
    logicOR: Logic_OR

    def tostring(self, n=0):
        return self.logicOR.tostring(n)

#####################################################################################
                                    # Expression
#####################################################################################

@dataclass
class Expression:
    assignment: Assignment

    def toString(self, n=0):
        return self.assignment.tostring(n)

#####################################################################################
                                    # Primary
#####################################################################################

@dataclass
class Primary:
    pass

@dataclass
class PrimaryString(Primary):
    value: str
    def tostring(self, n=0):
        return " " * n + self.value  # Simplemente devuelve la cadena con la indentación correcta

@dataclass
class PrimaryNumber(Primary):
    value: Number
    def tostring(self, n=0):
        return self.value.tostring(n)
    
@dataclass
class PrimaryAttribute(Primary):
    identificator: str
    def tostring(self, n=0):
        indent = " " * n
        output = f"{indent}super\n"
        output += f"{' ' * (n + 2)}.\n"
        output += f"{' ' * (n + 4)}{self.identificator}"
        return output
    
@dataclass
class PrimaryExpression(Primary):
    expresion: Expression
    def tostring(self, n=0):
        return " " * n + f"({self.expresion.toString(n)})"
    
#####################################################################################
                                    # Call
#####################################################################################

@dataclass
class Call:
    primary: Primary
    def tostring(self, n=0):
        return self.primary.tostring(n)


@dataclass
class CallAtribute(Call):
    identificator: Optional[str] = None
    additional_call: Optional[Call] = None

    def tostring(self, n=0):
        indent = " " * n
        output = self.primary.tostring(n)  # Imprimir el objeto primario (variable)
        if self.identificator:
            output += f"\n{' ' * (n + 2)}.\n"  # Imprimir el punto con más indentación
            output += f"{' ' * (n + 4)}{self.identificator}"  # Imprimir el atributo con más indentación
        if self.additional_call:
            output += "\n" + self.additional_call.tostring(n + 2)  # Procesar llamadas adicionales encadenadas
        return output

@dataclass
class CallMethod(Call):
    arguments: Optional["Arguments"] = None
    additional_call: Optional[Call] = None

    def tostring(self, n=0):
        indent = " " * n
        output = self.primary.tostring(n) + "\n"  # Imprimir el nombre del método

        # Imprimir los paréntesis y los argumentos
        output += f"{indent}  (\n"
        if self.arguments:
            for arg in self.arguments:
                output += arg.tostring(n + 4) + "\n"  # Llamar al método `tostring` de cada argumento
        output += f"{indent}  )"

        # Procesar llamadas adicionales encadenadas
        if self.additional_call:
            output += "\n" + self.additional_call.tostring(n + 2)
        return output
#####################################################################################
                                    # Unary
#####################################################################################

@dataclass
class Unary:
    pass

@dataclass
class UnaryOP(Unary):
    # Primer atributo: Un string que representa la operación
    op: str
    # Segundo atributo: Un objeto de tipo Unary
    unary: Unary

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la 
    # lista de tuplas sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"!", "-"}

        # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
        # con un mensaje de error para que no se pueda crear una instancia de la clase UnaryOP
        if self.op not in valid_operations:
            raise ValueError(f"Invalid operation for UnaryOP: {self.op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        output =" " * n + self.op + "\n"
        output += self.unary.tostring(n+2) + "\n"
        return output

@dataclass
class UnaryCall(Unary):
    call: Call
    
    def tostring(self, n):
        return self.call.tostring(n)

#####################################################################################
                                    # Factor
#####################################################################################

@dataclass
class Factor:
    # Primer atributo de tipo Unary
    first_attr: Unary

    # Segundo atributo(Opcional): Lista de tuplas compuestas por una operacion y un Unary
    second_attr: Optional[List[Tuple[str, Unary]]] = None 

    # Metodo que se ejecuta depués del método __init__ para verificar que las operaciones de la lista de tuplas
    # del segundo argumento sean validas
    def __post_init__(self):

        # Lista de operaciones válidas
        valid_operations = {"/", "*"}

        # Si la lista de tuplas no es None, comprobamos que las operaciones sean válidas
        if self.second_attr is not None:

            # Iteramos sobre la lista de tuplas teniendo en cuenta el primer argumento de la tupla
            # que es la operación
            for op,_ in self.second_attr:

                # Si la operación no está en la lista de operaciones válidas, lanzamos una excepción
                # con un mensaje de error para que no se pueda crear una instancia de la clase Factor
                if op not in valid_operations:
                    raise ValueError(f"Invalid operation for Factor: {op}, the only valid operations are {valid_operations}")

    def tostring(self, n):
        indent = " " * n
        output = ""

        # Si hay operaciones en second_attr, procesarlas recursivamente
        if self.second_attr:
            # Tomar la primera operación y sus operandos
            op, unary = self.second_attr[0]
            output += f"{indent}{op}\n"  # Imprimir la operación más externa
            output += self.first_attr.tostring(n + 2) + "\n"  # Imprimir el primer operando con más indentación

            # Si hay más operaciones, procesarlas recursivamente
            if len(self.second_attr) > 1:
                remaining_factor = Factor(unary, self.second_attr[1:])
                output += remaining_factor.tostring(n)
            else:
                # Si no hay más operaciones, imprimir el segundo operando
                output += unary.tostring(n + 2)
        else:
            # Si no hay operaciones, solo imprimimos el primer operando
            output += self.first_attr.tostring(n)
        return output
    
#####################################################################################
                                    # Statements
#####################################################################################

@dataclass
class Statement:
    pass

@dataclass
class ExprStmt(Statement):
    expression: Expression

    def toString(self, n=0):
        indent = " " * n
        return f"{indent}{self.expression.toString(n)};"
    
@dataclass
class ForStmt(Statement):
    body: Statement  # Cuerpo del bucle
    initializer: Optional[Union["VarDecl", "ExprStmt"]] = None  # Inicializador opcional
    expr1: Optional[Expression] = None  # Condición opcional
    expr2: Optional[Expression] = None  # Incremento opcional

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}for\n"  # Imprimir "for" en una nueva línea
        output += f"{' ' * (n + 2)}(\n"  # Abrir paréntesis con más indentación

        # Inicializador
        if self.initializer:
            output += self.initializer.toString(n + 4) + "\n"
        else:
            output += f"{' ' * (n + 4)};\n"  # Imprimir un punto y coma si no hay inicializador

        # Condición
        if self.expr1:
            output += self.expr1.toString(n + 4) + "\n"
        
        output += f"{' ' * (n + 4)};\n"  # Imprimir un punto y coma si no hay condición

        # Incremento
        if self.expr2:
            output += self.expr2.toString(n + 4) + "\n"

        output += f"{' ' * (n + 2)})\n"  # Cerrar paréntesis con más indentación

        # Cuerpo del bucle
        output += self.body.toString(n + 2)
        return output
    
@dataclass
class IfStmt(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement] = None

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}if\n"
        output += f"{indent}(\n"  # Abrir paréntesis en una nueva línea
        output += self.condition.toString(n + 2) + "\n"  # Imprimir la condición con más indentación
        output += f"{indent})\n"  # Cerrar paréntesis en una nueva línea

        # Ajustar la indentación del bloque `then_branch`
        then_output = self.then_branch.toString(n + 2).strip()
        output += f"{' ' * (n + 2)}{then_output}\n"

        # Ajustar la indentación del bloque `else_branch` si existe
        if self.else_branch:
            output += f"{indent}else\n"
            else_output = self.else_branch.toString(n + 2).strip()
            output += f"{' ' * (n + 2)}{else_output}\n"

        return output
    
@dataclass
class PrintStmt(Statement):
    expression: Expression

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}print\n"  # Imprimir "print" primero
        output += self.expression.toString(n + 2) + "\n"  # Imprimir la expresión con más indentación
        output += f"{indent};"  # Imprimir el punto y coma al final
        return output
    
@dataclass
class ReturnStmt(Statement):
    value: Optional[Expression] = None

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}return\n"  # Imprimir "return" primero

        # Si hay un valor, imprimirlo con la jerarquía adecuada
        if self.value:
            output += self.value.toString(n + 2) + "\n"

        # Imprimir el punto y coma al final
        output += f"{indent};"
        return output
        
@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Statement

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}while\n"  # Imprimir "while" primero
        output += f"{' ' * (n + 2)}(\n"  # Abrir paréntesis con dos niveles más de indentación
        output += self.condition.toString(n + 4) + "\n"  # Imprimir la condición con más indentación
        output += f"{' ' * (n + 2)})\n"  # Cerrar paréntesis con dos niveles más de indentación
        output += self.body.toString(n + 4)  # Imprimir el cuerpo con más indentación
        return output
    
@dataclass
class Block(Statement):
    declarations: Optional[List["Declaration"]] = None  # Lista de declaraciones (puede estar vacía)

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}{{\n"

        # Asegurarse de que `self.declarations` sea una lista
        if self.declarations is None:
            self.declarations = []
        elif not isinstance(self.declarations, list):
            self.declarations = [self.declarations]

        # Iterar sobre las declaraciones y generar su representación
        for declaration in self.declarations:
            output += declaration.toString(n + 2) + "\n"

        output += f"{indent}}}"
        return output
#####################################################################################
                                    # Unity Rules
#####################################################################################

@dataclass
class Function:
    name: str
    body: "Block"
    params: Optional["Parameters"] = None

    def tostring(self, n=0):
        indent = " " * n
        output = f"{indent}{self.name}\n"  # Imprimir el nombre de la función en una línea
        output += f"{' ' * (n + 2)}(\n"  # Abrir paréntesis con una tabulación más

        # Imprimir los parámetros con la indentación adecuada
        if self.params:
            for param in self.params.identifiers:
                output += f"{' ' * (n + 4)}{param},\n"
            output = output.rstrip(",\n") + "\n"  # Eliminar la última coma y salto de línea

        output += f"{' ' * (n + 2)})\n"  # Cerrar paréntesis con una tabulación más

        # Imprimir el cuerpo de la función con la indentación adecuada
        output += self.body.toString(n + 2)
        return output
    
@dataclass
class Parameters:
    id1: str  # El primer identificador es obligatorio
    identifiers: Optional[List[str]] = None  # Lista opcional de identificadores adicionales

    def tostring(self, n=0):
        indent = " " * n
        output = f"{indent}{self.id1}"  # Imprimir el primer identificador

        # Si hay identificadores adicionales, imprimirlos con comas y en líneas separadas
        if self.identifiers:
            for i, identifier in enumerate(self.identifiers):
                output += f",\n{indent}{identifier}"

        output += "\n"  # Agregar un salto de línea al final
        return output

@dataclass
class Arguments:
    arg1: Expression  # El primer argumento es obligatorio
    args: Optional[List[Expression]] = None  # Lista de argumentos adicionales

    def tostring(self, n=0):
        indent = " " * n
        output = f"{indent}{self.arg1.toString(n)}"  # Imprimir el primer argumento

        # Si hay argumentos adicionales, imprimirlos con comas y en líneas separadas
        if self.args:
            for arg in self.args:
                output += f",\n{arg.toString(n)}"

        output += "\n"  # Agregar un salto de línea al final
        return output
    
#####################################################################################
                                    # Declarations
#####################################################################################

@dataclass
class Declaration:
    pass

@dataclass
class ClassDecl(Declaration):
    identificador1: str
    identificador2: Optional[str] = None
    methods: Optional[List[Function]] = None  # Lista de métodos dentro de la clase

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}class\n"  # Imprimir "class" en una nueva línea
        output += f"{' ' * (n + 2)}{self.identificador1}\n"  # Imprimir el nombre de la clase con más indentación

        # Si hay un identificador2 (herencia), imprimirlo en una nueva línea
        if self.identificador2:
            output += f"{' ' * (n + 2)}<\n"
            output += f"{' ' * (n + 4)}{self.identificador2}\n"

        output += f"{' ' * (n + 2)}{{\n"  # Abrir el bloque con más indentación

        # Imprimir los métodos con la indentación adecuada
        for method in self.methods or []:
            output += method.tostring(n + 4) + "\n"

        output += f"{' ' * (n + 2)}}}"  # Cerrar el bloque con más indentación
        return output
    
@dataclass
class FunDecl(Declaration):
    fun: Function

    def toString(self, n=0):
        indent = " " * n
        output = f"{indent}fun\n"  # Imprimir "fun" en una nueva línea
        output += self.fun.tostring(n + 2)  # Delegar la impresión completa de la función al método `tostring` de `Function`
        return output
    
@dataclass
class VarDecl(Declaration):
    identificador: str
    expresion: Optional[Expression] = None

    def toString(self, n=0):
        indent = " " * n
        output = ""

        # Si hay una expresión, imprimir el operador `=` primero
        if self.expresion:
            output += f"{indent}=\n"

        # Imprimir `var` y el identificador con la jerarquía adecuada
        output += f"{indent}var\n"
        output += f"{' ' * (n + 4)}{self.identificador}\n"

        # Si hay una expresión, imprimirla con la jerarquía adecuada
        if self.expresion:
            output += self.expresion.toString(n + 2) + "\n"

        # Imprimir el punto y coma al final
        output += f"{indent};"
        return output



#####################################################################################
                                    # PROGRAM
#####################################################################################

@dataclass
class Program:
    declarations: List[Declaration]

    def toString(self, n=0):
        indent = " " * n
        if not self.declarations:
            return f"{indent}/* Empty program */"
        output = ""
        for declaration in self.declarations:
            output += declaration.toString(n) + "\n"
        return output

