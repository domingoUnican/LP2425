import re

def convertir_cadena(dot_string):
    # Expresión regular para extraer A, B y C
    patron = r'(\w+)\s*->\s*(\w+)\s*\[label="(.+?)"\];'
    coincidencia = re.match(patron, dot_string.strip())

    if coincidencia:
        A, B, C = coincidencia.groups()
        return f'dfa[(TokenType.{A}, TypesLiteral.{C})] = TokenType.{B}'
    else:
        return None  # Si la línea no tiene el formato esperado, la ignoramos

def procesar_archivo(entrada, salida):
    with open(entrada, 'r', encoding='utf-8') as f_in, open(salida, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            resultado = convertir_cadena(linea)
            if resultado:
                f_out.write(resultado + '\n')

# Archivos de entrada y salida
archivo_entrada = "entrada.txt"  # Nombre del archivo con las cadenas DOT
archivo_salida = "salida.txt"    # Nombre del archivo donde se guardará el resultado

procesar_archivo(archivo_entrada, archivo_salida)
print(f"Conversión completada. Resultado guardado en '{archivo_salida}'")
