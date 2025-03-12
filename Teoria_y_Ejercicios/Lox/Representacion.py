from abc import abstractmethod
from dataclasses import dataclass

from Lexer import Token
from typing import List, Literal, Tuple, Optional


@dataclass
class Primary:

    @abstractmethod
    def tostring(self):
        raise NotImplementedError


@dataclass
class NUMBER(Primary):
    tok: Token

    def tostring(self):
        s = " " + str(self.tok.tipo) + "\n"
        s += "   " + self.tok.value
        return s


@dataclass
class STRING(Primary):
    tok: Token

    def tostring(self):
        s = " " + str(self.tok.tipo) + "\n"
        s += "   " + self.tok.value
        return s


@dataclass
class IDENTIFIER(Primary):
    tok: Token

    def tostring(self):
        s = " " + str(self.tok.tipo) + "\n"
        s += "   " + self.tok.value
        return s


@dataclass
class Expression:

    @abstractmethod
    def tostring(self):
        raise NotImplementedError


@dataclass
class Arguments:
    expr: List[Expression]

    def tostring(self):
        s = self.expr[0]
        if len(self.expr) >= 2:
            for expr in self.expr[1:]:
                s += ", "
                s += expr
        return s


@dataclass
class Parameters:
    names: List[IDENTIFIER]

    def tostring(self):
        s = self.names[0]
        if len(self.names) >= 2:
            for name in self.names[1:]:
                s += ", "
                s += name
        return s


@dataclass
class Function:
    name: IDENTIFIER
    params: Parameters
    body: "Block"

    def tostring(self):
        s = self.name
        s += "("
        s += self.params.tostring()
        s += ")"
        s += self.body.tostring()
        return s


@dataclass
class Call(Primary):
    base: Primary
    args: Optional[Arguments]
    properties: List[Tuple[IDENTIFIER, Optional[Arguments]]]

    def tostring(self):
        s = self.base.tostring()

        for prop, args in self.properties:
            s += "."
            s += str(prop)
            if args:
                s += "("
                s += args.tostring()
                s += ")"

        if self.args is not None:
            s += "("
            s += self.args.tostring()
            s += ")"

        return s


@dataclass
class Unary:
    op: Literal["!", "="]
    attr: "Unary" | Call

    def tostring(self):
        s = self.op
        s += self.attr.tostring()
        return s


@dataclass
class Factor:
    unary: Unary
    other_unary: List[Tuple[Literal["/", "*"], Unary]]

    def tostring(self):
        s = self.unary.tostring()
        if self.other_unary:
            for unary in self.other_unary:
                s += " " + unary[0] + " "
                s += unary[1].tostring()
        return s


@dataclass
class Term:
    factor: Factor
    other_factor: List[Tuple[Literal["-", "+"], Factor]]

    def tostring(self):
        s = self.factor.tostring()
        if self.other_factor:
            for factor in self.other_factor:
                s += " " + factor[0] + " "
                s += factor[1].tostring()
        return s


@dataclass
class Comparison:
    term: Term
    other_term: List[Tuple[Literal[">", ">=", "<", "<="], Term]]

    def tostring(self):
        s = self.term.tostring()
        if self.other_term:
            for term in self.other_term:
                s += " " + term[0] + " "
                s += term[1].tostring()
        return s


@dataclass
class Equality:
    comp: Comparison
    other_comp: List[Tuple[Literal["!=", "=="], Comparison]]

    def tostring(self):
        s = self.comp.tostring()
        if self.other_comp:
            for comp in self.other_comp:
                s += " " + comp[0] + " "
                s += comp[1].tostring()
        return s


@dataclass
class LogicAnd:
    equality: List[Equality]

    def tostring(self):
        s = self.equality[0].tostring()
        if len(self.equality) >= 2:
            for equality in self.equality[1:]:
                s += " and "
                s += equality.tostring()
        return s


@dataclass
class LogicOr:
    logic_and: List[LogicAnd]

    def tostring(self):
        s = self.logic_and[0].tostring()
        if len(self.logic_and) >= 2:
            for logic_and in self.logic_and[1:]:
                s += " or "
                s += logic_and.tostring()
        return s


@dataclass
class Assignment(Expression):
    call: Call
    name: str
    assign: "Assignment"
    logic_or: LogicOr

    def tostring(self):
        s = ""
        if self.logic_or:
            s = self.logic_or.tostring()
        else:
            if self.call:
                s += self.call.tostring() + "."
            s += self.name
            s += " = "
            s += self.assign.tostring()
        return s


@dataclass
class Declaration:

    @abstractmethod
    def tostring(self):
        raise NotImplementedError


@dataclass
class ClassDecl(Declaration):
    name: str
    father: str
    methods: List[Function]

    def tostring(self):
        s = "class"
        s += " "
        s += self.name
        if self.father:
            s += " < " + self.father
        return s


@dataclass
class FunDecl(Declaration):
    fun: Function

    def tostring(self):
        s = "fun"
        s += self.fun.tostring()
        return s


@dataclass
class VarDecl(Declaration):
    name: str
    expr: Expression

    def tostring(self):
        s = "var"
        s += " "
        s += self.name
        if self.expr:
            s += " = " + self.expr.tostring()
        return s


@dataclass
class Statement(Declaration):

    @abstractmethod
    def tostring(self):
        raise NotImplementedError


@dataclass
class ExprStmt(Statement):
    expr: Expression

    def tostring(self):
        s = self.expr.tostring()
        s += ";"
        return s


@dataclass
class ForStmt(Statement):
    start: VarDecl | ExprStmt | Literal[";"]
    med: Expression
    end: Expression
    stmt: Statement

    def tostring(self):
        s = "for"
        s += "("
        s += self.start.tostring()
        if self.med:
            s += self.med.tostring()
        if self.end:
            s += self.end.tostring()
        s += ")"
        s += self.stmt.tostring()
        return s


@dataclass
class IfStmt(Statement):
    cond: Expression
    then_stmt: Statement
    else_stmt: Statement

    def tostring(self):
        s = "if"
        s += "("
        s += self.cond.tostring()
        s += ")"
        s += self.then_stmt.tostring()
        if self.else_stmt:
            s += "else" + self.else_stmt.tostring()
        return s


@dataclass
class PrintStmt(Statement):
    expr: Expression

    def tostring(self):
        s = "print"
        s += " "
        s += self.expr.tostring()
        s += ";"
        return s


@dataclass
class ReturnStmt(Statement):
    expr: Expression

    def tostring(self):
        s = "return"
        if self.expr:
            s += self.expr.tostring()
        s += ";"
        return s


@dataclass
class WhileStmt(Statement):
    cond: Expression
    stmt: Statement

    def tostring(self):
        s = "while"
        s += "("
        s += self.cond.tostring()
        s += ")"
        s += self.stmt.tostring()
        return s


@dataclass
class Block(Statement):
    decl: List[Declaration]

    def tostring(self):
        s = "{"
        if self.decl:
            for decl in self.decl:
                s += decl.tostring()
        s += "}"
        return s


@dataclass
class Program:
    declarations: List[Declaration]
