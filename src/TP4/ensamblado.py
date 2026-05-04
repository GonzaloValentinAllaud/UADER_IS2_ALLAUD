# PUNTO 3:
# Represente la lista de piezas componentes de un ensamblado con sus 
# relaciones jerárquicas. Empiece con un producto principal formado por tres 
# sub-conjuntos los que a su vez tendrán cuatro piezas cada uno. Genere clases 
# que representen esa configuración y la muestren. Luego agregue un sub
# conjunto opcional adicional también formado por cuatro piezas. (Use el patrón 
# composite).

"""
Estructura inicial:
  Producto Principal
  ├── SubConjunto A
  │   ├── Pieza A1
  │   ├── Pieza A2
  │   ├── Pieza A3
  │   └── Pieza A4
  ├── SubConjunto B
  │   ├── Pieza B1
  │   ├── Pieza B2
  │   ├── Pieza B3
  │   └── Pieza B4
  └── SubConjunto C
      ├── Pieza C1
      ├── Pieza C2
      ├── Pieza C3
      └── Pieza C4

Luego se agrega opcionalmente:
  └── SubConjunto D
      ├── Pieza D1
      ├── Pieza D2
      ├── Pieza D3
      └── Pieza D4

Jerarquía Composite:
  Component  (interface abstracta)
  ├── Pieza      (Leaf)
  └── Conjunto   (Composite — puede contener otros Component)
"""

from abc import ABC, abstractmethod
from typing import List


# ══════════════════════════════════════════════════════════════════
#  COMPONENT — Interface común para Leaf y Composite
# ══════════════════════════════════════════════════════════════════

class Componente(ABC):
    """
    Interface común (Component).
    Tanto las piezas individuales como los conjuntos la implementan,
    lo que permite tratar ambos de forma uniforme.
    """

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._padre: "Componente | None" = None

    @property
    def nombre(self) -> str:
        return self._nombre

    def set_padre(self, padre: "Componente") -> None:
        self._padre = padre

    # Operaciones de gestión de hijos (solo útiles en Composite)
    def agregar(self, componente: "Componente") -> None:
        pass

    def remover(self, componente: "Componente") -> None:
        pass

    def es_hoja(self) -> bool:
        return True

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> None:
        """Muestra el componente con indentación según su nivel en el árbol."""
        pass

    @abstractmethod
    def contar_piezas(self) -> int:
        """Cuenta recursivamente todas las piezas hoja contenidas."""
        pass


# ══════════════════════════════════════════════════════════════════
#  LEAF — Pieza individual (nodo hoja)
# ══════════════════════════════════════════════════════════════════

class Pieza(Componente):
    """
    Leaf: representa una pieza individual del ensamblado.
    No puede contener otros componentes.
    """

    def __init__(self, nombre: str, codigo: str = ""):
        super().__init__(nombre)
        self._codigo = codigo

    def es_hoja(self) -> bool:
        return True

    def mostrar(self, nivel: int = 0) -> None:
        prefijo = "    " * nivel + "└── "
        cod = f" [{self._codigo}]" if self._codigo else ""
        print(f"{prefijo}🔩 {self._nombre}{cod}")

    def contar_piezas(self) -> int:
        return 1


# ══════════════════════════════════════════════════════════════════
#  COMPOSITE — Conjunto (puede contener Piezas u otros Conjuntos)
# ══════════════════════════════════════════════════════════════════

class Conjunto(Componente):
    """
    Composite: representa un sub-conjunto o el producto principal.
    Puede contener Piezas u otros Conjuntos (recursividad).
    """

    def __init__(self, nombre: str):
        super().__init__(nombre)
        self._hijos: List[Componente] = []

    def es_hoja(self) -> bool:
        return False

    def agregar(self, componente: Componente) -> None:
        self._hijos.append(componente)
        componente.set_padre(self)

    def remover(self, componente: Componente) -> None:
        self._hijos.remove(componente)
        componente.set_padre(None)

    def mostrar(self, nivel: int = 0) -> None:
        prefijo = "    " * nivel + ("" if nivel == 0 else "└── ")
        icono = "📦" if nivel == 0 else "🗂️ "
        print(f"{prefijo}{icono} {self._nombre}  ({len(self._hijos)} componentes directos)")
        for hijo in self._hijos:
            hijo.mostrar(nivel + 1)

    def contar_piezas(self) -> int:
        """Cuenta recursivamente todas las piezas hoja del subárbol."""
        return sum(h.contar_piezas() for h in self._hijos)


# ══════════════════════════════════════════════════════════════════
#  Función auxiliar para construir sub-conjuntos con N piezas
# ══════════════════════════════════════════════════════════════════

def crear_subconjunto(nombre: str, letra: str, n_piezas: int = 4) -> Conjunto:
    """Crea un Conjunto con n_piezas hojas nombradas automáticamente."""
    sc = Conjunto(nombre)
    for i in range(1, n_piezas + 1):
        sc.agregar(Pieza(f"Pieza {letra}{i}", codigo=f"{letra}{i:03d}"))
    return sc


# ══════════════════════════════════════════════════════════════════
#  Demostración
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 60)
    print("  DEMO - Patrón Composite: Ensamblado de Piezas")
    print("=" * 60)

    # ── Construcción inicial: producto + 3 sub-conjuntos x 4 piezas ──
    producto = Conjunto("Producto Principal")

    sc_a = crear_subconjunto("SubConjunto A", "A")
    sc_b = crear_subconjunto("SubConjunto B", "B")
    sc_c = crear_subconjunto("SubConjunto C", "C")

    producto.agregar(sc_a)
    producto.agregar(sc_b)
    producto.agregar(sc_c)

    print("\n▶ Estructura inicial (3 sub-conjuntos × 4 piezas):\n")
    producto.mostrar()
    print(f"\n  Total de piezas: {producto.contar_piezas()}")

    # ── Agregar sub-conjunto opcional D ──────────────────────────────
    print("\n" + "─" * 60)
    print("▶ Agregando SubConjunto D opcional (4 piezas más):\n")

    sc_d = crear_subconjunto("SubConjunto D (opcional)", "D")
    producto.agregar(sc_d)

    producto.mostrar()
    print(f"\n  Total de piezas: {producto.contar_piezas()}")

    # ── Demostrar remoción del sub-conjunto opcional ──────────────────
    print("\n" + "─" * 60)
    print("▶ Removiendo SubConjunto D (es opcional):\n")

    producto.remover(sc_d)
    producto.mostrar()
    print(f"\n  Total de piezas: {producto.contar_piezas()}")

    print("\n" + "=" * 60)
    print("  El cliente opera igual sobre Piezas y Conjuntos.")
    print("  contar_piezas() recorre el árbol sin conocer su")
    print("  estructura exacta — eso es el patrón Composite. ✓")
    print("=" * 60)