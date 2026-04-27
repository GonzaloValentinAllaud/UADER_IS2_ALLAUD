# PUNTO 2:
# Elabore una clase para el cálculo del valor de impuestos a ser utilizado por 
# todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado 
# deberá recibir un valor de importe base imponible y deberá retornar la suma 
# del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre 
# esa base imponible.

# ─── Clase Singleton: Calculadora de Impuestos ──────────────────────

class TaxCalculator:
    """
    Clase Singleton para el cálculo de impuestos.
    Garantiza que todas las clases que la invoquen usen la misma instancia.
    """

    # Atributo de clase que almacena la única instancia (None hasta la primera llamada)
    _instancia = None

    # Tasas impositivas definidas como constantes de clase
    IVA         = 0.21   # 21%
    IIBB        = 0.05   # 5%
    CONTRIB_MUN = 0.012  # 1,2%

    def __new__(cls):
        """
        Sobrescribimos __new__ para controlar la creación del objeto.
        Si ya existe una instancia la retorna, si no, la crea por primera vez.
        """
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular_impuestos(self, base_imponible: float) -> dict:
        """
        Calcula los impuestos sobre una base imponible dada.
        Retorna un diccionario con el desglose de cada impuesto y los totales.
        """
        # Validamos que la base imponible no sea negativa
        if base_imponible < 0:
            raise ValueError("La base imponible no puede ser negativa.")

        # Calculamos cada impuesto por separado
        iva         = base_imponible * self.IVA
        iibb        = base_imponible * self.IIBB
        contrib_mun = base_imponible * self.CONTRIB_MUN

        # Sumamos el total de impuestos
        total = iva + iibb + contrib_mun

        # Retornamos el desglose completo redondeado a 2 decimales
        return {
            "base_imponible":        base_imponible,
            "IVA (21%)":             round(iva, 2),
            "IIBB (5%)":             round(iibb, 2),
            "Contribuciones (1,2%)": round(contrib_mun, 2),
            "total_impuestos":       round(total, 2),
            "total_con_impuestos":   round(base_imponible + total, 2),
        }


# ─── Clases que utilizan TaxCalculator ──────────────────────────────

class Factura:
    """Clase que representa una factura y utiliza TaxCalculator para calcular impuestos."""

    def procesar(self, importe: float):
        # Obtenemos la instancia Singleton de TaxCalculator
        calc = TaxCalculator()

        # Calculamos los impuestos sobre el importe recibido
        resultado = calc.calcular_impuestos(importe)

        # Mostramos el desglose por pantalla
        print(f"\n{'─'*40}")
        print(f"  Factura")
        print(f"{'─'*40}")
        for concepto, valor in resultado.items():
            print(f"  {concepto:<25} $ {valor:>10.2f}")
        print(f"{'─'*40}")


class Presupuesto:
    """Clase que representa un presupuesto y utiliza TaxCalculator para calcular impuestos."""

    def procesar(self, importe: float):
        # Obtenemos la instancia Singleton de TaxCalculator
        calc = TaxCalculator()

        # Calculamos los impuestos sobre el importe recibido
        resultado = calc.calcular_impuestos(importe)

        # Mostramos el desglose por pantalla
        print(f"\n{'─'*40}")
        print(f"  Presupuesto")
        print(f"{'─'*40}")
        for concepto, valor in resultado.items():
            print(f"  {concepto:<25} $ {valor:>10.2f}")
        print(f"{'─'*40}")


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # Instanciamos y ejecutamos cada clase con distintos importes
    Factura().procesar(1000)
    Presupuesto().procesar(2500.50)

    # Verificamos que ambas clases obtienen la misma instancia de TaxCalculator
    calc1 = TaxCalculator()
    calc2 = TaxCalculator()
    print(f"\n¿Misma instancia (TaxCalculator)? {calc1 is calc2}")  # Debe imprimir True