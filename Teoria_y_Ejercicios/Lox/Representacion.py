from dataclasses import dataclass, field
from Lexer import Token
from typing import List, Optional

@dataclass
class Primary:
    tok: Token
    tipo_expr: Optional["Expression"] = None
    def tostring(self,n):
        output = ""
        output +=  " " * (n) + str(self.tok.tipo) +  "\n"
        if (self.tok.tipo == "TSuper"):
            output += " " * (n + 2) + "super" + "\n"
            output += " " * (n + 2) + "." + "\n"
            output += " " * (n + 2) +self.tok.value + "\n"
        else:
            output += " " * (n+2) + self.tok.value + "\n"
        if self.tipo_expr:
            output += " " * (n) + "(" + "\n"
            output += self.tipo_expr.tostring(n)
            output += " " * (n) + ")" + "\n"
        return output

@dataclass
class Call():
    base: Primary
    args: List["Arguments"] = field(default_factory=list)
    otras: List[Token] = field(default_factory=list)  # tokens IDENTIFIER tras puntos

    def tostring(self, n=0):
        output = ""
        output += self.base.tostring(n)
        if self.args or self.otras:
            if self.args:
                for argumen in self.args:
                    output += " " * (n) + "(" + "\n"
                    output += argumen.tostring(n+2)
                    output += " " * (n) + ")" + "\n"
            if self.otras:
                for ident in self.otras:
                    output += " " * (n) + "." + "\n"
                    output += ident.tostring(n+2) + "\n"
        return output

    
@dataclass
class Unary:
    op: Optional["Token"]=None  
    unar: Optional["Unary"]=None  
    ca: Optional["Call"]=None

    def tostring(self, n):
        output= ""
        if self.unar and self.op:
            output += " "*n + self.op.value +"\n" 
            output += self.unar.tostring(n+2)
        if self.ca:
            output += self.ca.tostring(n)
        return output



@dataclass
class Factor:
    first_un: Unary
    op: Optional["Token"]=None  
    res1: List["Unary"] = field(default_factory=list)
    def tostring(self, n):
        output = ""
        if self.res1:
            output += " " * (n)+ self.op.value + "\n"
            output += self.first_un.tostring(n + 2)
            for i in self.res1:
                output += i.tostring(n + 2)
        else:
            output += self.first_un.tostring(n)
        return output
    
@dataclass
class Term:
    first_factor: Factor
    op: Optional["Token"]=None
    res1: List["Factor"] = field(default_factory=list)
    def tostring(self, n):
        output = ""
        if self.res1:
            output += " " * (n) + self.op.value + "\n"
            output += self.first_factor.tostring(n+2)
            for i in self.res1:
                output += i.tostring(n+2)
        else:
            output += self.first_factor.tostring(n)
        
        return output
        
@dataclass
class Comparison:
    compar_primer: Term
    op: Optional["Token"]=None
    siguiente: List["Term"] = field(default_factory=list)
    def tostring(self, n):
        output = ""
        if self.siguiente:
            output += " " * (n) + self.op.value + "\n"
            output += self.compar_primer.tostring(n+2)
            for i in self.siguiente:
                output += i.tostring(n+2)
        else:
            output += self.compar_primer.tostring(n)
        return output
        
@dataclass
class Equality:
    comp1: Comparison
    op: Optional["Token"]=None
    rcomp: List["Comparison"] = field(default_factory=list)
    def tostring(self, n):
        output = ""
        if self.rcomp:
            output += " " * (n) + self.op.value + "\n"
            output += self.comp1.tostring(n+2)
            for i in self.rcomp:
                output += i.tostring(n+2)
        else:
            output += self.comp1.tostring(n)
        
        return output

@dataclass
class LogicAnd:
    first_equlist: Equality
    equalitys: List[Equality] = field(default_factory=list)
    def tostring(self, n):
        output = ""
        if self.equalitys:
            output += " " * (n) + "and\n"
            output += self.first_equlist.tostring(n+2)
            for i in self.equalitys:
                output += i.tostring(n+2)
        else:
            output += self.first_equlist.tostring(n)
        return output
        

@dataclass
class LogicOr:
    first_logicAnd: LogicAnd
    logicosY: List[LogicAnd] = field(default_factory=list)

    def tostring(self, n):
        output = ""
        if self.logicosY:
            output += " " * (n) + "or\n"
            output += self.first_logicAnd.tostring(n+2)
        else:
            output += self.first_logicAnd.tostring(n)

        for i in self.logicosY:
            output += i.tostring(n+2)
        return output


@dataclass
class Assignment:
    pass


@dataclass
class AssigmentWithAssigment(Assignment):
    identificador: Token
    assignm: Assignment
    call: Optional["Call"]=None

    def tostring(self, n):
        output = ""
        output += " " * (n) + "=" + "\n"
        if self.call:
            output += self.call.tostring(n + 2)
            output += " " * (n) + "." + "\n"
        if self.identificador.tipo != "TIdentifier":
            return "EORR assigments"
        output += " " * (n) + self.identificador.value + "\n"
        output += self.assignm.tostring(n+2)
        return output
        


@dataclass
class AssigmentWithLogicOr(Assignment):
    logicOr: LogicOr
    def tostring(self, n):
        output = ""
        output += self.logicOr.tostring(n)
        return output
        


@dataclass
class Expression:
    assig: Assignment 
    def tostring(self, n):
        output = ""
        output += self.assig.tostring(n)
        return output







#Declarations
@dataclass
class ClassDeclaration():
    class_name: Token
    father: Optional["Token"] = None
    methods: List["Function"] = field(default_factory=list)

    def tostring(self, n):
        output = ""
        output += " "*(n) + "class" + "\n"
        output += " "*(n) + self.class_name.value + "\n"
        if self.father:
            output += " "*(n) + "<" + "\n"
            output += " "*(n) + self.father.value + "\n"
        if self.methods:
            output += " "*(n) + "{" + "\n"
            for m in self.methods:  
                output += m.tostring(n+2)
            output += " "*(n) + "}" + "\n"
        return output
    

@dataclass
class FunctionDeclaration():
    fun: "Function"

    def tostring(self, n):
        output = ""
        output += " "*(n) + "fun" + "\n"
        output += " "*(n) + self.fun.tostring(0) + "\n"
        return output


@dataclass
class VarDeclaration():
    name: Token
    expr: Optional["Expression"] = None
    def tostring(self, n):
        output = ""
        output += " "*(n) + "var" + "\n"
        output += " "*(n + 2) + self.name.value + "\n"
        if self.expr:
            output += " "*(n) + "=" + "\n"
            output += " "*(n) + self.expr.tostring(n + 2) + "\n"
        output += " "*(n) + ";" + "\n"
        return output
    


#Statements
@dataclass
class ExprStmt:
    express: Expression
    def tostring(self, n):
        output = ""
        output += self.express.tostring(n + 2)
        output += " " * (n) + ";" + "\n"
        return output
    

@dataclass
class ForStmt:
    state: "Statement"
    var: Optional["VarDeclaration"] = None 
    expr: Optional["ExprStmt"] = None 
    exp1: Optional["Expression"] = None 
    exp2: Optional["Expression"] = None 
    
    def tostring(self, n):
        output = ""
        output += " "*(n) + "for" + "\n"
        output += " "*(n) + "(" + "\n"
        if self.var:
            output += self.var.tostring(n + 2)
        elif self.expr:
            output += self.expr.tostring(n + 2)
        else:
            output += " "*(n) + ";" + "\n"

        if self.exp1:
            output += self.exp1.tostring(n + 2)

        if self.exp2:
            output += self.exp2.tostring(n + 2)
            output += " "*(n) + ")" + "\n"
        else:
            output += " "*(n) + ")" + "\n"
        output += self.state.tostring(n + 2)
        return output
    

@dataclass
class IfStmt:
    exp : Expression
    state : "Statement"
    else_state : Optional["Statement"] = None
    def tostring(self, n):
        output = ""
        output += " "*(n) + "if" + "\n"
        output += " "*(n) + "(" + "\n"
        output += self.exp.tostring(n + 2)
        output += " "*(n) + ")" + "\n"
        output += self.state.tostring(n + 2)
        if self.else_state:
            output += " "*(n) + "else" + "\n"
            output += self.else_state.tostring(n + 2)
        return output


@dataclass 
class PrintStmt:
    expres: Expression
    def tostring(self, n):
        output = ""
        output += " " * (n) + "print" + "\n"
        output += self.expres.tostring(n + 2) + "\n"
        output += " " * (n) +";"
        return output

@dataclass
class ReturnStmt:
    expres: Expression
    def tostring(self, n):
        output = ""
        output += " " * (n) + "return" + "\n"
        output += self.expres.tostring(n+2) + "\n"
        output += " " * (n) + ";" + "\n"
        return output

@dataclass
class WhileStmt:
    exp: Expression
    state: "Statement"
    def tostring(self, n):
        output = ""
        output += " "*(n) + "while" + "\n"
        output += " "*(n) + "(" + "\n"
        output += self.exp.tostring(n + 2)
        output += " "*(n) + ")" + "\n"
        output += self.state.tostring(n + 2)
        return output

@dataclass
class Block:
    decl_list: List["Declaration"] = field(default_factory=list)

    def tostring(self, n):
        output = ""
        if self.decl_list:
            output +=  " "*(n) + "{" + "\n"
            for decl in self.decl_list:    
                output += decl.tostring(n + 2)
            output += "\n" + " "*(n) + "}" + "\n"
        return output


@dataclass
class Statement:
    exprStmt: Optional["ExprStmt"] = None 
    forStmt: Optional["ForStmt"] = None
    ifStmt: Optional["IfStmt"] = None
    printStmt: Optional["PrintStmt"] = None
    returnStmt: Optional["ReturnStmt"] = None
    whileStmt: Optional["WhileStmt"] = None
    blockst: Optional["Block"] = None
    def tostring(self, n):
        if self.exprStmt:
            return self.exprStmt.tostring(n)
        elif self.forStmt:
            return self.forStmt.tostring(n)
        elif self.ifStmt:
            return self.ifStmt.tostring(n)
        elif self.printStmt:
            return self.printStmt.tostring(n)
        elif self.returnStmt:
            return self.returnStmt.tostring(n)
        elif self.whileStmt:
            return self.whileStmt.tostring(n)
        elif self.blockst:
            return self.blockst.tostring(n)
        else:
            return "EORR No statement"
    

            
#Utility Rules
@dataclass
class Function:
    name: Token
    body: Block
    params: Optional["Parameters"]=None

    def tostring(self, n):
        output = ""
        output += " "*n +self.name.value + "\n"
        output += " "*n + "( \n"
        if self.params:
            output += self.params.tostring(n + 2)
            output += " "*n + ")\n"
        else:
            output += " "*n + ")\n"
        output += self.body.tostring(n+2)
        return output


@dataclass
class Parameters:
    primer_param: Token
    lista_param: List[Token] = field(default_factory=list) 
    def tostring(self, n):
        output = ""
        output += " " * (n) + self.primer_param.value + "\n"
        if self.lista_param:
            for ident in self.lista_param:
                output += " " * (n) + "," + "\n"
                output += " " * (n) +ident.value + "\n"
        return output


@dataclass
class Arguments:
    primer_Expression: Expression
    expressionrest: List[Expression] = field(default_factory=list)

    def tostring(self, n):   
        output = ""
        output += self.primer_Expression.tostring(n)
        if self.expressionrest:
            for expr in self.expressionrest:
                output +=  " " * n +  "," + "\n"
                output += self.expression1.tostring(n)
        return output




@dataclass
class Declaration:
    clasDecl: Optional["ClassDeclaration"] = None
    funDecl: Optional["FunctionDeclaration"] = None
    varDecl: Optional["VarDeclaration"] = None
    state: Optional["Statement"] = None
    def tostring(self, n):
        output = ""
        if self.clasDecl:
            output += self.clasDecl.tostring(n)
        elif self.funDecl:
            output += self.funDecl.tostring(n)
        elif self.varDecl:
            output += self.varDecl.tostring(n)
        elif self.state:
            output += self.state.tostring(n)
        return output


#Syntax Grammar
@dataclass
class Program:
    declarations: List[Declaration]
    def tostring(self, n):
        output = ""
        for decl in self.declarations:
            output +=  " " * (n) + decl.tostring(n) + "\n"
        return output


