# PUNTO 3:
#     Implemente una clase bajo el patrón observer donde una serie de clases están 
#     subscriptas, cada clase espera que su propio ID (una secuencia arbitraria de 4 
#     caracteres) sea expuesta y emitirá un mensaje cuando el ID emitido y el propio 
#     coinciden. Implemente 4 clases de tal manera que cada una tenga un ID 
#     especifico. Emita 8 ID asegurándose que al menos cuatro de ellos coincidan con 
#     ID para el que tenga una clase implementada. 

"""
Patrón Observer - IS2 T2 C5
Publisher emite IDs de 4 caracteres; cada Subscriber reacciona
solo cuando el ID emitido coincide con el suyo propio.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


# ── Interfaces ────────────────────────────────────────────────────────────────

class EventListener(ABC):
    """«interface» Subscriber / EventListener."""

    @abstractmethod
    def update(self, emitted_id: str) -> None: ...


class EventManager:
    """Gestiona la lista de suscriptores y despacha notificaciones."""

    def __init__(self) -> None:
        self._listeners: List[EventListener] = []

    def subscribe(self, listener: EventListener) -> None:
        self._listeners.append(listener)
        print(f"  [EventManager] suscrito: {listener}")

    def unsubscribe(self, listener: EventListener) -> None:
        self._listeners.remove(listener)
        print(f"  [EventManager] desuscrito: {listener}")

    def notify(self, emitted_id: str) -> None:
        for listener in self._listeners:
            listener.update(emitted_id)


# ── Publisher ─────────────────────────────────────────────────────────────────

class IDPublisher:
    """
    Publisher que emite IDs de 4 caracteres.
    Delega la gestión de suscriptores al EventManager.
    """

    def __init__(self) -> None:
        self.events = EventManager()

    def emit(self, id_code: str) -> None:
        if len(id_code) != 4:
            raise ValueError(f"El ID debe tener exactamente 4 caracteres (recibido: '{id_code}').")
        print(f"\n>>> Publisher emite ID: '{id_code}'")
        self.events.notify(id_code)


# ── Subscribers concretos ─────────────────────────────────────────────────────

class IDSubscriber(EventListener):
    """
    Subscriber genérico: se activa únicamente cuando el ID emitido
    coincide con su propio ID de 4 caracteres.
    """

    def __init__(self, own_id: str, name: str) -> None:
        if len(own_id) != 4:
            raise ValueError(f"El ID del subscriber debe tener 4 caracteres (recibido: '{own_id}').")
        self._id   = own_id
        self._name = name
        self._hits = 0          # contador de coincidencias

    def update(self, emitted_id: str) -> None:
        if emitted_id == self._id:
            self._hits += 1
            print(f"  ✔  [{self._name}] ¡Coincidencia! Mi ID '{self._id}' fue emitido "
                  f"(hit #{self._hits})")
        else:
            print(f"  ·  [{self._name}] ID '{emitted_id}' recibido — no coincide con '{self._id}'")

    def __repr__(self) -> str:
        return f"{self._name}(id='{self._id}')"


# ── Clases especializadas (cada una con su ID fijo) ───────────────────────────

class SensorAlpha(IDSubscriber):
    def __init__(self) -> None:
        super().__init__("A1B2", "SensorAlpha")

class SensorBeta(IDSubscriber):
    def __init__(self) -> None:
        super().__init__("C3D4", "SensorBeta")

class SensorGamma(IDSubscriber):
    def __init__(self) -> None:
        super().__init__("E5F6", "SensorGamma")

class SensorDelta(IDSubscriber):
    def __init__(self) -> None:
        super().__init__("G7H8", "SensorDelta")


# ── Demo ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # --- Crear publisher y suscriptores --------------------------------------
    publisher = IDPublisher()

    alpha = SensorAlpha()   # ID: A1B2
    beta  = SensorBeta()    # ID: C3D4
    gamma = SensorGamma()   # ID: E5F6
    delta = SensorDelta()   # ID: G7H8

    print("=" * 55)
    print("  Suscribiendo clases al Publisher")
    print("=" * 55)
    publisher.events.subscribe(alpha)
    publisher.events.subscribe(beta)
    publisher.events.subscribe(gamma)
    publisher.events.subscribe(delta)

    # --- Emitir 8 IDs --------------------------------------------------------
    # 4 coincidentes (uno por suscriptor) + 4 que no coinciden con nadie
    ids_a_emitir = [
        "A1B2",   # ← coincide con SensorAlpha
        "ZZZZ",   # ← no coincide con nadie
        "C3D4",   # ← coincide con SensorBeta
        "0000",   # ← no coincide con nadie
        "E5F6",   # ← coincide con SensorGamma
        "XXXX",   # ← no coincide con nadie
        "G7H8",   # ← coincide con SensorDelta
        "9999",   # ← no coincide con nadie
    ]

    print("\n" + "=" * 55)
    print("  Emitiendo 8 IDs")
    print("=" * 55)
    for id_code in ids_a_emitir:
        publisher.emit(id_code)

    # --- Resumen -------------------------------------------------------------
    print("\n" + "=" * 55)
    print("  Resumen de hits por suscriptor")
    print("=" * 55)
    for sub in [alpha, beta, gamma, delta]:
        print(f"  {sub}  →  hits: {sub._hits}")