#!/usr/bin/python
#*-----------------------------------------------------------------------*
#* factorial.py                                                           *
#* calcula el factorial de un número, rango desde-hasta,                 *
#* -hasta (desde 1) o desde- (hasta 60)                                  *
#* Dr.P.E.Colla (c) 2022                                                 *
#* Creative commons                                                       *
#*-----------------------------------------------------------------------*
import sys

def factorial(num):
    if num < 0:
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0:
        return 1
    else:
        fact = 1
        while(num > 1):
            fact *= num
            num -= 1
        return fact

# Si no se pasa argumento, se lo solicita al usuario
if len(sys.argv) == 1:
    entrada = input("Ingrese un número, rango (4-8), (-10) o (4-): ")
    args = entrada.strip()
else:
    args = sys.argv[1]

# Caso: -hasta → sin límite inferior, calcula desde 1 hasta el número indicado
# Ejemplo: -10 calcula factoriales del 1 al 10
if args.startswith("-") and args[1:].isdigit():
    hasta = int(args[1:])        # convierte string a entero
    for i in range(1, hasta + 1):
        print("Factorial ", i, "! es ", factorial(i))

# Caso: desde- → sin límite superior, calcula desde el número indicado hasta 60
# Ejemplo: 4- calcula factoriales del 4 al 60
elif args.endswith("-") and args[:-1].isdigit():
    desde = int(args[:-1])       # convierte string a entero
    for i in range(desde, 61):
        print("Factorial ", i, "! es ", factorial(i))

# Caso: desde-hasta → calcula entre ambos extremos
# Ejemplo: 4-8 calcula factoriales del 4 al 8
elif "-" in args:
    partes = args.split("-")
    desde = int(partes[0])       # convierte string a entero
    hasta = int(partes[1])       # convierte string a entero
    for i in range(desde, hasta + 1):
        print("Factorial ", i, "! es ", factorial(i))

# Caso: número simple
# Ejemplo: 10 calcula el factorial de 10
else:
    num = int(args)              # convierte string a entero
    print("Factorial ", num, "! es ", factorial(num))
