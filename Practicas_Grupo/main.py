import os
import re
import sys
from colorama import init
from termcolor import colored

init()

DIRECTORIO = os.path.expanduser("./")
sys.path.append(DIRECTORIO)

from Lexer import *
from Parser import *
from Clases import *

PRACTICA = "02"  # Practica que hay que evaluar
DEBUG = True  # Decir si se lanzan mensajes de debug
NUMLINEAS = 10  # Numero de lineas que se muestran antes y después de la no coincidencia
DIR = os.path.join(DIRECTORIO, PRACTICA, "grading")
FICHEROS = os.listdir(DIR)
TESTS = [
    fich
    for fich in FICHEROS
    if os.path.isfile(os.path.join(DIR, fich))
    and re.search(r"^[a-zA-Z].*\.(cool|test|cl)$", fich)
]
TESTS.sort()
ficheros_fallidos = []  # Lista de ficheros fallidos
for fich in TESTS:
    lexer = CoolLexer()
    f = open(os.path.join(DIR, fich), "r", newline="")
    g = open(os.path.join(DIR, fich + ".out"), "r", newline="")
    if os.path.isfile(os.path.join(DIR, fich) + ".nuestro"):
        os.remove(os.path.join(DIR, fich) + ".nuestro")
    if os.path.isfile(os.path.join(DIR, fich) + ".bien"):
        os.remove(os.path.join(DIR, fich) + ".bien")
    entrada = f.read()
    f.close()

    if PRACTICA == "01":
        texto = "\n".join(lexer.salida(entrada))
        texto = f'#name "{fich}"\n' + texto
        resultado = g.read()
        g.close()
        if texto.strip().split() != resultado.strip().split():
            print(f"Revisa el fichero {fich}")
            ficheros_fallidos.append(fich)
            if DEBUG:
                texto = re.sub(r"#\d+\\b", "", texto)
                resultado = re.sub(r"#\d+\\b", "", resultado)
                nuestro = [linea for linea in texto.split("\n") if linea]
                bien = [linea for linea in resultado.split("\n") if linea]
                linea = 0
                while (
                    nuestro[linea : linea + NUMLINEAS]
                    == bien[linea : linea + NUMLINEAS]
                ):
                    linea += 1
                print(
                    colored(
                        "\n".join(nuestro[linea : linea + NUMLINEAS]),
                        "white",
                        "on_red",
                    )
                )
                print(
                    colored(
                        "\n".join(bien[linea : linea + NUMLINEAS]),
                        "blue",
                        "on_green",
                    )
                )
                f = open(os.path.join(DIR, fich) + ".nuestro", "w")
                g = open(os.path.join(DIR, fich) + ".bien", "w")
                f.write(texto.strip())
                g.write("".join(bien))
                f.close()
                g.close()
    elif PRACTICA in ("02", "03"):
        parser = CoolParser()
        parser.nombre_fichero = fich
        parser.errores = []
        bien = "".join([c for c in g.readlines() if c and "#" not in c])
        g.close()
        j = parser.parse(lexer.tokenize(entrada))
        try:
            #j.Tipo() # TODO
            if j and not parser.errores:
                resultado = "\n".join(
                    [c for c in j.str(0).split("\n") if c and "#" not in c]
                )
            else:
                resultado = "\n".join(parser.errores)
                resultado += "\n" + "Compilation halted due to lex and parse errors"
            if resultado.lower().strip().split() != bien.lower().strip().split():
                print(f"Revisa el fichero {fich}")
                ficheros_fallidos.append(fich)
                # Guardar los ficheros .nuestro y .bien
                with open(os.path.join(DIR, fich) + ".nuestro", "w") as f_nuestro:
                    f_nuestro.write(resultado.strip())
                with open(os.path.join(DIR, fich) + ".bien", "w") as f_bien:
                    f_bien.write(bien.strip())
                contexto_antes = 1  # Una línea antes del error
                contexto_despues = 10  # Diez líneas después del error
                for i, (line_res, line_bien) in enumerate(zip(resultado.splitlines(), bien.splitlines()), start=1):
                    if line_res.strip().lower().split() != line_bien.strip().lower().split():
                        print(f"Diferencia en la línea {i}:")
                        inicio = max(0, i - 1 - contexto_antes)
                        fin = i + contexto_despues
                        res_lines = resultado.splitlines()
                        bien_lines = bien.splitlines()
                        for j in range(inicio, fin):
                            if j >= len(res_lines) and j >= len(bien_lines):
                                break
                            res = res_lines[j] if j < len(res_lines) else ""
                            bien_ = bien_lines[j] if j < len(bien_lines) else ""
                            if j == i - 1:
                                col_res = colored(f">> {res}", "white", "on_red")
                                col_bien = colored(f">> {bien_}", "white", "on_green")
                            else:
                                col_res = colored(f"   {res}", "white", "on_red")
                                col_bien = colored(f"   {bien_}", "white", "on_green")
                            print(f"  nuestro  : {col_res}")
                            print(f"  bien     : {col_bien}")
                        break
        except Exception as e:
            print(f"Lanza excepción en {fich} con el texto {e}")
if ficheros_fallidos:
    print("\nFicheros fallidos:")
    for f in ficheros_fallidos:
        print(f"- {f}")
print(f"\nTotal de ficheros fallidos: {len(ficheros_fallidos)}")