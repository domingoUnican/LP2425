# AUTOR: NICOLÁS RECINELLA VIDÁN 
# Ejercicio 0 - warmup.py
#
# Un ejercicio de calentamiento para ilustrar algunos de los conceptos básicos de
# compiladores. Define una máquina virtual mínima. Las prácticas son
# escribir tres programas basados ​​en esta máquina. Seguir instrucciones
# cerca del final de este archivo.
# ------------------------------------------------- ---------------------

# TinyVM.
#
# Una pequeña máquina virtual. La máquina tiene 8 registros (R0, R1, ..., R7)
# y comprende las siguientes 8 instrucciones, que están codificadas como
# tuplas.
#
# ('ADD', 'Ra', 'Rb', 'Rd') -> Rd = Ra + Rb
# ('SUB', 'Ra', 'Rb', 'Rd') -> Rd = Ra - Rb
# ('MOV', valor, 'Rd') -> Rd = valor
# ('LD', 'Rs', 'Rd', offset) -> Rd = MEMORIA [Rs + desplazamiento]
# ('ST', 'Rs', 'Rd', offset) -> MEMORIA [Rd + desplazamiento] = Rs
# ('JMP', 'Rd', offset) -> PC = Rd + desplazamiento
# ('BRZ', 'Rt', offset) -> si Rt == 0: PC = PC + desplazamiento
# ('HALT,) -> Detiene la máquina
#
# En las instrucciones anteriores, 'Rx' significa algún número de registro como
# como R0, R1, etc. Inicialmente, la máquina inicializa R0, ..., R6 a 0.
# R7 se inicializa a la última dirección de memoria válida.


class Halt(Exception):
    pass


class TinyVM(object):
    def run(self, memory):
        '''
        Run a program. memory is a Python list containing the program
        instructions and other data.  Upon startup, all registers
        are initialized to 0.  R7 is initialized with the highest valid
        memory address.
        '''
        self.pc = 0
        self.registers = {f'R{d}': 0 for d in range(8)}
        self.memory = memory
        self.registers['R7'] = len(memory) - 1
        try:
            while True:
                op, *args = self.memory[self.pc]
                self.pc += 1
                getattr(self, op)(*args)
        except Halt:
            self.registers = {key: 0 for key in self.registers}
        return

    def ADD(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] + self.registers[rb]

    def SUB(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] - self.registers[rb]

    def MOV(self, value, rd):
        self.registers[rd] = value

    def LD(self, rs, rd, offset):
        self.registers[rd] = self.memory[self.registers[rs]+offset]

    def ST(self, rs, rd, offset):
        self.memory[self.registers[rd]+offset] = self.registers[rs]

    def JMP(self, rd, offset):
        self.pc = self.registers[rd] + offset

    def BRZ(self, rt, offset):
        if not self.registers[rt]:
            self.pc += offset

    def HALT(self):
        raise Halt()
    
            

machine = TinyVM()

# ------------------------------------------------- ---------------------
# Problema 1: Computadoras
#
# La CPU de una computadora ejecuta instrucciones de bajo nivel. Utilizando la
# La instrucción TinyVM establecida anteriormente, muestra cómo calcularía 2 + 3 - 4. 

prog1 = [  # Poner aquí las instrucciones
    ('MOV', 2, 'R1'),
    ('MOV', 3, 'R2'),
    ('MOV', 4, 'R3'),
    ('ADD', 'R1', 'R2', 'R4'),
    ('SUB', 'R4', 'R3', 'R4'),
    ('ST', 'R4', 'R7', 0),    # Cambiar el resultado por el registro
    ('HALT', ),
    0            # Guardar este valor en R7.
]

machine.run(prog1)
print('Resultado del programa 1:', prog1[-1], '(debería ser  1)')

# ------------------------------------------------- ---------------------
# Problema 2: Computación
#
# Escribir un programa TinyVM que calcule 23 * 37. Nota: La máquina
# no implementa la multiplicación, se debe deducir cómo
# para hacerlo.

prog2 = [  ('MOV', 23, 'R1'),
           ('MOV', 37, 'R2'),
           ('MOV', 23, 'R3'),    
           ('MOV', 1, 'R4'),
           ('SUB', 'R2', 'R4', 'R2'),
           ('BRZ', 'R2', 2),
           ('ADD', 'R1', 'R3', 'R3'),
           ('JMP', 'R4', 3),
           ('ST', 'R3', 'R7', 0),    # Cambiar el resultado por el registro     
           ('HALT',),
          0           # Resultado
        ]

machine.run(prog2)
print('Resultado del programa 1:', prog2[-1], f'(El resultado es {23*37})')

# ------------------------------------------------- ---------------------
# Problema 3: Abstracción
#
# Escribir una función de Python mul (x, y) que calcule x * y en TinyVM.
# Esta función debería abstraer los detalles; se supone que no se debe
# añadir nada sobre la implementacion. 


def mul(x, y):
    prog = [  # Instrucciones
             # ...
             ('MOV',x,'R1'),      # Input 1
             ('MOV',y,'R2'),      # Input 2
             ('BRZ', 'R2', 6),
             ('MOV',x,'R3'),    
             ('MOV', 1, 'R4'),
             ('SUB', 'R2', 'R4', 'R2'),
             ('BRZ', 'R2', 2),
             ('ADD', 'R1', 'R3', 'R3'),
             ('JMP', 'R4', 4),
             ('ST', 'R3', 'R7', 0),
             ('HALT',),
          x,        # Input 1
          y,        # Input 2
          0         # Resultado
    ]
    machine.run(prog)
    return prog[-1] 

print(f'Problema 3: 51 * 53 = {mul(51, 53)}. El resultado es {51*53}.')

# ------------------------------------------------- ---------------------
# Problema 4: Desafío
#
# Rescribir esta función de Python recursiva como un solo conjunto de TinyVM
# instrucciones que calculen recursivamente el mismo resultado.


def fib(n):
    if n <= 2:
        if n == 0:
            return 0
        return 1
    else:
        return fib(n-1) + fib(n-2)

# Your rewritten version should look like this:


def fib_vm(n):
    prog = [
        ('MOV', n, 'R1'),    # R1 = n
        ('BRZ', 'R1', 13),    # Si n == 0, saltamos al final con Fib(0) = 0
        ('MOV', 1, 'R2'),    # R2 = Fib(1) = 1
        ('MOV', 1, 'R3'),    # R3 = Fib(2) = 1
        ('MOV', 1, 'R6'),    # R6 = 1
        ('SUB', 'R1', 'R2', 'R4'),  # R4 = n - 1
        ('BRZ', 'R4', 6),    # Si n == 1, saltamos al final con Fib(1) = 1
        ('MOV', 2, 'R5'),    # R5 = 2 (contador de iteraciones)
        
        # Bucle de Fibonacci:
        ('SUB', 'R1', 'R5', 'R4'),  # R4 = n - contador
        ('BRZ', 'R4', 5),  # Si n - contador == 0, terminamos el bucle
        ('ADD', 'R2', 'R3', 'R4'),  # R4 = R2 + R3 (Fib(n) = Fib(n-1) + Fib(n-2))
        ('ADD', 'R0','R3', 'R2'),  # R2 = R3
        ('ADD', 'R0','R4', 'R3'),  # R3 = R4
        ('ADD', 'R5', 'R6', 'R5'),  # Incrementamos el contador
        ('JMP', 'R6', 7),  # Volvemos al inicio del bucle

        # Guardamos el resultado en memoria:
        ('ST', 'R3', 'R7', 0),  
        ('HALT',),
        n,  # Input n
        0   # Resultado
    ]
    machine.run(prog)
    return prog[-1]

# Prueba con fib(10)
print(f'Problema 4: fib(10) = {fib_vm(10)}. El resultado es {fib(10)}.')