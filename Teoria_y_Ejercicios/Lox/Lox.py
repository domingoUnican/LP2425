# Lox.py
# Este código es una implementación en Python del intérprete Lox,
# basada en el libro "Crafting Interpreters" de Robert Nystrom:
# https://craftinginterpreters.com/
__author__ = "Rubén Martínez Amodia"
__version__ = "2025"

import sys

from AstPrinter import AstPrinter
from Parser import Parser
from Scanner import Scanner, TokenType


class Lox:
    had_error = False
    had_runtime_error = False

    @staticmethod
    def main(args):
        if len(args) > 2:
            print("Usage: python Lox.py [script]")
            sys.exit(64)
        elif len(args) == 2:
            Lox.run_file(args[1])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path):
        with open(path, "r", encoding="utf-8") as file:
            source = file.read()
        Lox.run(source)

        # Indicate an error in the exit code.
        if Lox.had_error:
            sys.exit(65)
        if Lox.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                if line is None:
                    break
                Lox.run(line)
                Lox.had_error = False
            except EOFError:
                break

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()

        # Stop if there was a syntax error.
        if Lox.had_error:
            return

        print("____TOKENS____")
        for token in tokens:
            print(token.tostring())

        print("____AST_TREE____")
        for stmt in statements:
            print(AstPrinter().print(stmt))

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        sys.stderr.write(f"[line {line}] Error{where}: {message}\n")
        Lox.had_error = True

    @staticmethod
    def error_token(token, message):
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.text}'", message)

    @staticmethod
    def runtime_error(error):
        sys.stderr.write(f"{error.message}\n[line {error.token.line}]\n")
        Lox.had_runtime_error = True


if __name__ == "__main__":
    Lox.main(sys.argv)
