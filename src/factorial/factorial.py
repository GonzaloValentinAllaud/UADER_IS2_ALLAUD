#!/usr/bin/python
#*-----------------------------------------------------------------------*
#* factorial.py                                                           *
#* calcula el factorial de un número, rango desde-hasta,                 *
#* -hasta (desde 1) o desde- (hasta 60)                                  *
#* Dr.P.E.Colla (c) 2022                                                 *
#* Creative commons                                                       *
#*-----------------------------------------------------------------------*

# Librería para manejar argumentos de línea de comandos
import sys

def factorial(num):
    """Calcula el factorial de un número entero no negativo"""

    # No existe el factorial de números negativos
    if num < 0:
        print("Factorial de un número negativo no existe")
        return 0
    
    # Caso base: el factorial de 0 es 1
    elif num == 0:
        return 1
    
    # Caso general: multiplica de forma iterativa
    else:
        fact = 1
        while(num > 1):
            fact *= num   # acumula la multiplicación
            num -= 1      # decrementa el contador
        return fact

#-----------------------------------------------------------------------
# Procesamiento de argumentos
#-----------------------------------------------------------------------

# Si no se recibe ningún argumento, se solicita al usuario por teclado
if len(sys.argv) == 1:
    entrada = input("Ingrese un número, rango (4-8), (-10) o (4-): ")
    args = entrada.strip()   # elimina espacios en blanco
else:
    args = sys.argv[1]       # toma el primer argumento de la línea de comandos

#-----------------------------------------------------------------------
# Detección del tipo de entrada y cálculo correspondiente
#-----------------------------------------------------------------------

# Caso 1: -hasta → sin límite inferior
# Calcula factoriales desde 1 hasta el número indicado
# Ejemplo: -10 calcula del 1 al 10
if args.startswith("-") and args[1:].isdigit():
    hasta = int(args[1:])        # convierte string a entero
    for i in range(1, hasta + 1):
        print("Factorial ", i, "! es ", factorial(i))

# Caso 2: desde- → sin límite superior
# Calcula factoriales desde el número indicado hasta 60
# Ejemplo: 4- calcula del 4 al 60
elif args.endswith("-") and args[:-1].isdigit():
    desde = int(args[:-1])       # convierte string a entero
    for i in range(desde, 61):
        print("Factorial ", i, "! es ", factorial(i))

# Caso 3: desde-hasta → rango completo
# Calcula factoriales entre ambos extremos indicados
# Ejemplo: 4-8 calcula del 4 al 8
elif "-" in args:
    partes = args.split("-")
    desde = int(partes[0])       # convierte string a entero
    hasta = int(partes[1])       # convierte string a entero
    for i in range(desde, hasta + 1):
        print("Factorial ", i, "! es ", factorial(i))

# Caso 4: número simple
# Calcula el factorial de un único número
# Ejemplo: 10 calcula el factorial de 10
else:
    num = int(args)              # convierte string a entero
    print("Factorial ", num, "! es ", factorial(num))
