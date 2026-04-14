"""
rpn.py - Calculadora en notación polaca inversa (RPN)
Soporta: operaciones básicas, funciones matemáticas, trigonometría,
comandos de pila, constantes, memorias y manejo de errores.
"""

import math
import sys

# Precisión máxima de decimales en la salida
OUTPUT_PRECISION = 10


# Excepción personalizada para errores semánticos de la calculadora
class RPNError(Exception):
    """Excepción lanzada ante errores semánticos en la expresión RPN."""


class RPN:
    """Motor de evaluación RPN con pila, memorias y todas las operaciones."""

    # Tabla de despacho para operadores aritméticos básicos
    _BASIC_OPS = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
    }

    # Tabla de despacho para funciones trigonométricas (entrada/salida en grados)
    _TRIG_OPS = {
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tg": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atg": lambda x: math.degrees(math.atan(x)),
    }

    # CORRECCIÓN R0912: tabla de despacho para funciones matemáticas unarias simples.
    # Extraer ex, 10x y chs a una tabla reduce las ramas de _eval_math de 13 a 10,
    # resolviendo el warning too-many-branches (máximo permitido: 12).
    # CORRECCIÓN W0108: se referencian directamente math.exp y operator.neg en lugar
    # de envolverlas en lambdas innecesarias (unnecessary-lambda).
    _MATH_UNARY_OPS = {
        "ex": math.exp,
        "10x": lambda x: 10**x,  # no tiene equivalente directo en math
        "chs": lambda x: -x,  # negación unaria, sin equivalente directo
    }

    def __init__(self):
        # Pila principal de operandos
        self.s = []
        # 10 registros de memoria nombrados 00..09, inicializados en 0.0
        self.m = {f"{i:02d}": 0.0 for i in range(10)}

    def need(self, n):
        """Verifica que haya al menos n elementos en la pila; si no, lanza RPNError."""
        if len(self.s) < n:
            raise RPNError(f"Pila insuficiente (se necesitan {n}, hay {len(self.s)})")

    def pop(self):
        """Extrae y retorna el tope de la pila."""
        self.need(1)
        return self.s.pop()

    def push(self, x):
        """Convierte x a float y lo apila."""
        self.s.append(float(x))

    def _eval_constants(self, t):
        """Evalúa constantes matemáticas p, e, j. Retorna True si fue reconocido."""
        if t == "p":
            self.push(math.pi)  # pi ~ 3.14159
        elif t == "e":
            self.push(math.e)  # euler ~ 2.71828
        elif t == "j":
            self.push((1 + 5**0.5) / 2)  # phi (numero aureo) ~ 1.61803
        else:
            return False
        return True

    def _eval_basic_ops(self, t):
        """Evalúa operadores aritméticos básicos + - * /. Retorna True si reconocido."""
        if t not in self._BASIC_OPS and t != "/":
            return False
        self.need(2)
        b, a = self.pop(), self.pop()  # b = tope, a = segundo elemento
        if t == "/":
            if b == 0:
                raise RPNError("Division por cero")
            self.push(a / b)
        else:
            # Despacho via tabla: elimina elif por operador
            self.push(self._BASIC_OPS[t](a, b))
        return True

    def _eval_math(self, t):
        """Evalúa funciones matemáticas. Retorna True si el token fue reconocido."""
        if t == "sqrt":
            x = self.pop()
            if x < 0:
                raise RPNError("sqrt de número negativo")
            self.push(math.sqrt(x))
        elif t == "log":
            x = self.pop()
            if x <= 0:
                raise RPNError("log de número no positivo")
            self.push(math.log10(x))  # logaritmo base 10
        elif t == "ln":
            x = self.pop()
            if x <= 0:
                raise RPNError("ln de número no positivo")
            self.push(math.log(x))  # logaritmo natural
        elif t == "yx":
            self.need(2)
            x, y = self.pop(), self.pop()
            self.push(y**x)  # y elevado a x
        elif t == "1/x":
            x = self.pop()
            if x == 0:
                raise RPNError("Division por cero en 1/x")
            self.push(1 / x)  # inverso multiplicativo
        # CORRECCIÓN R0912: ex, 10x y chs se despachan via tabla _MATH_UNARY_OPS,
        # reemplazando 3 ramas elif por una sola, reduciendo la complejidad del método.
        elif t in self._MATH_UNARY_OPS:
            self.push(self._MATH_UNARY_OPS[t](self.pop()))
        else:
            return False
        return True

    def _eval_trig(self, t):
        """Evalúa funciones trigonométricas via tabla de despacho.
        
        Retorna True si el token fue reconocido.
        """
        if t not in self._TRIG_OPS:
            return False
        # Despacho directo: elimina la cadena de elif por función
        self.push(self._TRIG_OPS[t](self.pop()))
        return True

    def _eval_stack_cmds(self, t):
        """Evalúa comandos de pila dup/swap/drop/clear. Retorna True si reconocido."""
        # dup: duplica el tope | swap: intercambia los dos primeros
        # drop: descarta el tope | clear: vacia toda la pila
        if t == "dup":
            self.need(1)
            self.push(self.s[-1])
        elif t == "swap":
            self.need(2)
            self.s[-1], self.s[-2] = self.s[-2], self.s[-1]
        elif t == "drop":
            self.pop()
        elif t == "clear":
            self.s.clear()
        else:
            return False
        return True

    def eval(self, t):
        """
        Evalúa un token individual t delegando en métodos especializados.
        Orden: número → constantes → operadores → matemáticas → trig → pila.
        """
        # --- 1. Intentar parsear como número (int o float, incluyendo negativos) ---
        try:
            self.push(t)
            return
        except (ValueError, TypeError):
            pass

        # --- 2 a 6: delegar en métodos especializados por categoría ---
        if (
            self._eval_constants(t)
            or self._eval_basic_ops(t)
            or self._eval_math(t)
            or self._eval_trig(t)
            or self._eval_stack_cmds(t)
        ):
            return

        # --- 7. Token desconocido: ningún caso anterior lo reconocio ---
        raise RPNError(f"Token inválido: '{t}'")

    def run(self, expr):
        """
        Procesa la expresion RPN completa (string separado por espacios).
        Maneja sto/rcl como pares de tokens: '<valor> sto <slot>' / 'rcl <slot>'.
        Al finalizar debe quedar exactamente 1 elemento en la pila.
        """
        # Usar enumerate con iter permite consumir tokens de a pares para sto/rcl
        tokens = expr.split()
        it = iter(enumerate(tokens))
        for _, t in it:
            if t in ("sto", "rcl"):
                # El siguiente token es el slot de memoria
                try:
                    _, slot = next(it)
                # CORRECCIÓN W0707: se agrega 'from exc' para preservar la cadena
                # de excepciones original (raise-missing-from).
                except StopIteration as exc:
                    raise RPNError(
                        f"'{t}' requiere un slot (00-09) a continuacion"
                    ) from exc
                if slot not in self.m:
                    raise RPNError(f"Slot de memoria inválido: '{slot}' (use 00-09)")
                if t == "sto":
                    self.need(1)
                    self.m[slot] = self.pop()  # guarda en memoria
                else:
                    self.push(self.m[slot])  # recupera de memoria
            else:
                self.eval(t)

        # Validacion final: la pila debe tener exactamente 1 resultado
        # Si hay 0 o mas de 1, la expresion estaba mal formada
        if len(self.s) != 1:
            raise RPNError(
                f"La pila debe tener exactamente 1 valor al final (tiene {len(self.s)})"
            )
        return self.pop()


def format_result(result):
    """
    Formatea el resultado para mostrar enteros sin decimal
    y floats con precisión razonable, evitando artefactos de punto flotante.
    Ejemplo: 0.30000000000000004 se muestra como 0.3
    """
    if result == int(result):
        return str(int(result))
    # Redondear a OUTPUT_PRECISION cifras para evitar ruido de punto flotante
    rounded = round(result, OUTPUT_PRECISION)
    return str(rounded)


def main():
    """Punto de entrada: acepta expresion por argumento CLI o por stdin."""
    try:
        if len(sys.argv) > 1:
            expr = " ".join(sys.argv[1:])  # modo argumento: python rpn.py 3 4 +
        else:
            print("RPN> ", end="", flush=True, file=sys.stderr)
            expr = input()  # modo interactivo: lee desde stdin
        result = RPN().run(expr)
        # Mostrar resultado formateado sin artefactos de punto flotante
        print(format_result(result))
    except RPNError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
