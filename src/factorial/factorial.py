#!/usr/bin/python
#*-----------------------------------------------------------------------*
#* factorial.py                                                           *
#* calcula el factorial de un número o rango desde-hasta                 *
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
    entrada = input("Ingrese un número o rango (ej: 10 o 4-8): ")
    args = entrada.strip()
else:
    args = sys.argv[1]

# Detecta si es un rango desde-hasta (ej: 4-8)
if "-" in args and not args.startswith("-"):
    partes = args.split("-")
    desde = int(partes[0])   # convierte string a entero
    hasta = int(partes[1])   # convierte string a entero
    for i in range(desde, hasta + 1):
        print("Factorial ", i, "! es ", factorial(i))
else:
    num = int(args)
    print("Factorial ", num, "! es ", factorial(num))
