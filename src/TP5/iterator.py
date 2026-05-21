# PUNTO 2:
#     Implemente una clase bajo el patrón iterator que almacene una cadena de 
#     caracteres y permita recorrerla en sentido directo y reverso.

"""
Patrón Iterator - IS2 T2 C5
Colección: cadena de caracteres con recorrido directo y reverso.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Interfaces ────────────────────────────────────────────────────────────────

class Iterator(ABC):
    @abstractmethod
    def has_more(self) -> bool: ...

    @abstractmethod
    def get_next(self) -> str: ...

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if not self.has_more():
            raise StopIteration
        return self.get_next()


class IterableCollection(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Iterador directo (izquierda → derecha)."""
        ...

    @abstractmethod
    def create_reverse_iterator(self) -> Iterator:
        """Iterador reverso (derecha → izquierda)."""
        ...


# ── Iteradores concretos ───────────────────────────────────────────────────────

class ForwardIterator(Iterator):
    """Recorre la cadena de izquierda a derecha."""

    def __init__(self, collection: StringCollection) -> None:
        self._collection = collection
        self._position: int = 0

    def has_more(self) -> bool:
        return self._position < len(self._collection)

    def get_next(self) -> str:
        char = self._collection[self._position]
        self._position += 1
        return char


class ReverseIterator(Iterator):
    """Recorre la cadena de derecha a izquierda."""

    def __init__(self, collection: StringCollection) -> None:
        self._collection = collection
        self._position: int = len(collection) - 1

    def has_more(self) -> bool:
        return self._position >= 0

    def get_next(self) -> str:
        char = self._collection[self._position]
        self._position -= 1
        return char


# ── Colección concreta ─────────────────────────────────────────────────────────

class StringCollection(IterableCollection):
    """Almacena una cadena de caracteres y expone iteradores sobre ella."""

    def __init__(self, text: str = "") -> None:
        self._data: str = text

    # Acceso por índice (usado internamente por los iteradores)
    def __getitem__(self, index: int) -> str:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f'StringCollection("{self._data}")'

    # ── Métodos de la colección ──────────────────────────────────────────────

    def append(self, char: str) -> None:
        """Agrega un carácter al final de la cadena."""
        if len(char) != 1:
            raise ValueError("Solo se puede agregar un carácter a la vez.")
        self._data += char

    def get_text(self) -> str:
        return self._data

    # ── Fábrica de iteradores ────────────────────────────────────────────────

    def create_iterator(self) -> ForwardIterator:
        return ForwardIterator(self)

    def create_reverse_iterator(self) -> ReverseIterator:
        return ReverseIterator(self)


# ── Demo ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    coleccion = StringCollection("Hola Mundo")
    print(f"Colección: {coleccion}\n")

    # ── Recorrido directo ────────────────────────────────────────────────────
    print("=== Iterador Directo (forward) ===")
    it_fwd = coleccion.create_iterator()
    resultado_fwd = ""
    while it_fwd.has_more():
        c = it_fwd.get_next()
        resultado_fwd += c
        print(f"  get_next() → '{c}'")
    print(f"  Resultado: '{resultado_fwd}'\n")

    # ── Recorrido reverso ────────────────────────────────────────────────────
    print("=== Iterador Reverso ===")
    it_rev = coleccion.create_reverse_iterator()
    resultado_rev = ""
    while it_rev.has_more():
        c = it_rev.get_next()
        resultado_rev += c
        print(f"  get_next() → '{c}'")
    print(f"  Resultado: '{resultado_rev}'\n")

    # ── Uso con for (protocolo nativo de Python) ─────────────────────────────
    print("=== Uso con for nativo (forward) ===")
    print("  ", end="")
    for c in coleccion.create_iterator():
        print(c, end=" ")
    print()

    print("=== Uso con for nativo (reverso) ===")
    print("  ", end="")
    for c in coleccion.create_reverse_iterator():
        print(c, end=" ")
    print()

    # ── Agregar caracteres y volver a iterar ─────────────────────────────────
    print("\n=== Append + iteración ===")
    coleccion2 = StringCollection()
    for letra in "Python":
        coleccion2.append(letra)
    print(f"  Colección: {coleccion2}")
    print("  Forward : ", "".join(coleccion2.create_iterator()))
    print("  Reverso : ", "".join(coleccion2.create_reverse_iterator()))