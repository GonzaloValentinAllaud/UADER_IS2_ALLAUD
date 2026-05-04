# PUNTO 4:
#  Implemente una clase que permita a un número cualquiera imprimir su valor, 
# luego agregarle sucesivamente. 

# a. Sumarle 2. 
# b. Multiplicarle por 2. 
# c. Dividirlo por 3. 

# Mostrar los resultados de la clase sin agregados y con la invocación anidada a 
# las clases con las diferentes operaciones. Use un patrón decorator para 
# implementar.

"""
Estructura:
Componente base: Numero
    - imprime su valor

Decoradores (se apilan en cualquier orden):
    - SumarDos      : agrega 2 al valor
    - MultiplicarDos: multiplica el valor por 2
    - DividirTres   : divide el valor por 3

El patrón Decorator envuelve (wrapper) el objeto base y cada
decorador llama al anterior via super(), formando una cadena
recursiva de transformaciones.
"""

from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════
#  COMPONENT — Interface base
# ══════════════════════════════════════════════════════════════════

class ComponenteNumero(ABC):
    """
    Interface común para el componente base y todos los decoradores.
    Define la única operación: obtener el valor procesado.
    """

    @abstractmethod
    def valor(self) -> float:
        """Retorna el valor numérico (posiblemente transformado)."""
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """Retorna una descripción de las operaciones acumuladas."""
        pass

    def imprimir(self) -> None:
        """Imprime el valor y la descripción de cómo se obtuvo."""
        print(f"  Operación : {self.descripcion()}")
        print(f"  Resultado : {self.valor()}")


# ══════════════════════════════════════════════════════════════════
#  CONCRETE COMPONENT — Número base (sin decoradores)
# ══════════════════════════════════════════════════════════════════

class Numero(ComponenteNumero):
    """
    Componente concreto base.
    Almacena el valor original y lo entrega sin modificaciones.
    """

    def __init__(self, valor_inicial: float):
        self._valor = valor_inicial

    def valor(self) -> float:
        return self._valor

    def descripcion(self) -> str:
        return f"{self._valor}"


# ══════════════════════════════════════════════════════════════════
#  BASE DECORATOR — Wrapper abstracto
# ══════════════════════════════════════════════════════════════════

class DecoradorNumero(ComponenteNumero):
    """
    Decorador base (wrapper abstracto).
    Mantiene la referencia al componente envuelto y delega
    las llamadas a él antes de aplicar su propia transformación.
    """

    def __init__(self, componente: ComponenteNumero):
        self._componente = componente   # referencia al objeto envuelto

    def valor(self) -> float:
        # Por defecto delega al componente interior
        return self._componente.valor()

    def descripcion(self) -> str:
        return self._componente.descripcion()


# ══════════════════════════════════════════════════════════════════
#  CONCRETE DECORATORS — Operaciones concretas
# ══════════════════════════════════════════════════════════════════

class SumarDos(DecoradorNumero):
    """Decorador que suma 2 al valor del componente envuelto."""

    def valor(self) -> float:
        return self._componente.valor() + 2

    def descripcion(self) -> str:
        return f"({self._componente.descripcion()} + 2)"


class MultiplicarDos(DecoradorNumero):
    """Decorador que multiplica por 2 el valor del componente envuelto."""

    def valor(self) -> float:
        return self._componente.valor() * 2

    def descripcion(self) -> str:
        return f"({self._componente.descripcion()} × 2)"


class DividirTres(DecoradorNumero):
    """Decorador que divide por 3 el valor del componente envuelto."""

    def valor(self) -> float:
        return self._componente.valor() / 3

    def descripcion(self) -> str:
        return f"({self._componente.descripcion()} ÷ 3)"


# ══════════════════════════════════════════════════════════════════
#  Demostración
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    VALOR_INICIAL = 6   # número de ejemplo

    print("=" * 58)
    print("  DEMO - Patrón Decorator: Operaciones Numéricas")
    print(f"  Valor inicial: {VALOR_INICIAL}")
    print("=" * 58)

    # ── Sin decoradores ───────────────────────────────────────────
    print("\n▶ Sin decoradores (valor base):")
    n = Numero(VALOR_INICIAL)
    n.imprimir()

    # ── Solo Sumar 2 ──────────────────────────────────────────────
    print("\n▶ Con SumarDos:")
    n_sum = SumarDos(Numero(VALOR_INICIAL))
    n_sum.imprimir()

    # ── Sumar 2 → Multiplicar por 2 ──────────────────────────────
    print("\n▶ Con SumarDos + MultiplicarDos:")
    n_sum_mul = MultiplicarDos(SumarDos(Numero(VALOR_INICIAL)))
    n_sum_mul.imprimir()

    # ── Sumar 2 → Multiplicar por 2 → Dividir por 3 ──────────────
    print("\n▶ Con SumarDos + MultiplicarDos + DividirTres (anidado completo):")
    n_completo = DividirTres(MultiplicarDos(SumarDos(Numero(VALOR_INICIAL))))
    n_completo.imprimir()

    # ── Variante: distinto orden de decoradores ───────────────────
    print("\n" + "─" * 58)
    print("▶ Variante — distinto orden (el orden tiene semántica):")

    print("\n  Primero ×2, luego +2, luego ÷3:")
    variante = DividirTres(SumarDos(MultiplicarDos(Numero(VALOR_INICIAL))))
    variante.imprimir()

    print("\n  Solo DividirTres directamente:")
    solo_div = DividirTres(Numero(VALOR_INICIAL))
    solo_div.imprimir()

    print("\n" + "=" * 58)
    print("  Cada decorador envuelve al anterior y agrega su")
    print("  comportamiento sin modificar las clases existentes. ✓")
    print("=" * 58)