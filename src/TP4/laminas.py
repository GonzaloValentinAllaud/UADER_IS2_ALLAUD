# PUNTO 2:
# Para un producto láminas de acero de 0.5” de espesor y 1,5 metros de ancho 
# dispone de dos trenes laminadores, uno que genera planchas de 5 mts y otro 
# de 10 mts. Genere una clase que represente a las láminas en forma genérica al 
# cual se le pueda indicar que a que tren laminador se enviará a producir. (Use el 
# patrón bridge en la solución). 

"""
Contexto:
Producto: láminas de acero de 0.5" de espesor y 1.5 m de ancho.
Dos trenes laminadores disponibles:
    - TrenLaminador5m  : genera planchas de 5 metros de largo
    - TrenLaminador10m : genera planchas de 10 metros de largo

El patrón Bridge separa la abstracción (Lamina) de la implementación
(TrenLaminador), permitiendo combinarlas independientemente.

Jerarquía:
Implementación (interface):  TrenLaminador
    └─ TrenLaminador5m
    └─ TrenLaminador10m

Abstracción:                 Lamina
    └─ LaminaAcero             (refinement concreto)
"""

from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════
#  LADO IMPLEMENTACIÓN — Trenes laminadores
# ══════════════════════════════════════════════════════════════════

class TrenLaminador(ABC):
    """
    Interface de implementación (lado derecho del Bridge).
    Define la operación que cualquier tren laminador debe proveer.
    """

    @abstractmethod
    def producir(self, espesor_pulg: float, ancho_m: float) -> None:
        """Produce una plancha con las dimensiones indicadas."""
        pass

    @abstractmethod
    def largo_plancha_m(self) -> float:
        """Retorna el largo de plancha que produce este tren."""
        pass


class TrenLaminador5m(TrenLaminador):
    """Implementación concreta: tren que genera planchas de 5 metros."""

    def largo_plancha_m(self) -> float:
        return 5.0

    def producir(self, espesor_pulg: float, ancho_m: float) -> None:
        print(f"  [TrenLaminador5m]  Produciendo plancha de acero:")
        print(f"    Espesor : {espesor_pulg}\"  ({espesor_pulg * 25.4:.1f} mm)")
        print(f"    Ancho   : {ancho_m} m")
        print(f"    Largo   : {self.largo_plancha_m()} m")
        print(f"    → Plancha lista en tren de 5 m ✓")


class TrenLaminador10m(TrenLaminador):
    """Implementación concreta: tren que genera planchas de 10 metros."""

    def largo_plancha_m(self) -> float:
        return 10.0

    def producir(self, espesor_pulg: float, ancho_m: float) -> None:
        print(f"  [TrenLaminador10m] Produciendo plancha de acero:")
        print(f"    Espesor : {espesor_pulg}\"  ({espesor_pulg * 25.4:.1f} mm)")
        print(f"    Ancho   : {ancho_m} m")
        print(f"    Largo   : {self.largo_plancha_m()} m")
        print(f"    → Plancha lista en tren de 10 m ✓")


# ══════════════════════════════════════════════════════════════════
#  LADO ABSTRACCIÓN — Lámina genérica
# ══════════════════════════════════════════════════════════════════

class Lamina(ABC):
    """
    Abstracción base (lado izquierdo del Bridge).
    Mantiene una referencia a la implementación (TrenLaminador)
    y delega la producción en ella.
    
    El tren puede asignarse en construcción o cambiarse en runtime
    con set_tren(), cumpliendo el propósito del patrón Bridge.
    """

    def __init__(self, tren: TrenLaminador):
        self._tren = tren          # referencia a la implementación

    def set_tren(self, tren: TrenLaminador) -> None:
        """Permite cambiar el tren laminador en tiempo de ejecución."""
        self._tren = tren
        print(f"  [Lamina] Tren cambiado a: {type(tren).__name__}")

    @abstractmethod
    def enviar_a_producir(self) -> None:
        """Envía la lámina al tren asignado para su producción."""
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """Descripción del producto."""
        pass


class LaminaAcero(Lamina):
    """
    Abstracción refinada: lámina de acero con especificaciones fijas.
    Espesor: 0.5" — Ancho: 1.5 m
    """

    ESPESOR_PULG = 0.5
    ANCHO_M      = 1.5

    def __init__(self, tren: TrenLaminador):
        super().__init__(tren)

    def descripcion(self) -> str:
        return (f"Lámina de acero | "
                f"Espesor: {self.ESPESOR_PULG}\" | "
                f"Ancho: {self.ANCHO_M} m")

    def enviar_a_producir(self) -> None:
        """
        Delega la producción al tren laminador asignado
        (el 'puente' entre abstracción e implementación).
        """
        print(f"\n[LaminaAcero] {self.descripcion()}")
        print(f"[LaminaAcero] Enviando a → {type(self._tren).__name__}")
        self._tren.producir(self.ESPESOR_PULG, self.ANCHO_M)


# ══════════════════════════════════════════════════════════════════
#  Demostración
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 58)
    print("  DEMO - Patrón Bridge: Láminas de Acero + Trenes")
    print("=" * 58)

    # Instanciar los dos trenes laminadores
    tren_5m  = TrenLaminador5m()
    tren_10m = TrenLaminador10m()

    # ── Caso 1: lámina enviada al tren de 5 m ──────────────────
    print("\n▶ Caso 1: Producir en tren de 5 m")
    lamina = LaminaAcero(tren=tren_5m)
    lamina.enviar_a_producir()

    # ── Caso 2: misma lámina, ahora al tren de 10 m ────────────
    print("\n▶ Caso 2: Producir en tren de 10 m")
    lamina2 = LaminaAcero(tren=tren_10m)
    lamina2.enviar_a_producir()

    # ── Caso 3: cambio de tren en runtime (Bridge lo permite) ──
    print("\n▶ Caso 3: Cambiar tren en runtime (sin modificar LaminaAcero)")
    lamina.set_tren(tren_10m)
    lamina.enviar_a_producir()

    print("\n" + "=" * 58)
    print("  Abstracción (LaminaAcero) e implementaciones")
    print("  (TrenLaminador5m / TrenLaminador10m) son")
    print("  completamente independientes entre sí. ✓")
    print("=" * 58)