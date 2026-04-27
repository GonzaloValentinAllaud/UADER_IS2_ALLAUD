# PUNTO 4:
# Implemente una clase “factura” que tenga un importe correspondiente al total 
# de la factura pero de acuerdo a la condición impositiva del cliente (IVA 
# Responsable, IVA No Inscripto, IVA Exento) genere facturas que indiquen tal 
# condición.  

# ─── Clase base abstracta de Factura ────────────────────────────────

class Factura:
    """
    Clase base que define la interfaz común para todos los tipos de factura.
    Cada subclase implementa su propio comportamiento según condición impositiva.
    """

    def __init__(self, cliente: str, importe: float):
        self.cliente = cliente
        self.importe = importe

    def tipo_factura(self) -> str:
        """Retorna el tipo de factura (A, B o C)."""
        raise NotImplementedError

    def condicion(self) -> str:
        """Retorna la condición impositiva del cliente."""
        raise NotImplementedError

    def calcular(self) -> dict:
        """Calcula el desglose de importes según la condición impositiva."""
        raise NotImplementedError

    def emitir(self):
        """Emite la factura mostrando todos sus datos por pantalla."""

        # Obtenemos el desglose según la condición impositiva
        desglose = self.calcular()

        # Imprimimos el encabezado
        print(f"\n{'═'*45}")
        print(f"  {self.tipo_factura()}")
        print(f"{'─'*45}")
        print(f"  Cliente:    {self.cliente}")
        print(f"  Condición:  {self.condicion()}")
        print(f"{'─'*45}")

        # Imprimimos el desglose de importes
        for concepto, valor in desglose.items():
            print(f"  {concepto:<30} $ {valor:>8.2f}")

        print(f"{'═'*45}")


# ─── Productos concretos (tipos de factura) ──────────────────────────

class FacturaA(Factura):
    """
    Factura tipo A para clientes con IVA Responsable Inscripto.
    Discrimina el IVA del importe neto.
    """

    def tipo_factura(self) -> str:
        return "FACTURA A"

    def condicion(self) -> str:
        return "IVA Responsable Inscripto"

    def calcular(self) -> dict:
        # El importe es la base neta, se calcula y discrimina el IVA
        iva   = round(self.importe * 0.21, 2)
        total = round(self.importe + iva, 2)
        return {
            "Importe neto":  self.importe,
            "IVA (21%)":     iva,
            "Total factura": total,
        }


class FacturaB(Factura):
    """
    Factura tipo B para clientes con IVA No Inscripto.
    El IVA está incluido en el precio final y no se discrimina.
    """

    def tipo_factura(self) -> str:
        return "FACTURA B"

    def condicion(self) -> str:
        return "IVA No Inscripto"

    def calcular(self) -> dict:
        # El importe ya incluye el IVA, no se discrimina
        return {
            "Importe total (IVA incluido)": self.importe,
        }


class FacturaC(Factura):
    """
    Factura tipo C para clientes con IVA Exento.
    No se aplica ninguna carga de IVA sobre el importe.
    """

    def tipo_factura(self) -> str:
        return "FACTURA C"

    def condicion(self) -> str:
        return "IVA Exento"

    def calcular(self) -> dict:
        # El importe no tiene carga de IVA
        return {
            "Importe exento de IVA": self.importe,
        }


# ─── Abstract Factory ────────────────────────────────────────────────

class FacturaFactory:
    """
    Abstract Factory que centraliza la creación de facturas.
    Según la condición impositiva del cliente, instancia
    el tipo de factura correspondiente.
    """

    # Mapa de condiciones impositivas a sus clases de factura
    _tipos = {
        "responsable":  FacturaA,
        "no_inscripto": FacturaB,
        "exento":       FacturaC,
    }

    @staticmethod
    def crear_factura(cliente: str, importe: float, condicion: str) -> Factura:
        """
        Método de fábrica que crea y retorna la factura correspondiente.
        :param cliente: Nombre del cliente
        :param importe: Importe base de la factura
        :param condicion: 'responsable', 'no_inscripto' o 'exento'
        """
        # Verificamos que la condición impositiva sea válida
        if condicion not in FacturaFactory._tipos:
            raise ValueError(f"Condición inválida. Opciones: {list(FacturaFactory._tipos.keys())}")

        # Instanciamos y retornamos el tipo de factura correspondiente
        return FacturaFactory._tipos[condicion](cliente, importe)


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # Creamos las facturas a través de la fábrica según condición impositiva
    factura1 = FacturaFactory.crear_factura("Juan Pérez", 1000.00, "responsable")
    factura1.emitir()

    factura2 = FacturaFactory.crear_factura("María López", 1500.00, "no_inscripto")
    factura2.emitir()

    factura3 = FacturaFactory.crear_factura("Hospital Municipal", 3200.00, "exento")
    factura3.emitir()