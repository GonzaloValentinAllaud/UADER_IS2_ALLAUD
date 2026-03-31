#!/usr/bin/python
#*-----------------------------------------------------------------------*
#* collatz.py                                                             *
#* Calcula la conjetura de Collatz para números entre 1 y 10000          *
#* y grafica las iteraciones necesarias para converger                   *
#*-----------------------------------------------------------------------*

# Librería para graficar
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
# Función que calcula los pasos de Collatz para un número n
#-----------------------------------------------------------------------
def collatz(n):
    """Calcula cuántas iteraciones tarda n en converger a 1"""
    
    # Contador de iteraciones
    iteraciones = 0
    
    # Aplica la conjetura hasta llegar a 1
    while n != 1:
        if n % 2 == 0:
            # Si n es par: dividir por 2
            n = n // 2
        else:
            # Si n es impar: multiplicar por 3 y sumar 1 (2n+1 generalizado)
            n = 3 * n + 1
        iteraciones += 1
    
    return iteraciones

#-----------------------------------------------------------------------
# Cálculo para todos los números entre 1 y 10000
#-----------------------------------------------------------------------

# Lista de números de inicio (eje Y - ordenadas)
numeros = list(range(1, 10001))

# Lista de iteraciones para cada número (eje X - abscisas)
iteraciones = []

print("Calculando conjetura de Collatz para números del 1 al 10000...")

for n in numeros:
    iteraciones.append(collatz(n))

print("Cálculo completado. Generando gráfico...")

#-----------------------------------------------------------------------
# Generación del gráfico
#-----------------------------------------------------------------------

# Tamaño del gráfico
plt.figure(figsize=(14, 6))

# Grafica puntos: eje X = iteraciones, eje Y = número de inicio
plt.scatter(iteraciones, numeros, s=0.5, color="steelblue", alpha=0.5)

# Títulos y etiquetas
plt.title("Conjetura de Collatz — Números del 1 al 10000")
plt.xlabel("Número de iteraciones para converger")
plt.ylabel("Número n de inicio de la secuencia")

# Cuadrícula para mejor lectura
plt.grid(True, linestyle="--", alpha=0.4)

# Ajuste del layout
plt.tight_layout()

# Guarda el gráfico como imagen
plt.savefig("collatz.png", dpi=150)
print("Gráfico guardado como collatz.png")

# Muestra el gráfico en pantalla
plt.show()