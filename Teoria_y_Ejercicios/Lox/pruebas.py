from Representacion import * 
#####################################################################################
                                    # PRUEBAS
#####################################################################################

#####################################################################################
# En principio, todas las pruebas salen comentadas para poder ver una a una
#####################################################################################

# Crear objetos de cada clase
# Tipo Number
print("Pruebas Tipo Number")
print("--------------------")
num1 = Number(1)           # 1
#print(num1.tostring(0))

num2 = Number(2)           # 2
#print(num2.tostring(0))
print("")

# Tipo Primary
print("Pruebas Tipo Primary")
print("--------------------")
prim_string = PrimaryString("variable")           # variable
#print(prim_string.tostring(0))

prim_number = PrimaryNumber(num1)                 # 1
#print(prim_number.tostring(0))

prim_attr = PrimaryAttribute("atributo")          # super.atributo
#print(prim_attr.tostring(0))
print("")

# Tipo Call
print("Pruebas Tipo Call")
print("--------------------")
call = Call(prim_string)                                            # variable
#print(call.tostring(0))

call_attr = CallAtribute(prim_string, "atributo")                   # variable.atributo
#print(call_attr.tostring(0))

call_method_args = CallMethod(prim_string, [prim_number, prim_number])     # variable(1, 1)
#print(call_method_args.tostring(0))

call_method = CallMethod(prim_string)                               # variable()  
#print(call_method.tostring(0))
print("")

# Tipo Unary
print("Pruebas Tipo Unary")
print("--------------------")
unary_op = UnaryOP("-", call)              # -variable
#print(unary_op.tostring(0))

unary_call = UnaryCall(call_method)        # variable()
#print(unary_call.tostring(0))
print("")

# Tipo Factor
print("Pruebas Tipo Factor")
print("--------------------")
factor = Factor(unary_op, [("/", unary_op)]) # -variable / -variable 
#print(factor.tostring(0))
print("")

# Tipo Term
print("Pruebas Tipo Term")
print("--------------------")
term = Term(factor, [("-", factor)]) # factor - factor 
#print(term.tostring(0))

term1 = Term(factor) # factor
#print(term1.tostring(0))
print("")

# Tipo Comparison
print("Pruebas Tipo Comparison")
print("------------------------")
comp = Comparison(term, [("<", term1)]) # term < term1
#print(comp.tostring(0))

comp1 = Comparison(term1) # term1
#print(comp1.tostring(0))

comp2 = Comparison(term) # term1
print("")

# Tipo Equality
print("Pruebas Tipo Equality")
print("----------------------")
eq = Equality(comp1, [("==", comp2)]) # comp == comp1
#print(eq.tostring(0))

eq1 = Equality(comp1) # comp1
#print(eq1.tostring(0))

eq2 = Equality(comp, [("!=", comp1)]) # comp != comp1
#print(eq2.tostring(0))
print("")

# Tipo Logic_AND
print("Pruebas Tipo Logic_AND")
print("-----------------------")
logic_and = Logic_AND(eq1, [("and", eq1)]) # eq and eq1
#print(logic_and.tostring(0))

logic_and1 = Logic_AND(eq, [("and", eq2)]) # eq and eq2
#print(logic_and1.tostring(0))
print("")

# Tipo Logic_OR
print("Pruebas Tipo Logic_OR")
print("----------------------")
logic_or = Logic_OR(logic_and, [("or", logic_and)]) # logic_and or logic_and1
#print(logic_or.tostring(0))
print("")

# Tipo Assignment
print("Pruebas Tipo Assignment")
print("------------------------")
assignment = AssignmentWithLogicOR(logic_or) # logic_or
#print(assignment.tostring(0))

assignment1 = AssignmentWithAssignment("identificador", assignment, call) # call.identificador = assignment
#print(assignment1.tostring(0))
print("")

# Tipo expression
print("Pruebas Tipo Expression")
print("------------------------")
expression = Expression(assignment1) # assignment1
#print(expression.toString(0))
print("")

#######################STATEMENTS########################
var_declaration = VarDecl("variable", expression)

# Tipo Statement
print("Pruebas Tipo ExprStmt")
print("----------------------")
expr_statement = ExprStmt(expression) # expression
#print(statement.toString(0)) # expression
print("")

# Tipo ForStmt
print("Pruebas Tipo ForStmt")
print("----------------------")
for_stmt = ForStmt(expr_statement, var_declaration) # var_declaration; statement; expression
#print(for_stmt.toString(0)) # statement; statement; expression
print("")

# Tipo IfStmt
print("Pruebas Tipo IfStmt")
print("----------------------")
if_stmt = IfStmt(expression, expr_statement, expr_statement) # expression; statement; statement
#print(if_stmt.toString(0)) # expression; statement; statement
print("")

# Tipo PrintStmt
print("Pruebas Tipo PrintStmt")
print("----------------------")
print_stmt = PrintStmt(expression) # expression
#print(print_stmt.toString(0)) # expression
print("")

# Tipo ReturnStmt
print("Pruebas Tipo ReturnStmt")
print("----------------------")
return_stmt = ReturnStmt(expression) # expression
#print(return_stmt.toString(0))
print("")

# Tipo WhileStmt
print("Pruebas Tipo WhileStmt")
print("----------------------")
while_stmt = WhileStmt(expression, print_stmt)
#print(while_stmt.toString(0))
print("")

# Tipo Block
print("Pruebas Tipo Block")
print("----------------------")
bloque = Block() # {}
#print(bloque.toString(0)) # {}
print("")

########################UNITY RULES########################
# Tipo Parameters
print("Pruebas Tipo Parameters")
print("----------------------")
parameters = Parameters(["param1", "param2"]) # variable, 1
#print(parameters.tostring(0)) # variable, 1
print("")

# Tipo Arguments
print("Pruebas Tipo Arguments")
print("----------------------")
arguments = Arguments([expression, expression]) # variable, 1
#print(arguments.tostring(0)) # variable, 1
print("")

# Tipo Function
print("Pruebas Tipo Function")
print("----------------------")
function = Function("funcion", bloque, parameters)
#print(function.tostring(0)) # funcion {}
print("")

##########################DECLARATIONS##########################
# Tipo VarDeclaration
print("Pruebas Tipo VarDecl")
print("----------------------")
#print(var_declaration.toString(0))
print("")

# Tipo ClassDeclaration
print("Pruebas Tipo ClassDecl")
print("----------------------")
class_declaration = ClassDecl("Clase", "id", [function])
#print(class_declaration.toString(0)) # funcion {}
print("")

# Tipo FunDeclaration
print("Pruebas Tipo FunDecl")
print("----------------------")
fun_declaration = FunDecl(function)
#print(fun_declaration.toString(0)) # funcion {}
print("")

# Tipo Program
print("Pruebas Tipo Program")
print("----------------------")
program = Program([class_declaration, fun_declaration]) # funcion {}
#print(program.toString(0)) # funcion {}
print("")

""" 
# Probar Block 
print("Pruebas Tipo Block")
print("----------------------")
bloque = Block([declaration])
print(bloque.toString(0)) # { var variable = expression; }
print("")

# Probar Function
function = Function("function", bloque) # function { var variable = expression; }
print(function.tostring(0))
print("")

declaration1 = FunctionDeclaration(function) # fun function { var variable = expression; }
print(declaration1.toString(0))
print("")

declaration2 = ClassDeclaration("Clase1", "Clase2", [function]) # class Clase1 < Clase2 { fun function { var variable = expression; } }
print(declaration2.toString(0))
print("")





 """