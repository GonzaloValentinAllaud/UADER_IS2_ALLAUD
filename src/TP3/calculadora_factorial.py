# PUNTO 1:
#Provea una clase que dado un número entero cualquiera retorne el factorial del 
#mismo, debe asegurarse que todas las clases que lo invoquen utilicen la misma 
#instancia de clase.


# ─── Clase Singleton ────────────────────────────────────────────────

class FactorialCalculator:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular_factorial(self, n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("El argumento debe ser un número entero.")
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos.")
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado


# ─── Clases que usan el Singleton ───────────────────────────────────

class ClaseA:
    def ejecutar(self):
        calc = FactorialCalculator()
        print(f"ClaseA - 5! = {calc.calcular_factorial(5)}")


class ClaseB:
    def ejecutar(self):
        calc = FactorialCalculator()
        print(f"ClaseB - 7! = {calc.calcular_factorial(7)}")


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":
    ClaseA().ejecutar()
    ClaseB().ejecutar()

    instancia1 = FactorialCalculator()
    instancia2 = FactorialCalculator()

    print(f"¿Misma instancia? {instancia1 is instancia2}")
    print(f"0! = {instancia1.calcular_factorial(0)}")
    print(f"10! = {instancia1.calcular_factorial(10)}")