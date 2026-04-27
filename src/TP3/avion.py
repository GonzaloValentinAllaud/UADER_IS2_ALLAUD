# PUNTO 5:
# Extienda el ejemplo visto en el taller en clase de forma que se pueda utilizar 
# para construir aviones en lugar de vehículos. Para simplificar suponga que un 
# avión tiene un “body”, 2 turbinas, 2 alas y un tren de aterrizaje. 

# ─── Clase Avion (Producto final) ────────────────────────────────────

class Avion:
    """
    Clase que representa el avión como producto final.
    Sus partes son ensambladas progresivamente por el Builder.
    """

    def __init__(self):
        # Inicializamos todas las partes como None hasta que sean construidas
        self.body             = None
        self.turbinas         = None
        self.alas             = None
        self.tren_aterrizaje  = None

    def mostrar(self):
        """Muestra el avión ensamblado con todas sus partes."""
        print(f"\n{'═'*45}")
        print(f"  AVIÓN ENSAMBLADO")
        print(f"{'─'*45}")
        print(f"  Body:              {self.body}")
        print(f"  Turbinas:          {self.turbinas}")
        print(f"  Alas:              {self.alas}")
        print(f"  Tren de aterrizaje:{self.tren_aterrizaje}")
        print(f"{'═'*45}")


# ─── Builder base (interfaz) ─────────────────────────────────────────

class AvionBuilder:
    """
    Clase base que define la interfaz del Builder.
    Cada subclase concreta implementa cómo construir cada parte del avión.
    """

    def __init__(self):
        # Cada builder parte de un avión vacío
        self.avion = Avion()

    def construir_body(self):
        raise NotImplementedError

    def construir_turbinas(self):
        raise NotImplementedError

    def construir_alas(self):
        raise NotImplementedError

    def construir_tren_aterrizaje(self):
        raise NotImplementedError

    def obtener_avion(self) -> Avion:
        """Retorna el avión construido."""
        return self.avion


# ─── Builders concretos ──────────────────────────────────────────────

class AvionComercialBuilder(AvionBuilder):
    """Builder concreto para construir un avión comercial de pasajeros."""

    def construir_body(self):
        # Cuerpo amplio para pasajeros
        self.avion.body = "Body ancho (wide-body) para 300 pasajeros"

    def construir_turbinas(self):
        # Los aviones comerciales tienen 2 turbinas de alto empuje
        self.avion.turbinas = "2 turbinas CFM56 de alto empuje"

    def construir_alas(self):
        # Alas largas y optimizadas para largas distancias
        self.avion.alas = "2 alas de 35m con winglets aerodinámicos"

    def construir_tren_aterrizaje(self):
        # Tren de aterrizaje robusto para pistas comerciales
        self.avion.tren_aterrizaje = "Tren triciclo retráctil con 6 ruedas"


class AvionCazaBuilder(AvionBuilder):
    """Builder concreto para construir un avión de combate."""

    def construir_body(self):
        # Cuerpo estrecho y aerodinámico para alta velocidad
        self.avion.body = "Body estrecho de fibra de carbono reforzado"

    def construir_turbinas(self):
        # Los cazas tienen turbinas con postcombustión
        self.avion.turbinas = "2 turbinas General Electric F110 con postcombustión"

    def construir_alas(self):
        # Alas cortas y en delta para maniobras a alta velocidad
        self.avion.alas = "2 alas en delta de 9m para alta maniobrabilidad"

    def construir_tren_aterrizaje(self):
        # Tren reforzado para operaciones en portaaviones
        self.avion.tren_aterrizaje = "Tren retráctil reforzado para portaaviones"


# ─── Director ────────────────────────────────────────────────────────

class DirectorAvion:
    """
    Director que define el orden en que se construyen las partes del avión.
    Trabaja con cualquier Builder que respete la interfaz base.
    """

    def __init__(self, builder: AvionBuilder):
        # Recibe el builder concreto a utilizar
        self._builder = builder

    def cambiar_builder(self, builder: AvionBuilder):
        """Permite cambiar el builder en tiempo de ejecución."""
        self._builder = builder

    def construir_avion(self):
        """
        Dirige la construcción del avión paso a paso en el orden correcto:
        primero el body, luego las turbinas, las alas y finalmente el tren.
        """
        print("\n  Iniciando construcción del avión...")
        self._builder.construir_body()
        print("  ✓ Body construido")
        self._builder.construir_turbinas()
        print("  ✓ Turbinas instaladas")
        self._builder.construir_alas()
        print("  ✓ Alas ensambladas")
        self._builder.construir_tren_aterrizaje()
        print("  ✓ Tren de aterrizaje montado")

    def obtener_avion(self) -> Avion:
        """Retorna el avión ya construido desde el builder."""
        return self._builder.obtener_avion()


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # ── Construimos un avión comercial ──
    print("╔══════════════════════════════════════════════╗")
    print("║       Construcción: Avión Comercial          ║")
    print("╚══════════════════════════════════════════════╝")
    builder_comercial = AvionComercialBuilder()
    director = DirectorAvion(builder_comercial)
    director.construir_avion()
    avion_comercial = director.obtener_avion()
    avion_comercial.mostrar()

    # ── Construimos un avión de combate ──
    print("\n╔══════════════════════════════════════════════╗")
    print("║       Construcción: Avión de Combate         ║")
    print("╚══════════════════════════════════════════════╝")
    builder_caza = AvionCazaBuilder()
    director.cambiar_builder(builder_caza)
    director.construir_avion()
    avion_caza = director.obtener_avion()
    avion_caza.mostrar()