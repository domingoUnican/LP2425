from Representacion import *
from Lexer import Token

def main():
    # Tokens
    ident_x = Token(1, "x", "TIdentifier")
    ident_y = Token(1, "y", "TIdentifier")
    ident_f = Token(1, "f", "TIdentifier")
    ident_g = Token(1, "g", "TIdentifier")
    ident_i = Token(1, "i", "TIdentifier")
    ident_sumar = Token(1, "sumar", "TIdentifier")
    ident_a = Token(1, "a", "TIdentifier")
    ident_b = Token(1, "b", "TIdentifier")
    num_0 = Token(1, "0", "TNumber")
    num_1 = Token(1, "1", "TNumber")
    num_2 = Token(1, "2", "TNumber")
    num_10 = Token(1, "10", "TNumber")
    num_100 = Token(1, "100", "TNumber")
    plus = Token(1, "+", "TPlus")
    star = Token(1, "*", "TStar")
    less = Token(1, "<", "TLess")

    # Expresión: x + 2 * 10
    expr = Expresion(
        Assignment(
            Logic_or(
                Logic_and(
                    Equality(
                        Comparison(
                            Term(
                                Factor(
                                    Unary(call=Call(Primary(ident_x))),
                                    right=[]
                                ),
                                right=[
                                    (plus, Factor(
                                        Unary(call=Call(Primary(num_2))),
                                        right=[
                                            (star, Unary(call=Call(Primary(num_10))))
                                        ]
                                    ))
                                ]
                            )
                        )
                    )
                )
            )
        )
    )

    # Variable: var x = 1;
    var_decl = VarDeclaration(ident=ident_x, expr=Expresion(
        Assignment(
            Logic_or(
                Logic_and(
                    Equality(
                        Comparison(
                            Term(
                                Factor(
                                    Unary(call=Call(Primary(num_1)))
                                )
                            )
                        )
                    )
                )
            )
        )
    ))

    # Función: f(y) { return y; }
    func_decl = FunctionDeclaration(
        fun=Function(
            ident=ident_f,
            param=Parameters(ident1=ident_y),
            body=Block(declarations=[
                ReturnStmt(expression=Expresion(
                    Assignment(
                        Logic_or(
                            Logic_and(
                                Equality(
                                    Comparison(
                                        Term(
                                            Factor(
                                                Unary(call=Call(Primary(ident_y)))
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                ))
            ])
        )
    )

    return_stmt_sumar = ReturnStmt(
        expression=Expresion(
            Assignment(
                Logic_or(
                    Logic_and(
                        Equality(
                            Comparison(
                                Term(
                                    Factor(
                                        Unary(call=Call(Primary(ident_a))),
                                        right=[
                                            (plus, Factor(
                                                Unary(call=Call(Primary(ident_b)))
                                            ))
                                        ]
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    func_sumar = FunctionDeclaration(
        fun=Function(
            ident=ident_sumar,
            param=Parameters(ident1=ident_a, idents=[ident_b]),
            body=Block(declarations=[
                return_stmt_sumar
            ])
        )
    )

    # Llamada: g(100)
    call_expr = Expresion(
        Assignment(
            Logic_or(
                Logic_and(
                    Equality(
                        Comparison(
                            Term(
                                Factor(
                                    Unary(call=Call(
                                        primary=Primary(ident_g),
                                        args=[
                                            Arguments(expression1=Expresion(
                                                Assignment(
                                                    Logic_or(
                                                        Logic_and(
                                                            Equality(
                                                                Comparison(
                                                                    Term(
                                                                        Factor(
                                                                            Unary(call=Call(Primary(num_100)))
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            ))
                                        ]
                                    ))
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    # Print: print x + 2 * 10;
    print_stmt = PrintStmt(expr=expr)

    # If: if (x) print x + 2 * 10;
    if_stmt = IfStmt(
        condition=Expresion(
            Assignment(
                Logic_or(
                    Logic_and(
                        Equality(
                            Comparison(
                                Term(
                                    Factor(
                                        Unary(call=Call(Primary(ident_x)))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        ),
        statement=print_stmt
    )

    # For: for (var i = 0; i < 10; i = i + 1)
    for_stmt = ForStmt(
        decl=VarDeclaration(
            ident=ident_i,
            expr=Expresion(
                Assignment(
                    Logic_or(
                        Logic_and(
                            Equality(
                                Comparison(
                                    Term(
                                        Factor(
                                            Unary(call=Call(Primary(num_0)))
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        ),
        expression1=Expresion(
            Assignment(
                Logic_or(
                    Logic_and(
                        Equality(
                            Comparison(
                                left=Term(
                                    Factor(
                                        Unary(call=Call(Primary(ident_i)))
                                    )
                                ),
                                right=[
                                    (less,
                                     Term(Factor(Unary(call=Call(Primary(num_10))))))
                                ]
                            )
                        )
                    )
                )
            )
        ),
        expression2=Expresion(
            Assignment(
                Logic_or(
                    Logic_and(
                        Equality(
                            Comparison(
                                Term(
                                    Factor(
                                        Unary(call=Call(Primary(ident_i)))
                                    ),
                                    right=[
                                        (plus, Factor(
                                            Unary(call=Call(Primary(num_1)))
                                        ))
                                    ]
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    # Programa completo
    program = Program(declarations=[
        var_decl,
        func_decl,
        func_sumar,
        ExprStmt(expr=call_expr),
        print_stmt,
        if_stmt,
        for_stmt
    ])

    print(program.tostring())

if __name__ == "__main__":
    main()
