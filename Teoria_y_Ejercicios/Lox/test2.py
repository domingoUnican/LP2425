from Representacion import *

def main(): 
    print(f"GENERACION DE PRIMAY")
    print(f"--------------------")
    primary1 = Primary(Token(1, "15", "TNumber"))
    print(f">>PRIMAY 1:\n\n{primary1.tostring()}\n")
    primary2 = Primary(Token(1, "7", "TNumber"))
    print(f">>PRIMAY 2:\n\n{primary2.tostring()}\n")
    primary3 = Primary(Token(1, "20", "TNumber"))
    print(f">>PRIMAY 3:\n\n{primary3}\n")

    print(f"GENERACION DE CALL")
    print(f"--------------------")
    call1 = Call(primary1)
    print(f">>CALL 1 un numero:\n\n{call1.tostring()}\n")

    call2 = Call(primary2)
    print(f">>CALL 2 un numero:\n\n{call2.tostring()}\n")

    call3 = Call(primary3, idents=[Token(1, "argumento1", "TIdentifier"), Token(1, "argumento2", "TIdentifier")])
    print(f">>CALL 3 varios UNARY:\n\n{call3.tostring()}\n")

    print("El otro call para luego que ahora no se puede generar flalta expression\n")

    print(f"GENERACION DE UNARY")
    print(f"------------------")
    unary1 = Unary(call=call1)
    print(f">>UNARY 1 un numero:\n\n{unary1.tostring()}\n")

    unary2 = Unary(call=call2)
    print(f">>UNARY 2 un numero:\n\n{unary2.tostring()}\n")

    unary3 = Unary(op=Token(1, "!", "TyBang"), unary=unary1)
    print(f">>UNARY 3 otro unary:\n\n{unary3.tostring()}\n")

    unary4 = Unary(op=Token(1, "?", "TyBang"), unary=unary1)
    print(f">>UNARY 4 generador de error:\n\n{unary4.tostring()}\n")


    print(f"GENERACION DE FACTOR")
    print(f"------------------")
    factor1 = Factor(unary1)
    print(f">>FACTOR 1 un numero:\n\n{factor1.tostring()}\n")
    factor2 = Factor(unary2)
    print(f">>FACTOR 2 un numero:\n\n{factor2.tostring()}\n")

    factor3 = Factor(unary1, [(Token(1, "*", "TyStar"), unary2)])
    print(f">>FACTOR 3 multiplicacion de numeros:\n\n{factor3.tostring()}\n")

    factor4 = Factor(unary1, [(Token(1, "*", "TyStar"), unary2), (Token(1, "/", "TySlash"), unary1)])
    print(f">>FACTOR 4 varias operaciones:\n\n{factor4.tostring()}\n")


    print(f"GENERACION DE TERM")
    print(f"-----------------")

    term1 = Term(factor1)
    print(f">>TERM 1 un numero:\n\n{term1.tostring()}\n")

    term2 = Term(factor2)
    print(f">>TERM 2 un numero:\n\n{term2.tostring()}\n")

    term3 = Term(factor1, [(Token(1, "+", "TyPlus"), factor2)])
    print(f">>TERM 3 con dos factores simples, dos numeros:\n\n{term2.tostring()}\n")

    term4 = Term(factor1, [(Token(1, "-", "TyMinus"), factor2)])
    print(f">>TERM 4 una multiplicaion:\n\n{term3.tostring()}\n")

    term5 = Term(factor1, [(Token(1, "-", "TyMinus"), factor2), (Token(1, "+", "TyPlus"), factor1)])
    print(f">>TERM 5 dos operaciones simples:\n\n{term4.tostring()}\n")

    term6 = Term(factor1, [(Token(1, "-", "TyMinus"), factor2), (Token(1, "+", "TyPlus"), factor4)])
    print(f">>TERM 6 dos operaciones un factor simple y un factor compuesto:\n\n{term6.tostring()}\n")
    

    print(f"GENERACION DE COMPARISON")
    print(f"-----------------------")

    comp1 = Comparison(term1)
    print(f">>COMPARISON 1 un numero:\n\n{comp1.tostring()}\n")

    comp2 = Comparison(term2)
    print(f">>COMPARISON 2 un numero:\n\n{comp2.tostring()}\n")
    
    comp3 = Comparison(term1, [(Token(1, "<", "TyLess"), term2)])
    print(f">>COMPARISON 3 :\n\n{comp3.tostring()}\n")

    comp4 = Comparison(term1, [(Token(1, "<", "TyLess"), term2)])
    print(f">>COMPARISON 3 :\n\n{comp4.tostring()}\n")





if __name__ == "__main__":
    main()