# PUNTO 3:
# Genere una clase donde se instancie una comida rápida “hamburguesa” que 
# pueda ser entregada en mostrador, retirada por el cliente o enviada por 
# delivery. A los efectos prácticos bastará que la clase imprima el método de 
# entrega. 

# ─── Clases de métodos de entrega ───────────────────────────────────

class EntregaMostrador:
    """Entrega la hamburguesa directamente en el mostrador del local."""

    def entregar(self):
        print("  Entrega en MOSTRADOR: su hamburguesa está lista, retírela en caja.")


class RetiroCliente:
    """El cliente retira la hamburguesa en un punto de retiro designado."""

    def entregar(self):
        print("  Retiro por el CLIENTE: diríjase a la zona de retiro con su número de pedido.")


class Delivery:
    """La hamburguesa es enviada al domicilio del cliente."""

    def entregar(self):
        print("  DELIVERY: su hamburguesa está en camino, llegará en 30 minutos.")


# ─── Clase Hamburguesa (Factory Method) ─────────────────────────────

class Hamburguesa:
    """
    Clase que representa una hamburguesa.
    Utiliza el patrón Factory Method para instanciar el método de entrega
    correspondiente según lo que se indique al momento de crear el pedido.
    """

    # Métodos de entrega disponibles y sus clases correspondientes
    METODOS_ENTREGA = {
        "mostrador": EntregaMostrador,
        "retiro":    RetiroCliente,
        "delivery":  Delivery,
    }

    def __init__(self, nombre: str, metodo_entrega: str):
        """
        Constructor de la hamburguesa.
        :param nombre: Nombre o descripción de la hamburguesa
        :param metodo_entrega: 'mostrador', 'retiro' o 'delivery'
        """
        self.nombre = nombre

        # Verificamos que el método de entrega sea válido
        if metodo_entrega not in self.METODOS_ENTREGA:
            raise ValueError(f"Método de entrega inválido. Opciones: {list(self.METODOS_ENTREGA.keys())}")

        # Factory Method: instanciamos la clase de entrega correspondiente
        self.entrega = self.METODOS_ENTREGA[metodo_entrega]()

    def preparar(self):
        """Simula la preparación de la hamburguesa."""
        print(f"\n{'─'*50}")
        print(f"  Preparando: {self.nombre}")
        print(f"{'─'*50}")

    def entregar(self):
        """Delega la entrega al objeto de entrega instanciado por el Factory Method."""
        self.entrega.entregar()
        print(f"{'─'*50}")


# ─── Programa principal ──────────────────────────────────────────────

if __name__ == "__main__":

    # Creamos tres pedidos con distintos métodos de entrega
    pedido1 = Hamburguesa("Hamburguesa Clásica", "mostrador")
    pedido1.preparar()
    pedido1.entregar()

    pedido2 = Hamburguesa("Hamburguesa Doble Cheddar", "retiro")
    pedido2.preparar()
    pedido2.entregar()

    pedido3 = Hamburguesa("Hamburguesa BBQ Bacon", "delivery")
    pedido3.preparar()
    pedido3.entregar()