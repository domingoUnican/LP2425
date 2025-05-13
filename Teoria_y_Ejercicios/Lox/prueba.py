import Lexer
import Representacion as r

for tok in Lexer.tokenize("10"):
    a = r.Factor(op="-", first_un=r.Unary("-", r.Number(tok=tok)), 
                  second_un=r.Unary("-", r.Number(tok=tok))
                )

print(a.tostring(0))

