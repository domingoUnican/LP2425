# RuntimeError.py
# Este código es una implementación en Python del intérprete Lox,
# basada en el libro "Crafting Interpreters" de Robert Nystrom:
# https://craftinginterpreters.com/
__author__ = "Rubén Martínez Amodia"
__version__ = "2025"

from Scanner import Token


class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
