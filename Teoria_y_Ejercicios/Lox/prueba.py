import Lexer
# import Representacion as r
import Representacion_Maxim as r

for tok in Lexer.tokenize("5"):
    a = r.Factor(op="-", first_un=r.Unary("-", r.Number(tok=tok)), 
                  second_un=r.Unary("-", r.Number(tok=tok))
                )
#TODO hacer el to string de las clases

print(a.tostring(0))

