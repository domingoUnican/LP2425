# LoxFunction.py
# Este código es una implementación en Python del intérprete Lox,
# basada en el libro "Crafting Interpreters" de Robert Nystrom:
# https://craftinginterpreters.com/
__author__ = "Rubén Martínez Amodia"
__version__ = "2025"

from Environment import Environment
from Representacion import Function
from LoxCallable import LoxCallable
from Return import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            param_name = self.declaration.params[i].lexeme
            environment.define(param_name, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None
