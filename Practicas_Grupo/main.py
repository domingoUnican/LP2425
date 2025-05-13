import os
import re
import sys
#from colorama import init
#from termcolor import colored
#init()


#DIRECTORIO = os.path.expanduser("C:\Users\David\Documents\Ing. Informática\Teoria del Cuarto Curso de ing. Informatica\LenguajesDeProgramacion\Repositorios\LP2425")
DIRECTORIO = "."
sys.path.append(DIRECTORIO)

from Lexer import *
from Parser import *
from Clases import *

# Ultima version
tipo_test = r'grading'
PRACTICA = r"01" # Practica que hay que evaluar
DEBUG = True   # Decir si se lanzan mensajes de debug
NUMLINEAS = 3   # Numero de lineas que se muestran antes y después de la no coincidencia
sys.path.append(DIRECTORIO)
DIR = os.path.join(DIRECTORIO, PRACTICA, tipo_test)
FICHEROS = os.listdir(r"./"+PRACTICA+r"/"+tipo_test)
TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(DIR, fich)) and
         re.search(r"^[a-zA-Z].*\.(cool|test|cl)$",fich)]
TESTS.sort()
#TESTS = ["associativity-.test"]

if True:
    for fich in TESTS:
        lexer = CoolLexer()
        f = open(os.path.join(DIR, fich), 'r', newline='')
        g = open(os.path.join(DIR, fich + '.out'), 'r', newline='')
        if os.path.isfile(os.path.join(DIR, fich)+'.nuestro'):
            os.remove(os.path.join(DIR, fich)+'.nuestro')
        if os.path.isfile(os.path.join(DIR, fich)+'.bien'):
            os.remove(os.path.join(DIR, fich)+'.bien')            
        texto = ''
        entrada = f.read()
        f.close()
        if PRACTICA == '01':
            texto = '\n'.join(lexer.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            #print(texto)
            resultado = g.read()
            g.close()
            a = texto.strip().split()
            b = resultado.strip().split()
            a = [c for c in a if c[0] != '#']
            b = [c for c in b if c[0] != '#']
            if a != b:
                print(f"Revisa el fichero {fich}")
                if DEBUG:
                    texto = re.sub(r'#\d+\b','',texto)
                    resultado = re.sub(r'#\d+\b','',resultado)
                    nuestro = [linea + '\r' for linea in texto.split('\n') if linea]
                    bien = [linea for linea in resultado.split('\n') if linea]
                    #print(nuestro)
                    #print(bien)
                    #for i,j in zip(nuestro, bien):
                    #    if i.strip() != j.strip():
                    #        print('fich:', fich)
                    #        print(f"Nuestro: {i}")
                    #        print(f"Bien: {j}")
                    #        break
                    #print('###############################3')
                    #print(resultado)
                    linea = 0
                    while nuestro[linea:linea+NUMLINEAS] == bien[linea:linea+NUMLINEAS]:
                        linea += 1
                    #print(colored('\n'.join(nuestro[linea:linea+NUMLINEAS]), 'white', 'on_red'))
                    #print(colored('\n'.join(bien[linea:linea+NUMLINEAS]), 'blue', 'on_green'))
                    f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                    f.write(texto.strip())
                    f.close()
                    g = open(os.path.join(DIR, fich)+'.bien', 'w')
                    g.write(resultado.strip())
                    g.close()
        elif PRACTICA in ('02', '03'):
            parser = CoolParser()
            parser.nombre_fichero = fich
            parser.errores = []
            bien = ''.join([c for c in g.readlines() if c and '#' not in c])
            bien_total = bien
            
            g.close()
            
            j = parser.parse(lexer.tokenize(entrada))
            try:
                
                #j.Tipo()
                if j and not parser.errores:
                    resultado = '\n'.join([c for c in j.str(0).split('\n')
                                           if c and '#' not in c])
                else:
                    resultado = '\n'.join(parser.errores)
                    resultado += '\n' + "Compilation halted due to lex and parse errors"
                if resultado.lower().strip().split() != bien.lower().strip().split():
                    print(f"Revisa el fichero {fich}")
                    if DEBUG:
                        nuestro = [linea for linea in resultado.split('\n') if linea]
                        bien = [linea for linea in bien.split('\n') if linea]
                        linea = 0
                        #while nuestro[linea:linea+NUMLINEAS] == bien[linea:linea+NUMLINEAS]:
                        #    linea += 1
                        #print(colored('\n'.join(nuestro[linea:linea+NUMLINEAS]), 'white', 'on_red'))
                        #print(colored('\n'.join(bien[linea:linea+NUMLINEAS]), 'blue', 'on_green'))
                        f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                        g = open(os.path.join(DIR, fich)+'.bien', 'wb')
                        f.write(resultado.strip())
                        g.write(bien_total.strip().encode('ascii'))
                        f.close()
                        g.close()
                        #print(bien_total)
                        #print("Alcanzado el final")
            except Exception as e:
                print(f"Lanza excepción en {fich} con el texto {e}")

