# PUNTO 1:
#     Cree una clase bajo el patrón cadena de responsabilidad donde los números del 
#     1 al 100 sean pasados a las clases subscriptas en secuencia, aquella que 
#     identifique la necesidad de consumir el número lo hará y caso contrario lo 
#     pasará al siguiente en la cadena. Implemente una clase que consuma números 
#     primos y otra números pares. Puede ocurrir que un número no sea consumido 
#     por ninguna clase en cuyo caso se marcará como no consumido. 

"""
Patrón de Diseño: Chain of Responsibility
==========================================
Ingeniería de Software II — Dr. Pedro E. Colla

Problema: pasar los números del 1 al 100 a través de una cadena de handlers.
  - PrimeHandler : consume números primos.
  - EvenHandler  : consume números pares (que no hayan sido consumidos antes).
  - Si ningún handler consume el número, se registra como "no consumido".
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


# ---------------------------------------------------------------------------
# Interfaz base
# ---------------------------------------------------------------------------

class Handler(ABC):
    """Handler abstracto de la cadena."""

    def __init__(self) -> None:
        self._next: Optional[Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        """Encadena el siguiente handler y lo retorna para permitir fluent API."""
        self._next = handler
        return handler

    def pass_to_next(self, number: int) -> bool:
        """Delega al siguiente handler; si no hay, el número no fue consumido."""
        if self._next:
            return self._next.handle(number)
        return False  # fin de cadena sin consumir

    @abstractmethod
    def handle(self, number: int) -> bool:
        """Devuelve True si el número fue consumido, False si se pasa."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...


# ---------------------------------------------------------------------------
# Handlers concretos
# ---------------------------------------------------------------------------

class PrimeHandler(Handler):
    """Consume números primos."""

    name = "PrimeHandler"

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def handle(self, number: int) -> bool:
        if self._is_prime(number):
            print(f"  [PrimeHandler] consumió {number:3d}  (primo)")
            return True
        return self.pass_to_next(number)


class EvenHandler(Handler):
    """Consume números pares."""

    name = "EvenHandler"

    def handle(self, number: int) -> bool:
        if number % 2 == 0:
            print(f"  [EvenHandler ] consumió {number:3d}  (par)")
            return True
        return self.pass_to_next(number)


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------

def main() -> None:
    # Construcción de la cadena: PrimeHandler → EvenHandler
    prime_handler = PrimeHandler()
    even_handler  = EvenHandler()
    prime_handler.set_next(even_handler)

    not_consumed: list[int] = []

    print("=" * 55)
    print("  Chain of Responsibility — números del 1 al 100")
    print("  Cadena: PrimeHandler → EvenHandler")
    print("=" * 55)

    for number in range(1, 101):
        consumed = prime_handler.handle(number)
        if not consumed:
            not_consumed.append(number)
            print(f"  [--- ninguno ---] {number:3d}  (no consumido)")

    # Resumen
    print("\n" + "=" * 55)
    print("RESUMEN")
    print("=" * 55)

    primes  = [n for n in range(1, 101) if PrimeHandler()._is_prime(n)]
    evens   = [n for n in range(1, 101) if n % 2 == 0 and n not in primes]

    print(f"  Primos consumidos por PrimeHandler : {len(primes):3d}")
    print(f"  Pares consumidos  por EvenHandler  : {len(evens):3d}")
    print(f"  No consumidos                       : {len(not_consumed):3d}  → {not_consumed}")
    print("=" * 55)


if __name__ == "__main__":
    main()