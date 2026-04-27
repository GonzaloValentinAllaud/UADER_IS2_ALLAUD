# PUNTO 6:
# Dado una clase que implemente el patrón “prototipo” verifique que una clase 
# generada a partir de ella permite por su parte obtener también copias de si 
# misma.

import copy

# ─── Clase base Prototype ────────────────────────────────────────────

class Prototype:
    """
    Clase base que implementa el patrón Prototype.
    Cualquier subclase que herede de ella tendrá la capacidad
    de clonarse a sí misma mediante el método clonar().
    """

    def clonar(self):
        """
        Retorna una copia profunda (deep copy) de la instancia actual.
        La copia es independiente del original: modificar el clon
        no afecta al objeto original.
        """
        return copy.deepcopy(self)


# ─── Clase concreta que hereda de Prototype ──────────────────────────

class Producto(Prototype):
    """
    Clase concreta que representa un producto.
    Al heredar de Prototype, puede clonarse a sí misma
    y sus clones también pueden generar nuevas copias.
    """

    def __init__(self, nombre: str, precio: float, categoria: str):
        self.nombre    = nombre
        self.precio    = precio
        self.categoria = categoria

    def mostrar(self, etiqueta: str = "Producto"):
        """Muestra los datos del producto por pantalla."""
        print(f"\n{'─'*40}")
        print(f"  {etiqueta}")
        print(f"{'─'*40}")
        print(f"  Nombre:    {self.nombre}")
        print(f"  Precio:    $ {self.precio:.2f}")
        print(f"  Categoría: {self.categoria}")
        print(f"  ID objeto: {id(self)}")
        print(f"{'─'*40}")


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # ── Paso 1: Creamos el objeto original ──
    print("╔══════════════════════════════════════════════╗")
    print("║            OBJETO ORIGINAL                   ║")
    print("╚══════════════════════════════════════════════╝")
    original = Producto("Laptop", 1500.00, "Electrónica")
    original.mostrar("Original")

    # ── Paso 2: Clonamos el original ──
    print("\n╔══════════════════════════════════════════════╗")
    print("║         CLON GENERADO DESDE EL ORIGINAL      ║")
    print("╚══════════════════════════════════════════════╝")
    clon1 = original.clonar()

    # Modificamos el clon para demostrar que es independiente del original
    clon1.nombre = "Laptop Gamer"
    clon1.precio = 2200.00
    clon1.mostrar("Clon 1 (modificado)")

    # Verificamos que el original no fue afectado por los cambios del clon
    print("\n  ¿El original fue modificado por el clon?")
    original.mostrar("Original (sin cambios)")

    # ── Paso 3: Verificamos que el clon también puede clonar ──
    print("\n╔══════════════════════════════════════════════╗")
    print("║      CLON GENERADO DESDE EL CLON 1           ║")
    print("╚══════════════════════════════════════════════╝")

    # El clon genera su propia copia, demostrando que la capacidad se hereda
    clon2 = clon1.clonar()
    clon2.nombre = "Laptop Gamer Pro"
    clon2.precio = 3100.00
    clon2.mostrar("Clon 2 (clon del clon, modificado)")

    # Verificamos que el clon1 tampoco fue afectado
    print("\n  ¿El clon 1 fue modificado por el clon 2?")
    clon1.mostrar("Clon 1 (sin cambios)")

    # ── Paso 4: Verificamos que todos son objetos distintos en memoria ──
    print("\n╔══════════════════════════════════════════════╗")
    print("║         VERIFICACIÓN DE IDENTIDAD            ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\n  ¿original es clon1?  {original is clon1}")  # False
    print(f"  ¿clon1 es clon2?     {clon1 is clon2}")      # False
    print(f"  ¿original es clon2?  {original is clon2}")   # False
    print(f"\n  Todos son objetos independientes en memoria ✓")