# PUNTO 7:
# Imagine una situación donde pueda ser de utilidad el patrón “abstract factory”.



# ─── Productos abstractos (componentes de la UI) ─────────────────────

class Boton:
    """Clase base abstracta para botones."""

    def renderizar(self):
        raise NotImplementedError


class Checkbox:
    """Clase base abstracta para checkboxes."""

    def renderizar(self):
        raise NotImplementedError


class Ventana:
    """Clase base abstracta para ventanas."""

    def renderizar(self):
        raise NotImplementedError


# ─── Productos concretos Windows ─────────────────────────────────────

class BotonWindows(Boton):
    """Botón con estilo visual de Windows."""

    def renderizar(self):
        print("  [Botón Windows]  Bordes rectangulares, fondo azul, texto en blanco.")


class CheckboxWindows(Checkbox):
    """Checkbox con estilo visual de Windows."""

    def renderizar(self):
        print("  [Checkbox Windows]  Cuadrado con tilde azul al seleccionar.")


class VentanaWindows(Ventana):
    """Ventana con estilo visual de Windows."""

    def renderizar(self):
        print("  [Ventana Windows]  Barra de título azul, botones minimizar/maximizar/cerrar en esquina superior derecha.")


# ─── Productos concretos MacOS ───────────────────────────────────────

class BotonMacOS(Boton):
    """Botón con estilo visual de MacOS."""

    def renderizar(self):
        print("  [Botón MacOS]  Bordes redondeados, fondo gris claro, texto en negro.")


class CheckboxMacOS(Checkbox):
    """Checkbox con estilo visual de MacOS."""

    def renderizar(self):
        print("  [Checkbox MacOS]  Círculo con tilde azul al seleccionar.")


class VentanaMacOS(Ventana):
    """Ventana con estilo visual de MacOS."""

    def renderizar(self):
        print("  [Ventana MacOS]  Barra de título gris, botones cerrar/minimizar/maximizar en esquina superior izquierda.")


# ─── Abstract Factory (fábrica base) ────────────────────────────────

class UIFactory:
    """
    Fábrica abstracta que define la interfaz para crear
    familias de componentes visuales según la plataforma.
    """

    def crear_boton(self) -> Boton:
        raise NotImplementedError

    def crear_checkbox(self) -> Checkbox:
        raise NotImplementedError

    def crear_ventana(self) -> Ventana:
        raise NotImplementedError


# ─── Fábricas concretas ──────────────────────────────────────────────

class WindowsFactory(UIFactory):
    """
    Fábrica concreta que crea componentes con estilo Windows.
    Produce una familia completa y coherente de componentes para Windows.
    """

    def crear_boton(self) -> Boton:
        return BotonWindows()

    def crear_checkbox(self) -> Checkbox:
        return CheckboxWindows()

    def crear_ventana(self) -> Ventana:
        return VentanaWindows()


class MacOSFactory(UIFactory):
    """
    Fábrica concreta que crea componentes con estilo MacOS.
    Produce una familia completa y coherente de componentes para MacOS.
    """

    def crear_boton(self) -> Boton:
        return BotonMacOS()

    def crear_checkbox(self) -> Checkbox:
        return CheckboxMacOS()

    def crear_ventana(self) -> Ventana:
        return VentanaMacOS()


# ─── Aplicación cliente ──────────────────────────────────────────────

class Aplicacion:
    """
    Clase cliente que utiliza la fábrica para construir su interfaz.
    No sabe qué plataforma está usando: solo trabaja con la fábrica
    que recibe, lo que la hace completamente independiente del SO.
    """

    def __init__(self, factory: UIFactory):
        # Recibimos la fábrica correspondiente a la plataforma
        self._factory = factory

        # Creamos los componentes a través de la fábrica
        self.boton    = self._factory.crear_boton()
        self.checkbox = self._factory.crear_checkbox()
        self.ventana  = self._factory.crear_ventana()

    def renderizar_interfaz(self):
        """Renderiza todos los componentes de la interfaz."""
        print(f"  Renderizando interfaz...")
        self.ventana.renderizar()
        self.boton.renderizar()
        self.checkbox.renderizar()


# ─── Selector de fábrica según plataforma ───────────────────────────

def obtener_factory(plataforma: str) -> UIFactory:
    """
    Retorna la fábrica correspondiente según la plataforma indicada.
    En una aplicación real, esto podría detectarse automáticamente del sistema.
    """
    fabricas = {
        "windows": WindowsFactory,
        "macos":   MacOSFactory,
    }

    if plataforma not in fabricas:
        raise ValueError(f"Plataforma inválida. Opciones: {list(fabricas.keys())}")

    return fabricas[plataforma]()


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # ── Ejecutamos la app en Windows ──
    print("╔══════════════════════════════════════════════╗")
    print("║         Plataforma: WINDOWS                  ║")
    print("╚══════════════════════════════════════════════╝")
    factory_windows = obtener_factory("windows")
    app_windows = Aplicacion(factory_windows)
    app_windows.renderizar_interfaz()

    # ── Ejecutamos la app en MacOS ──
    print("\n╔══════════════════════════════════════════════╗")
    print("║         Plataforma: MacOS                    ║")
    print("╚══════════════════════════════════════════════╝")
    factory_macos = obtener_factory("macos")
    app_macos = Aplicacion(factory_macos)
    app_macos.renderizar_interfaz()