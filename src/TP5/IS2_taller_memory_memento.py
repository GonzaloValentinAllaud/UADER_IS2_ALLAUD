# PUNTO 5:
#     Modifique el programa IS2_taller_memory.py para que la clase tenga la 
# 	capacidad de almacenar hasta 4 estados en el pasado y pueda recuperar los 
# 	mismos en cualquier orden de ser necesario. El método undo deberá tener un 
# 	argumento adicional indicando si se desea recuperar el inmediato anterior (0) y 
# 	los anteriores a el (1,2,3). 

import os

#*--------------------------------------------------------------------
#* Design pattern: Memento
#* Modificación: FileWriterCaretaker almacena hasta 4 estados y
#* permite recuperar cualquiera de ellos mediante un índice.
#*   undo(writer, 0) -> estado más reciente guardado
#*   undo(writer, 1) -> el anterior a ese
#*   undo(writer, 2) -> dos pasos atrás
#*   undo(writer, 3) -> tres pasos atrás (el más antiguo posible)
#*--------------------------------------------------------------------

MAX_HISTORY = 4


class Memento:
    def __init__(self, file, content):
        self.file    = file
        self.content = content


class FileWriterUtility:

    def __init__(self, file):
        self.file    = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file    = memento.file
        self.content = memento.content


class FileWriterCaretaker:
    """
    Mantiene un historial de hasta MAX_HISTORY (4) estados.
    El más reciente queda en la posición 0 de la lista; el más
    antiguo en la posición -1.

    save(writer)        -> agrega un snapshot al historial.
    undo(writer, n)     -> restaura el estado n-ésimo hacia atrás
                           (0 = último guardado, 3 = más antiguo).
    history_summary()   -> imprime los estados almacenados.
    """

    def __init__(self):
        self._history: list[Memento] = []   # índice 0 = más reciente

    # ------------------------------------------------------------------
    def save(self, writer: FileWriterUtility) -> None:
        snapshot = writer.save()
        self._history.insert(0, snapshot)           # más reciente primero
        if len(self._history) > MAX_HISTORY:
            dropped = self._history.pop()           # descarta el más viejo
            print(f"  [Caretaker] historial lleno — se descartó el estado "
                  f"más antiguo ('{dropped.content[:30].strip()}...')")

    # ------------------------------------------------------------------
    def undo(self, writer: FileWriterUtility, n: int = 0) -> None:
        if not self._history:
            print("  [Caretaker] ERROR: no hay estados guardados.")
            return

        if n < 0 or n >= MAX_HISTORY:
            print(f"  [Caretaker] ERROR: índice {n} inválido. "
                  f"Debe estar entre 0 y {MAX_HISTORY - 1}.")
            return

        if n >= len(self._history):
            print(f"  [Caretaker] AVISO: solo hay {len(self._history)} "
                  f"estado(s) guardado(s). "
                  f"Se recupera el más antiguo disponible (índice "
                  f"{len(self._history) - 1}).")
            n = len(self._history) - 1

        writer.undo(self._history[n])
        print(f"  [Caretaker] undo({n}) aplicado — "
              f"estado recuperado: índice {n} de {len(self._history)} guardados.")

    # ------------------------------------------------------------------
    def history_summary(self) -> None:
        print(f"\n  [Historial — {len(self._history)}/{MAX_HISTORY} estados]")
        if not self._history:
            print("    (vacío)")
            return
        for i, m in enumerate(self._history):
            preview = m.content.replace('\n', '↵')[:50]
            print(f"    [{i}] {preview}")
        print()


# ======================================================================
# Programa principal
# ======================================================================
if __name__ == '__main__':

    os.system("clear")

    caretaker = FileWriterCaretaker()
    writer    = FileWriterUtility("GFG.txt")

    print("=" * 60)
    print("  Patrón Memento — historial de hasta 4 estados")
    print("=" * 60)

    # --- Estado 1 ---
    writer.write("Clase de IS2 en UADER\n")
    caretaker.save(writer)
    print(f"\n[Escritura 1] '{writer.content.strip()}'")
    caretaker.history_summary()

    # --- Estado 2 ---
    writer.write("Material adicional de la clase de patrones\n")
    caretaker.save(writer)
    print(f"[Escritura 2] '{writer.content.strip()}'")
    caretaker.history_summary()

    # --- Estado 3 ---
    writer.write("Material adicional de la clase de patrones II\n")
    caretaker.save(writer)
    print(f"[Escritura 3] '{writer.content.strip()}'")
    caretaker.history_summary()

    # --- Estado 4 ---
    writer.write("Cuarto bloque de contenido agregado\n")
    caretaker.save(writer)
    print(f"[Escritura 4] '{writer.content.strip()}'")
    caretaker.history_summary()

    # --- Estado 5 (desborda el límite de 4) ---
    writer.write("Quinto bloque — provoca descarte del estado más viejo\n")
    caretaker.save(writer)
    print(f"[Escritura 5] '{writer.content.strip()}'")
    caretaker.history_summary()

    # ------------------------------------------------------------------
    print("=" * 60)
    print("  Recuperaciones con undo(n)")
    print("=" * 60)

    # Recuperar el estado inmediato anterior (n=0)
    print("\nundo(0) → estado más reciente guardado:")
    caretaker.undo(writer, 0)
    print(f"  Contenido actual:\n{writer.content}")

    # Recuperar dos pasos atrás (n=2)
    print("undo(2) → dos pasos atrás:")
    caretaker.undo(writer, 2)
    print(f"  Contenido actual:\n{writer.content}")

    # Recuperar el estado más antiguo disponible (n=3)
    print("undo(3) → estado más antiguo guardado:")
    caretaker.undo(writer, 3)
    print(f"  Contenido actual:\n{writer.content}")

    # Intentar un índice inválido
    print("undo(5) → índice fuera de rango (debería dar error):")
    caretaker.undo(writer, 5)

    print("\n" + "=" * 60)
    print("  Fin del taller")
    print("=" * 60)
