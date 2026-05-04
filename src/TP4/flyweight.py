# PUNTO 5:
# Imagine una situación donde pueda ser de utilidad el patrón “flyweight”. 

# Escenario elegido: un sistema de renderizado de texto donde cada carácter tiene propiedades compartidas (fuente, tamaño, color) que se repiten
# miles de veces, y solo la posición es única por instancia.

"""
══════════════════════════════════════════════════════════════════
SITUACIÓN IMAGINADA
══════════════════════════════════════════════════════════════════

Un editor de texto necesita renderizar documentos con miles de
caracteres en pantalla. Cada carácter tiene:

  Estado INTRÍNSECO (compartido, no cambia entre instancias):
    - símbolo     : el carácter en sí ('A', 'b', '1', etc.)
    - fuente      : nombre de la tipografía ('Arial', 'Times', ...)
    - tamaño      : tamaño en puntos (10, 12, 14, ...)
    - color       : color del texto ('#000000', '#FF0000', ...)

  Estado EXTRÍNSECO (único por ocurrencia, lo pasa el cliente):
    - posicion_x  : columna en pantalla
    - posicion_y  : fila en pantalla

SIN Flyweight: si un documento tiene 50.000 caracteres, se crean
50.000 objetos completos, cada uno guardando fuente+tamaño+color
aunque sean idénticos en el 95% de los casos.

CON Flyweight: solo se crean objetos únicos por combinación
(símbolo, fuente, tamaño, color). Si el documento usa solo
80 caracteres distintos con 2 estilos, habrá a lo sumo 160
objetos Flyweight en memoria, sin importar cuántas veces aparezcan.

Jerarquía:
  CaracterFlyweight         — objeto compartido (estado intrínseco)
  CaracterFlyweightFactory  — caché / fábrica de flyweights
  Editor                    — cliente que gestiona el estado extrínseco
══════════════════════════════════════════════════════════════════
"""

import sys
from typing import Dict, Tuple


# ══════════════════════════════════════════════════════════════════
#  FLYWEIGHT — Objeto compartido con estado intrínseco
# ══════════════════════════════════════════════════════════════════

class CaracterFlyweight:
    """
    Flyweight concreto.
    Almacena SOLO el estado intrínseco (compartido entre ocurrencias).
    El estado extrínseco (posición) se pasa en cada llamada a render().
    """

    def __init__(self, simbolo: str, fuente: str,
                 tamanio: int, color: str):
        # Estado intrínseco — inmutable, compartido
        self._simbolo  = simbolo
        self._fuente   = fuente
        self._tamanio  = tamanio
        self._color    = color

    def render(self, pos_x: int, pos_y: int) -> None:
        """
        Renderiza el carácter usando su estado intrínseco más
        el estado extrínseco recibido como parámetro.
        """
        print(f"  Render '{self._simbolo}' | "
              f"fuente={self._fuente} | "
              f"tam={self._tamanio}pt | "
              f"color={self._color} | "
              f"pos=({pos_x},{pos_y})")

    @property
    def clave(self) -> str:
        return f"{self._simbolo}|{self._fuente}|{self._tamanio}|{self._color}"

    def __repr__(self) -> str:
        return (f"CaracterFlyweight('{self._simbolo}', "
                f"{self._fuente}, {self._tamanio}pt, {self._color})")


# ══════════════════════════════════════════════════════════════════
#  FLYWEIGHT FACTORY — Caché de flyweights
# ══════════════════════════════════════════════════════════════════

class CaracterFlyweightFactory:
    """
    Fábrica y caché de objetos Flyweight.
    Garantiza que solo exista UNA instancia por combinación única
    de (símbolo, fuente, tamaño, color).
    Si el flyweight ya existe lo retorna; si no, lo crea y lo guarda.
    """

    def __init__(self):
        self._cache: Dict[str, CaracterFlyweight] = {}

    def get(self, simbolo: str, fuente: str,
            tamanio: int, color: str) -> CaracterFlyweight:
        clave = f"{simbolo}|{fuente}|{tamanio}|{color}"
        if clave not in self._cache:
            self._cache[clave] = CaracterFlyweight(
                simbolo, fuente, tamanio, color
            )
            print(f"  [Factory] Nuevo flyweight creado → {clave}")
        return self._cache[clave]

    def total_flyweights(self) -> int:
        return len(self._cache)

    def listar_cache(self) -> None:
        print(f"\n  Cache actual ({self.total_flyweights()} flyweights únicos):")
        for clave, fw in self._cache.items():
            print(f"    • {clave}  →  id={id(fw)}")


# ══════════════════════════════════════════════════════════════════
#  CLIENTE — Editor de texto (gestiona estado extrínseco)
# ══════════════════════════════════════════════════════════════════

class Editor:
    """
    Cliente del patrón Flyweight.
    Mantiene la lista de caracteres del documento como tuplas
    (flyweight, pos_x, pos_y), donde el estado extrínseco
    (posición) vive aquí, NO dentro del flyweight.
    """

    def __init__(self, factory: CaracterFlyweightFactory):
        self._factory = factory
        # Cada elemento: (flyweight, pos_x, pos_y)
        self._caracteres: list[Tuple[CaracterFlyweight, int, int]] = []

    def agregar_caracter(self, simbolo: str, fuente: str,
                         tamanio: int, color: str,
                         pos_x: int, pos_y: int) -> None:
        """Agrega un carácter al documento usando el flyweight correspondiente."""
        fw = self._factory.get(simbolo, fuente, tamanio, color)
        self._caracteres.append((fw, pos_x, pos_y))

    def renderizar(self) -> None:
        """Renderiza todos los caracteres del documento."""
        print(f"\n  Renderizando {len(self._caracteres)} caracteres...")
        for fw, x, y in self._caracteres:
            fw.render(x, y)

    def total_caracteres(self) -> int:
        return len(self._caracteres)


# ══════════════════════════════════════════════════════════════════
#  Demostración
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 62)
    print("  DEMO - Patrón Flyweight: Editor de Texto")
    print("=" * 62)
    print("""
  Situación: un editor renderiza un documento con muchos
  caracteres. La mayoría comparte fuente, tamaño y color.
  Solo la posición varía por ocurrencia.
""")

    factory = CaracterFlyweightFactory()
    editor  = Editor(factory)

    # ── Simular texto: "Hola Mundo" en estilo normal (Arial 12 negro)
    print("▶ Agregando texto 'Hola Mundo' en Arial 12 negro:\n")
    texto_normal = [
        ('H', 0, 0), ('o', 1, 0), ('l', 2, 0), ('a', 3, 0),
        (' ', 4, 0),
        ('M', 5, 0), ('u', 6, 0), ('n', 7, 0), ('d', 8, 0), ('o', 9, 0),
    ]
    for sim, x, y in texto_normal:
        editor.agregar_caracter(sim, "Arial", 12, "#000000", x, y)

    # ── Mismas letras pero en negrita roja (distinto estilo)
    print("\n▶ Agregando 'Hola' en Arial 14 rojo (énfasis):\n")
    texto_enfasis = [
        ('H', 0, 1), ('o', 1, 1), ('l', 2, 1), ('a', 3, 1),
    ]
    for sim, x, y in texto_enfasis:
        editor.agregar_caracter(sim, "Arial", 14, "#FF0000", x, y)

    # ── Mostrar el caché de flyweights creados
    factory.listar_cache()

    # ── Renderizar el documento completo
    print("\n▶ Renderizado completo del documento:")
    editor.renderizar()

    # ── Comparación de memoria
    print("\n" + "─" * 62)
    print("▶ Análisis de memoria (estimación):\n")

    total_chars   = editor.total_caracteres()
    total_fw      = factory.total_flyweights()
    tam_fw        = sys.getsizeof(list(factory._cache.values())[0])
    tam_sin_fw    = tam_fw * total_chars
    tam_con_fw    = tam_fw * total_fw

    print(f"  Caracteres en el documento : {total_chars}")
    print(f"  Flyweights únicos en cache : {total_fw}")
    print(f"  Tamaño aprox. por objeto   : {tam_fw} bytes")
    print(f"  Sin Flyweight ({total_chars} objetos)  : ~{tam_sin_fw} bytes")
    print(f"  Con Flyweight ({total_fw} objetos)   : ~{tam_con_fw} bytes")
    reduccion = (1 - tam_con_fw / tam_sin_fw) * 100
    print(f"  Reducción de memoria       : ~{reduccion:.1f}%")

    print("\n" + "=" * 62)
    print("  Aunque el documento tiene 14 caracteres, solo se")
    print(f"  crearon {total_fw} objetos Flyweight únicos en memoria.")
    print("  En un documento real con miles de repeticiones,")
    print("  el ahorro sería proporcional y muy significativo. ✓")
    print("=" * 62)