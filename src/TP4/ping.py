# PUNTO 1:
# Provea una clase ping que luego de creada al ser invocada con un método 
# “execute(string)” realice 10 intentos de ping a la dirección IP contenida en 
# “string” (argumento pasado), la clase solo debe funcionar si la dirección IP 
# provista comienza con “192.”. Provea un método executefree(string) que haga 
# lo mismo pero sin el control de dirección. Ahora provea una clase pingproxy 
# cuyo método execute(string) si la dirección es “192.168.0.254” realice un ping a 
# www.google.com usando el método executefree de ping y re-envie a execute 
# de la clase ping en cualquier otro caso. (Modele la solución como un patrón 
# proxy). 

import subprocess
import platform


class ping:
    """
    Clase de servicio real que ejecuta pings a una dirección IP.
    
    execute(string)    : solo acepta direcciones que comiencen con "192."
    executefree(string): ejecuta el ping sin ningún control de dirección
    """

    def _do_ping(self, address: str, count: int = 10) -> None:
        """Ejecuta el ping real al sistema operativo."""
        # El flag varía según el SO (-n en Windows, -c en Linux/Mac)
        flag = "-n" if platform.system().lower() == "windows" else "-c"
        print(f"\n[ping] Ejecutando {count} pings a: {address}")
        try:
            result = subprocess.run(
                ["ping", flag, str(count), address],
                capture_output=True,
                text=True,
                timeout=30
            )
            print(result.stdout)
            if result.returncode != 0:
                print(f"[ping] Host no alcanzable o error: {result.stderr}")
        except FileNotFoundError:
            print("[ping] Comando 'ping' no disponible en este sistema.")
        except subprocess.TimeoutExpired:
            print("[ping] Tiempo de espera agotado.")

    def execute(self, string: str) -> None:
        """
        Realiza 10 intentos de ping a la dirección IP en 'string'.
        Solo funciona si la dirección comienza con "192."
        """
        if not string.startswith("192."):
            print(f"[ping.execute] RECHAZADO: la dirección '{string}' "
                  f"no comienza con '192.' — operación cancelada.")
            return
        self._do_ping(string, count=10)

    def executefree(self, string: str) -> None:
        """
        Realiza 10 intentos de ping a la dirección IP en 'string'
        sin ningún control sobre el formato de la dirección.
        """
        self._do_ping(string, count=10)


class pingproxy:
    """
    Proxy de ping.

    Intercepta las llamadas a execute(string):
      - Si la dirección es exactamente "192.168.0.254":
            hace un ping a www.google.com usando ping.executefree()
      - En cualquier otro caso:
            re-envía la llamada a ping.execute()

    El cliente usa pingproxy sin saber que existe la clase ping subyacente.
    """

    def __init__(self):
        self._real_ping = ping()
        self._redirect_address = "192.168.0.254"
        self._google = "www.google.com"

    def execute(self, string: str) -> None:
        """
        Punto de entrada del proxy.
        Decide a qué método del servicio real delegar según la IP.
        """
        if string == self._redirect_address:
            print(f"[pingproxy] IP especial detectada ({string}). "
                  f"Redirigiendo a '{self._google}' via executefree().")
            self._real_ping.executefree(self._google)
        else:
            print(f"[pingproxy] IP normal ({string}). "
                  f"Delegando a ping.execute().")
            self._real_ping.execute(string)


# ─────────────────────────────────────────────
#  Demostración del comportamiento
# ─────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("  DEMO - Patrón Proxy: pingproxy")
    print("=" * 60)

    proxy = pingproxy()

    # Caso 1: IP normal válida (empieza con "192.") → ping.execute() la acepta
    print("\n--- Caso 1: IP válida '192.168.1.1' ---")
    proxy.execute("192.168.1.1")

    # Caso 2: IP que NO empieza con "192." → ping.execute() la rechaza
    print("\n--- Caso 2: IP fuera de rango '10.0.0.1' ---")
    proxy.execute("10.0.0.1")

    # Caso 3: IP especial → proxy redirige a google via executefree
    print("\n--- Caso 3: IP especial '192.168.0.254' ---")
    proxy.execute("192.168.0.254")

    print("\n" + "=" * 60)
    print("  DEMO - Clase ping directa (sin proxy)")
    print("=" * 60)

    p = ping()

    # execute con IP válida
    print("\n--- ping.execute() con '192.168.1.100' ---")
    p.execute("192.168.1.100")

    # execute con IP inválida
    print("\n--- ping.execute() con '8.8.8.8' (debe rechazar) ---")
    p.execute("8.8.8.8")

    # executefree sin restricción
    print("\n--- ping.executefree() con '8.8.8.8' (sin restricción) ---")
    p.executefree("8.8.8.8")