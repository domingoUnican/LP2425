from Representacion import *


def main(): 
    print(f"GENERACION DE PRIMAY")
    print(f"--------------------")
    primary1 = Primary(Token(1, "15", "TNumber"))
    primary2 = Primary(Token(1, "7", "TNumber"))
    primary3 = Primary(Token(1, "2", "TNumber"))

    primary_super = Primary(Token(1, "super", "TSuper"))

    print(f"Primary1: \n{primary1.tostring()}")
    """  
    TNumber
        15
    """

    print(f"Primary2: \n{primary2.tostring()}")
    """  
    TNumber
        7
    """
    print(f"Primary3: \n{primary3.tostring()}")
    """
    TNumber
        2
    """
    print(f"PrimarySuper: \n{primary_super.tostring()}")

    print(f"GENERACION VARIOS COLLS CON SOLO 1 NUMERO PARA FACILITAR OPERACIONES")
    print(f"-------------------------------------------------------------------")

    num_coll = Call(primary1)
    print(f"\n{num_coll.tostring()}")
    num_coll_2 = Call(primary2)
    print(f"\n{num_coll_2.tostring()}")

    
    # Crear Unary con Token
    print(f"GENERACION DE UNARYS")
    print(f"--------------------")
    unary1 = Unary(Token(1, "!", "TyBang"), primary1)
    unary2 = Unary(Token(1, "-", "TyMinus"), primary2)
    unary3 = Unary(Token(1, "!", "TyBang"), primary3)

    print(f"UNARI 1: \n\n{unary1.tostring()}")
    """ 
    TBang
        !
    TNumber
        15
    """
    print(f"UNARI 2: \n\n{unary2.tostring()}")
    """
    TMinus
        -
    TNumber
        7
    """
    print(f"UNARI 3: \n\n{unary3.tostring()}")
    """
    TNumber
    TBang
        !
        2
    """

    # Crear un Factor con multiplicación
    print(f"\nGENERACION DE FACTOR")
    print(f"--------------------")
    factor1 = Factor(num_coll, [(Token(1, "/", "Operator"), num_coll_2)])
    factor2 = Factor(unary3, [(Token(1, "*", "Operator"), unary3)])
    print(f"FACTOR 1 sin operandos en unary: \n\n{factor1.tostring()}")
    """ 
    /
        TNumber
            5
        TNumber
        3
    """
    print(f"FACTOR 2 con operandos en unarys: \n\n{factor2.tostring()}")
    """
    *
        TNumber
            2
        TNumber
            2
    """

    print(f"--Solo un Unary sin operando")
    factor3 = Factor(num_coll)
    print(f"FACTOR 3: \n\n{factor3.tostring()}")
    """ 
    TNumber
        5
    """

    print(f"--Solo un Unary con operando")
    factor4 = Factor(unary1)
    print(f"FACTOR 4: \n\n{factor3.tostring()}")
    """ 
    TNumber
        5
    """

    print(f"--Lista de Unaris")
    factor4 = Factor(unary1, [(Token(1, "/", "Operator"), unary2), (Token(1, "*", "Operator"), unary3)])
    print(f"FACTOR 4: \n\n{factor4.tostring()}")
    """
    /
    *
        TNumber
            5
        TNumber
            3
        TNumber
            2
    """
    
    # Crear un TERM
    print(f"\nGENERACION DE TERM")
    print(f"------------------")


    term1 = Term(factor1, [(Token(1, "+", "Operator"), factor2)])
    print(f"TERM 1: \n\n{term1.tostring()}")

    """ 
    +
        /
            TNumber
            5
            TNumber
            3
        *
            TNumber
            2
            TNumber
            2
    """

    term2 = Term(factor2)
    print(f"TERM 2 (solo un factor): \n\n{term2.tostring()}")
    """  
    *
        TNumber
        2
        TNumber
        2
    """

    term3 = Term(factor3)
    print(f"TERM 3 (un factor de un unary): \n\n{term3.tostring()}")
    """ 
    TNumber
    2
    """

    print(f"GENERACION DE COMPARISON\n")
    print(f"-----------------------")
    comparison1 = Comparison(term1, [(Token(1, ">=", "Operator"), term1)])
    print(f"COMPARISON 1: \n\n{comparison1.tostring()}")
    """ 
    >=
        +
            /
                TNumber
                5
                TNumber
                3
            *
                TNumber
                2
                TNumber
                2
        +
            /
                TNumber
                5
                TNumber
                3
            *
                TNumber
                2
                TNumber
                2
    """


    print(f"Con dos Term simples con un unary cada uno")
    comparison2 = Comparison(term3, [(Token(1, "<", "Operator"), term3)])
    print(comparison2.tostring())
    """ 
    <
        TNumber
        2
        TNumber
        2
    """
    print(f"Con un Term simple con un unary")
    comparison3 = Comparison(term3)
    print(f"COMPARACION un argumento:\n{comparison3.tostring()}")
    """ 
    TNumber
        2
    """

    print(f"GENERACION DE EQUALITY\n")
    print(f"--------------------")
    print(f"Completo")
    equality1 = Equality(comparison1, [(Token(1, "==", "Operator"), comparison1)])
    print(equality1.tostring())

    """ 
    ==
        >=
            +
                /
                    TNumber
                    5
                    TNumber
                    3
                *
                    TNumber
                    2
                    TNumber
                    2
            +
                /
                    TNumber
                    5
                    TNumber
                    3
                *
                    TNumber
                    2
                    TNumber
                    2
    
                    
        >=
            +
                /
                    TNumber
                    5
                    TNumber
                    3
                *
                    TNumber
                    2
                    TNumber
                    2
            +
                /
                    TNumber
                    5
                    TNumber
                    3
                *
                    TNumber
                    2
                    TNumber
                    2
    """
    print(f"---Un comparation con dos term que son cada uno un Unary")
    equality2 = Equality(comparison2)
    print(f"{equality2.tostring()}")

    print(f"---Un unay")
    equality3 = Equality(comparison3)
    print(f"{equality3.tostring()}")
    """  
    
    """



    print(f"GENERACION DE LOGIC OR\n")
    print(f"--------------------")

    print(f"Simple con dos equalitys que son dos unarys")
    logic_Or1 = Logic_or(equality3, [equality3])
    print(f"{logic_Or1.tostring()}")

    print(f"\nGENERACION DE ASSIGNMENT")
    print(f"------------------------")

    print(f"\n---Assignmen logic or")
    assignment_log = Assignment(logic_Or1)
    print(f"{assignment_log.tostring()}")

    print(f"\nGENERACION PRIMAY")
    print(f"------------------")
    primaty1 = Primary(Token(1, "true", "TTrue"))
    print(f"{primaty1.tostring()}")

    print(f"\nGENERACION EXPRESSION")
    print(f"---------------------")
    expression1 = Expresion(assignment_log)
    print(f"{expression1.tostring()}")
    """ 
    
    
    """

    print(f"\nGENERACION ARGUMENt")
    print(f"------------------")
    argument1 = Arguments(expression1,[])
    print(f"{argument1.tostring()}")

    print(f"\nGENERACION CALL")
    print(f"------------------")
    call1 = Call(primaty1, [argument1])
    print(f"{call1.tostring()}")

    """ 
    TTrue
        true
    (
    and
        TNumber
            5
        TNumber
            5
    ) 
    """
    print(f"\n---dos argumentos")
    call2 = Call(primaty1, [argument1], [Token(1, "x", "TIdentifier")])
    print(f"{call2.tostring()}")

    """ 
    TTrue
        true
    (
    and
        TNumber
            5
        TNumber
            5
    ) 
    """

    print(f"\n---AssignmentWithAsigment")
    assignmentwith_asig = AssignmentWithAsigment(call1, Token(1, "x", "TIdentifier"), assignment_log)
    print(f"{assignmentwith_asig.tostring()}")

    print(f"\nGENERACION EXPRESION")
    expr = Expresion(assignmentwith_asig)
    print(f"{expr.tostring()}")


    print(f"\nGENERACION  DE CLASES")
    print(f"----------------------")
    clase_3 = ClassDeclaration(Token(1, "clase_1", "TIdentifier"), Token(1, "clase_HOLA", "TIdentifier"))
    print(f"{clase_3.tostring()}")


    print(f"\nGENERACION  DE VAR DECLARATION")
    print(f"------------------------------")
    varDecl = VarDeclaration(Token(1, "var_1", "TIdentifier"), expression1)
    print(f"{varDecl.tostring()}")
    """ 
    var
    var_1
    =
        and
        TNumber
            15
        TNumber
            15
    ;
    """

    print(f"\nGENERACION  DE EXPRESION STMT")
    print(f"------------------------------")
    exprstm = ExprStmt(expression1)
    print(f"{exprstm.tostring()}")

    """ 
        and
        TNumber
            15
        TNumber
            15
    ;
    """

    print(f"\nGENERACION  DE EXPRESION STMT")
    print(f"------------------------------")
    print1 = PrintStmt(expression1)
    print(f"{print1.tostring()}")

    """
    print 
        and
        TNumber
            15
        TNumber
            15
    ;
    """

    print(f"\nGENERACION  DE FOR")
    print(f"--------------------")
    forstm = ForStmt(decl=varDecl, expression1=expression1, expression2=expression1)
    print(f"{forstm.tostring()}")

    """
    for
    (
        var
        var_1
        =
            and
                TNumber
                    15

                TNumber
                    15

    ;
        and
            TNumber
                15

            TNumber
                15

    ;
        and
            TNumber
                15

            TNumber
                15
    )
    """

    print(f"\nGENERACION  DE IF")
    print(f"-----------------")
    if1 = IfStmt(expression1, exprstm)
    print(f"{if1.tostring()}")

    """
    if
    (
        and
            TNumber
                15

            TNumber
                15

    )
    """

    print(f"\nGENERACION  DE RETURN")
    print(f"---------------------")
    return1 = ReturnStmt(expression1)
    print(f"RETURN 1\n\n{return1.tostring()}")
    """
    return
        and
            TNumber
                15

            TNumber
                15
    """

    return2 = ReturnStmt()
    print(f"RETURN 2\n\n{return2.tostring()}")
    
    
    print(f"\nGENERACION  DE WHILE")
    print(f"---------------------")
    while1 = WhileStmt(expression1, if1)
    print(f"WHILE 1\n\n{while1.tostring()}")
    """
    while
    (
        and
            TNumber
                15

            TNumber
                15

    )
    """

if __name__ == "__main__":
    main()