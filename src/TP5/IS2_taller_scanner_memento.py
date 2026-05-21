# PUNTO 4:
#  	Modifique el programa IS2_taller_scanner.py para que además la secuencia de 
# 	barrido de radios que tiene incluya la sintonía de una serie de frecuencias 
# 	memorizadas tanto de AM como de FM. Las frecuencias estarán etiquetadas 
# 	como M1, M2, M3 y M4. Cada memoria podrá corresponder a una radio de AM 
# 	o de FM en sus respectivas frecuencias específicas. En cada ciclo de barrido se 
# 	barrerán las cuatro memorias.

import os

#*--------------------------------------------------------------------
#* Ejemplo de design pattern de tipo State + Memento
#* Extensión: memorias M1-M4 con frecuencias AM/FM predefinidas
#*--------------------------------------------------------------------

# ═══════════════════════════════════════════════════════════════════
#  MEMENTO  — guarda el estado de una memoria (banda + frecuencia)
# ═══════════════════════════════════════════════════════════════════

class PresetMemento:
    """Almacena una frecuencia memorizada (banda + frecuencia)."""

    def __init__(self, label: str, band: str, frequency: str):
        self._label     = label      # "M1" … "M4"
        self._band      = band       # "AM" | "FM"
        self._frequency = frequency  # ej. "1250" o "89.1"

    @property
    def label(self) -> str:
        return self._label

    @property
    def band(self) -> str:
        return self._band

    @property
    def frequency(self) -> str:
        return self._frequency

    def __str__(self) -> str:
        return f"{self._label}: {self._band} {self._frequency}"


# ═══════════════════════════════════════════════════════════════════
#  CARETAKER  — administra las cuatro memorias (M1-M4)
# ═══════════════════════════════════════════════════════════════════

class PresetCaretaker:
    """Gestiona hasta 4 memorias de radio (M1-M4)."""

    LABELS = ["M1", "M2", "M3", "M4"]

    def __init__(self):
        # Inicializa cuatro memorias vacías
        self._presets: dict[str, PresetMemento | None] = {
            lbl: None for lbl in self.LABELS
        }

    def save(self, label: str, band: str, frequency: str) -> None:
        """Guarda (o sobreescribe) una memoria."""
        if label not in self.LABELS:
            raise ValueError(f"Etiqueta inválida '{label}'. Use: {self.LABELS}")
        self._presets[label] = PresetMemento(label, band, frequency)
        print(f"  [Memoria] {label} guardada → {band} {frequency}")

    def get(self, label: str) -> PresetMemento | None:
        return self._presets.get(label)

    def all_presets(self) -> list[PresetMemento]:
        """Devuelve la lista de memorias definidas (no vacías), en orden."""
        return [p for p in self._presets.values() if p is not None]

    def __str__(self) -> str:
        lines = ["Memorias:"]
        for lbl, p in self._presets.items():
            lines.append(f"  {p if p else lbl + ': (vacía)'}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
#  STATE — base
# ═══════════════════════════════════════════════════════════════════

class State:
    """Clase base de estado: implementa el barrido secuencial."""

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print(f"  Sintonizando... Estación {self.stations[self.pos]} {self.name}")


# ═══════════════════════════════════════════════════════════════════
#  STATES concretos
# ═══════════════════════════════════════════════════════════════════

class AmState(State):

    def __init__(self, radio):
        self.radio    = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos      = 0
        self.name     = "AM"

    def toggle_amfm(self):
        print("  Cambiando a FM")
        self.radio.state = self.radio.fmstate


class FmState(State):

    def __init__(self, radio):
        self.radio    = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos      = 0
        self.name     = "FM"

    def toggle_amfm(self):
        print("  Cambiando a AM")
        self.radio.state = self.radio.amstate


# ═══════════════════════════════════════════════════════════════════
#  RADIO  — Publisher + Context
# ═══════════════════════════════════════════════════════════════════

class Radio:

    def __init__(self, caretaker: PresetCaretaker):
        self.fmstate   = FmState(self)
        self.amstate   = AmState(self)
        self.state     = self.fmstate          # inicia en FM
        self.caretaker = caretaker

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

    def scan_presets(self):
        """Recorre las cuatro memorias M1-M4 y sintoniza cada una."""
        presets = self.caretaker.all_presets()
        if not presets:
            print("  [Memorias] No hay memorias guardadas.")
            return

        print("  ── Barrido de memorias ──")
        for preset in presets:
            # Cambia al estado correspondiente a la banda de la memoria
            if preset.band == "AM":
                self.state = self.amstate
            else:
                self.state = self.fmstate
            print(f"  Sintonizando memoria {preset.label} → "
                  f"{preset.band} {preset.frequency}")

        # Restaura el estado al que estaba antes del barrido de memorias
        # (queda en la banda de la última memoria; se puede ajustar si se desea)
        print("  ── Fin barrido memorias ──")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.system("clear")

    # --- Configurar memorias M1-M4 ---------------------------------------
    print("╔══════════════════════════════════════════════╗")
    print("║         Configurando memorias M1-M4         ║")
    print("╚══════════════════════════════════════════════╝")

    caretaker = PresetCaretaker()
    caretaker.save("M1", "FM",  "89.1")    # FM
    caretaker.save("M2", "AM", "1250")     # AM
    caretaker.save("M3", "FM", "103.9")    # FM
    caretaker.save("M4", "AM", "1380")     # AM

    print(f"\n{caretaker}\n")

    # --- Crear radio y secuencia de acciones -----------------------------
    radio = Radio(caretaker)

    print("╔══════════════════════════════════════════════╗")
    print("║     Secuencia de acciones (2 ciclos)        ║")
    print("╚══════════════════════════════════════════════╝")
    print("Secuencia por ciclo:")
    print("  scan x3  →  toggle AM/FM  →  scan x3  →  scan_presets\n")

    # Secuencia original + barrido de memorias al final de cada ciclo
    actions = (
        [radio.scan] * 3 +
        [radio.toggle_amfm] +
        [radio.scan] * 3 +
        [radio.scan_presets]
    ) * 2

    for i, action in enumerate(actions, 1):
        # Separador visual al inicio de cada ciclo
        if action == radio.scan and i == 1:
            print(f"┌─── Ciclo 1 ───────────────────────────────┐")
        if action == radio.scan_presets and i == len(actions) // 2 + 1:
            print(f"\n┌─── Ciclo 2 ───────────────────────────────┐")
        action()