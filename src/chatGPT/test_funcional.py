"""
test_functional_rpn.py
======================
Test funcional de la calculadora RPN (rpn.py).

Objetivo
--------
Verificar el comportamiento observable del programa completo desde la
perspectiva del usuario final: entrada de expresión → salida correcta
o mensaje de error apropiado. No se testea la estructura interna.

Estrategia de casos
-------------------
Se aplican las siguientes técnicas de diseño:

  1. Clases de equivalencia  – un representante por cada grupo de entradas
     que el sistema debería tratar de la misma forma.
  2. Valores límite           – bordes de rangos: cero, negativos, enteros
     exactos vs. flotantes con artefactos, slots 00 y 09.
  3. Casos de uso reales      – expresiones que un usuario típico escribiría
     (conversión de temperaturas, hipotenusa, interés compuesto, etc.).
  4. Encadenamiento           – expresiones largas que ejercitan la pila con
     múltiples operaciones consecutivas.
  5. Errores esperados        – cada categoría de error debe producir un
     mensaje reconocible; se verifica tanto que se lanza RPNError como que
     el texto del mensaje es adecuado.

Organización
------------
  TC-01  Literales numéricos
  TC-02  Operaciones aritméticas básicas
  TC-03  Funciones matemáticas
  TC-04  Trigonometría (entrada y salida en grados)
  TC-05  Comandos de pila
  TC-06  Memoria STO / RCL
  TC-07  Constantes matemáticas
  TC-08  Expresiones encadenadas (casos de uso reales)
  TC-09  Formato de salida (format_result)
  TC-10  Errores semánticos esperados
  TC-11  Interfaz CLI (main)
"""

import math
import sys
import io
import unittest

from rpn import RPN, RPNError, format_result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(expr: str) -> float:
    """Ejecuta una expresión RPN y devuelve el resultado numérico."""
    return RPN().run(expr)


def run_main(args: list[str], stdin_text: str | None = None) -> tuple[str, str]:
    """
    Ejecuta main() capturando stdout y stderr.
    Devuelve (stdout_strip, stderr_strip).
    """
    from rpn import main
    old_argv = sys.argv
    sys.argv = ["rpn.py"] + args
    out, err = io.StringIO(), io.StringIO()
    old_out, old_err, old_in = sys.stdout, sys.stderr, sys.stdin
    sys.stdout, sys.stderr = out, err
    if stdin_text is not None:
        sys.stdin = io.StringIO(stdin_text)
    try:
        main()
    except SystemExit:
        pass
    finally:
        sys.stdout, sys.stderr, sys.stdin = old_out, old_err, old_in
        sys.argv = old_argv
    return out.getvalue().strip(), err.getvalue().strip()


def assert_error(test_case, expr: str, keyword: str):
    """
    Afirma que expr lanza RPNError y que el mensaje contiene keyword
    (comparación insensible a mayúsculas y tildes no son problema porque
    se busca en .lower()).
    """
    with test_case.assertRaises(RPNError) as ctx:
        run(expr)
    test_case.assertIn(keyword, str(ctx.exception).lower(),
                       msg=f"Se esperaba '{keyword}' en el mensaje de error para: {expr!r}")


# ===========================================================================
# TC-01  Literales numéricos
# ===========================================================================
class TC01_Literals(unittest.TestCase):
    """
    Verifica que el parser reconoce correctamente distintos formatos
    de literales numéricos como único token en la pila.

    Casos:
      TC-01-01  Entero positivo                → 7
      TC-01-02  Entero negativo                → -3
      TC-01-03  Cero                           → 0
      TC-01-04  Flotante con parte decimal     → 3.14
      TC-01-05  Flotante negativo              → -2.5
      TC-01-06  Notación científica positiva   → 1e3  (1000.0)
      TC-01-07  Notación científica negativa   → 1e-2 (0.01)
    """

    def test_TC0101_positive_integer(self):
        self.assertEqual(run("7"), 7)

    def test_TC0102_negative_integer(self):
        self.assertEqual(run("-3"), -3)

    def test_TC0103_zero(self):
        self.assertEqual(run("0"), 0)

    def test_TC0104_positive_float(self):
        self.assertAlmostEqual(run("3.14"), 3.14)

    def test_TC0105_negative_float(self):
        self.assertAlmostEqual(run("-2.5"), -2.5)

    def test_TC0106_scientific_positive(self):
        self.assertAlmostEqual(run("1e3"), 1000.0)

    def test_TC0107_scientific_negative_exp(self):
        self.assertAlmostEqual(run("1e-2"), 0.01)


# ===========================================================================
# TC-02  Operaciones aritméticas básicas
# ===========================================================================
class TC02_BasicOps(unittest.TestCase):
    """
    Verifica las cuatro operaciones aritméticas (+, -, *, /) con
    combinaciones de valores positivos, negativos y flotantes.

    Casos:
      TC-02-01  Suma de enteros positivos          3 4 +  → 7
      TC-02-02  Resta con resultado positivo       10 3 - → 7
      TC-02-03  Resta con resultado negativo       3 10 - → -7
      TC-02-04  Multiplicación positivos           6 7 *  → 42
      TC-02-05  Multiplicación con negativo        -3 4 * → -12
      TC-02-06  Multiplicación dos negativos       -3 -4 *→ 12
      TC-02-07  División exacta                    10 2 / → 5
      TC-02-08  División con resultado decimal     1 3 /  → 0.333…
      TC-02-09  División donde dividendo < divisor 1 4 /  → 0.25
      TC-02-10  Operación con flotantes            1.5 2.5 + → 4.0
    """

    def test_TC0201_add_positive(self):
        self.assertEqual(run("3 4 +"), 7)

    def test_TC0202_subtract_positive_result(self):
        self.assertEqual(run("10 3 -"), 7)

    def test_TC0203_subtract_negative_result(self):
        self.assertEqual(run("3 10 -"), -7)

    def test_TC0204_multiply_positive(self):
        self.assertEqual(run("6 7 *"), 42)

    def test_TC0205_multiply_one_negative(self):
        self.assertEqual(run("-3 4 *"), -12)

    def test_TC0206_multiply_two_negatives(self):
        self.assertEqual(run("-3 -4 *"), 12)

    def test_TC0207_divide_exact(self):
        self.assertEqual(run("10 2 /"), 5)

    def test_TC0208_divide_repeating_decimal(self):
        self.assertAlmostEqual(run("1 3 /"), 1/3)

    def test_TC0209_divide_small_result(self):
        self.assertAlmostEqual(run("1 4 /"), 0.25)

    def test_TC0210_float_operands(self):
        self.assertAlmostEqual(run("1.5 2.5 +"), 4.0)


# ===========================================================================
# TC-03  Funciones matemáticas
# ===========================================================================
class TC03_MathFunctions(unittest.TestCase):
    """
    Verifica cada función matemática con al menos un valor representativo
    y uno en el límite del dominio válido donde corresponda.

    Casos:
      TC-03-01  sqrt de cuadrado perfecto          9 sqrt   → 3
      TC-03-02  sqrt de flotante                   2 sqrt   → √2
      TC-03-03  sqrt de cero (límite inferior)     0 sqrt   → 0
      TC-03-04  log base 10 de 100                 100 log  → 2
      TC-03-05  log base 10 de 1 (límite)          1 log    → 0
      TC-03-06  ln de e                            e ln     → 1
      TC-03-07  ln de 1 (límite)                   1 ln     → 0
      TC-03-08  e^x con x=1                        1 ex     → e
      TC-03-09  e^0 (límite)                       0 ex     → 1
      TC-03-10  10^x con x=2                       2 10x    → 100
      TC-03-11  10^0 (límite)                      0 10x    → 1
      TC-03-12  y^x: 2^10                          2 10 yx  → 1024
      TC-03-13  y^x: fraccionario 4^0.5            4 0.5 yx → 2
      TC-03-14  Inverso 1/4                        4 1/x    → 0.25
      TC-03-15  Cambio de signo positivo           5 chs    → -5
      TC-03-16  Cambio de signo negativo           -3 chs   → 3
      TC-03-17  Cambio de signo de cero            0 chs    → 0
    """

    def test_TC0301_sqrt_perfect_square(self):
        self.assertAlmostEqual(run("9 sqrt"), 3.0)

    def test_TC0302_sqrt_float(self):
        self.assertAlmostEqual(run("2 sqrt"), math.sqrt(2))

    def test_TC0303_sqrt_zero(self):
        self.assertAlmostEqual(run("0 sqrt"), 0.0)

    def test_TC0304_log10_100(self):
        self.assertAlmostEqual(run("100 log"), 2.0)

    def test_TC0305_log10_one(self):
        self.assertAlmostEqual(run("1 log"), 0.0)

    def test_TC0306_ln_of_e(self):
        self.assertAlmostEqual(run("e ln"), 1.0)

    def test_TC0307_ln_of_one(self):
        self.assertAlmostEqual(run("1 ln"), 0.0)

    def test_TC0308_exp_one(self):
        self.assertAlmostEqual(run("1 ex"), math.e)

    def test_TC0309_exp_zero(self):
        self.assertAlmostEqual(run("0 ex"), 1.0)

    def test_TC0310_pow10_two(self):
        self.assertAlmostEqual(run("2 10x"), 100.0)

    def test_TC0311_pow10_zero(self):
        self.assertAlmostEqual(run("0 10x"), 1.0)

    def test_TC0312_yx_integer(self):
        self.assertAlmostEqual(run("2 10 yx"), 1024.0)

    def test_TC0313_yx_fractional(self):
        self.assertAlmostEqual(run("4 0.5 yx"), 2.0)

    def test_TC0314_inverse(self):
        self.assertAlmostEqual(run("4 1/x"), 0.25)

    def test_TC0315_chs_positive(self):
        self.assertAlmostEqual(run("5 chs"), -5.0)

    def test_TC0316_chs_negative(self):
        self.assertAlmostEqual(run("-3 chs"), 3.0)

    def test_TC0317_chs_zero(self):
        self.assertAlmostEqual(run("0 chs"), 0.0)


# ===========================================================================
# TC-04  Trigonometría
# ===========================================================================
class TC04_Trig(unittest.TestCase):
    """
    Todas las funciones trigonométricas trabajan en grados.
    Se verifican ángulos notables y los pares directas/inversas.

    Casos:
      TC-04-01  sin(0°)   → 0
      TC-04-02  sin(90°)  → 1
      TC-04-03  sin(180°) → 0  (≈ 0 por aritmética flotante)
      TC-04-04  cos(0°)   → 1
      TC-04-05  cos(90°)  → 0  (≈ 0)
      TC-04-06  cos(180°) → -1
      TC-04-07  tg(45°)   → 1
      TC-04-08  tg(0°)    → 0
      TC-04-09  asin(1)   → 90°
      TC-04-10  asin(0)   → 0°
      TC-04-11  acos(1)   → 0°
      TC-04-12  acos(0)   → 90°
      TC-04-13  atg(1)    → 45°
      TC-04-14  atg(0)    → 0°
      TC-04-15  Ciclo sin→asin: asin(sin(30°)) → 30°
    """

    def test_TC0401_sin_zero(self):
        self.assertAlmostEqual(run("0 sin"), 0.0)

    def test_TC0402_sin_90(self):
        self.assertAlmostEqual(run("90 sin"), 1.0)

    def test_TC0403_sin_180(self):
        self.assertAlmostEqual(run("180 sin"), 0.0, places=10)

    def test_TC0404_cos_zero(self):
        self.assertAlmostEqual(run("0 cos"), 1.0)

    def test_TC0405_cos_90(self):
        self.assertAlmostEqual(run("90 cos"), 0.0, places=10)

    def test_TC0406_cos_180(self):
        self.assertAlmostEqual(run("180 cos"), -1.0)

    def test_TC0407_tan_45(self):
        self.assertAlmostEqual(run("45 tg"), 1.0)

    def test_TC0408_tan_zero(self):
        self.assertAlmostEqual(run("0 tg"), 0.0)

    def test_TC0409_asin_one(self):
        self.assertAlmostEqual(run("1 asin"), 90.0)

    def test_TC0410_asin_zero(self):
        self.assertAlmostEqual(run("0 asin"), 0.0)

    def test_TC0411_acos_one(self):
        self.assertAlmostEqual(run("1 acos"), 0.0)

    def test_TC0412_acos_zero(self):
        self.assertAlmostEqual(run("0 acos"), 90.0)

    def test_TC0413_atan_one(self):
        self.assertAlmostEqual(run("1 atg"), 45.0)

    def test_TC0414_atan_zero(self):
        self.assertAlmostEqual(run("0 atg"), 0.0)

    def test_TC0415_sin_asin_roundtrip(self):
        # asin(sin(30°)) debe devolver 30°
        self.assertAlmostEqual(run("30 sin asin"), 30.0)


# ===========================================================================
# TC-05  Comandos de pila
# ===========================================================================
class TC05_StackCommands(unittest.TestCase):
    """
    Verifica que dup, swap, drop y clear manipulan la pila correctamente.

    Casos:
      TC-05-01  dup duplica el tope: 3 dup +        → 6
      TC-05-02  dup no altera el original            pila tiene 2 copias
      TC-05-03  swap invierte el orden: 10 3 swap - → -7 (3-10)
      TC-05-04  drop descarta el tope: 5 99 drop    → 5
      TC-05-05  clear vacía la pila, luego push: 9 8 7 clear 42 → 42
      TC-05-06  Cadena dup+swap: 4 dup swap -       → 0  (4-4)
    """

    def test_TC0501_dup_used_in_sum(self):
        self.assertEqual(run("3 dup +"), 6)

    def test_TC0502_dup_keeps_two_copies(self):
        rpn = RPN()
        rpn.push(7)
        rpn.eval("dup")
        self.assertEqual(len(rpn.s), 2)
        self.assertEqual(rpn.s[0], rpn.s[1])

    def test_TC0503_swap_reverses_order(self):
        self.assertAlmostEqual(run("10 3 swap -"), -7)

    def test_TC0504_drop_discards_top(self):
        self.assertEqual(run("5 99 drop"), 5)

    def test_TC0505_clear_empties_stack(self):
        self.assertEqual(run("9 8 7 clear 42"), 42)

    def test_TC0506_dup_then_swap_subtract(self):
        # 4 dup → [4,4], swap → [4,4], - → 0
        self.assertAlmostEqual(run("4 dup swap -"), 0.0)


# ===========================================================================
# TC-06  Memoria STO / RCL
# ===========================================================================
class TC06_Memory(unittest.TestCase):
    """
    Verifica los 10 slots de memoria (00-09): escritura, lectura,
    sobreescritura y que el valor por defecto es 0.

    Casos:
      TC-06-01  STO y RCL básico en slot 05         → 42
      TC-06-02  RCL sin STO previo devuelve 0       → 0.0
      TC-06-03  Slot 00 (primer slot límite)        → 99
      TC-06-04  Slot 09 (último slot límite)        → 77
      TC-06-05  Sobreescritura del mismo slot       → 20
      TC-06-06  Dos slots independientes no se mezclan
      TC-06-07  STO consume el tope; pila queda con lo anterior
    """

    def test_TC0601_sto_rcl_basic(self):
        self.assertEqual(run("42 sto 05 8 rcl 05 +"), 50)

    def test_TC0602_rcl_default_zero(self):
        self.assertAlmostEqual(run("rcl 03"), 0.0)

    def test_TC0603_slot_00(self):
        self.assertAlmostEqual(run("99 sto 00 rcl 00"), 99.0)

    def test_TC0604_slot_09(self):
        self.assertAlmostEqual(run("77 sto 09 rcl 09"), 77.0)

    def test_TC0605_overwrite_slot(self):
        self.assertAlmostEqual(run("10 sto 01 20 sto 01 rcl 01"), 20.0)

    def test_TC0606_two_slots_independent(self):
        self.assertAlmostEqual(run("10 sto 01 20 sto 02 rcl 01 rcl 02 +"), 30.0)

    def test_TC0607_sto_consumes_top(self):
        # 5 10 sto 00 → queda 5 en pila; rcl 00 → [5, 10]; + → 15
        self.assertAlmostEqual(run("5 10 sto 00 rcl 00 +"), 15.0)


# ===========================================================================
# TC-07  Constantes matemáticas
# ===========================================================================
class TC07_Constants(unittest.TestCase):
    """
    Verifica las tres constantes integradas.

    Casos:
      TC-07-01  p → π  (math.pi)
      TC-07-02  e → e  (math.e)
      TC-07-03  j → φ  (número áureo)
      TC-07-04  p usada en cálculo: 2*π usando p 2 *
      TC-07-05  e usada en ln: e ln → 1
    """

    def test_TC0701_pi(self):
        self.assertAlmostEqual(run("p"), math.pi)

    def test_TC0702_euler(self):
        self.assertAlmostEqual(run("e"), math.e)

    def test_TC0703_phi(self):
        self.assertAlmostEqual(run("j"), (1 + math.sqrt(5)) / 2)

    def test_TC0704_pi_in_expression(self):
        self.assertAlmostEqual(run("p 2 *"), 2 * math.pi)

    def test_TC0705_e_in_ln(self):
        self.assertAlmostEqual(run("e ln"), 1.0)


# ===========================================================================
# TC-08  Expresiones encadenadas (casos de uso reales)
# ===========================================================================
class TC08_RealWorldExpressions(unittest.TestCase):
    """
    Expresiones compuestas que simulan usos reales de la calculadora.
    Ejercitan múltiples operaciones en secuencia y el estado de la pila.

    Casos:
      TC-08-01  Clásico RPN: 5 1 2 + 4 * + 3 -         → 14
      TC-08-02  Hipotenusa: √(3²+4²) = 5
                  3 dup * 4 dup * + sqrt               → 5
      TC-08-03  Celsius → Fahrenheit: 100°C
                  formula: F = C*9/5 + 32
                  100 9 * 5 / 32 +                     → 212
      TC-08-04  Interés compuesto: A = P*(1+r)^n
                  P=1000, r=0.1, n=2 → 1210
                  1000 1 0.1 + 2 yx *                  → 1210
      TC-08-05  Área del círculo: π*r² con r=5
                  p 5 dup * *                           → π*25 ≈ 78.5398
      TC-08-06  Distancia euclídea 2D: √((x2-x1)²+(y2-y1)²)
                  puntos (1,2) y (4,6) → 5
                  4 1 - dup * 6 2 - dup * + sqrt       → 5
      TC-08-07  Uso de memoria en cálculo multi-paso
                  (3+4) guardado, luego (3+4)*2
                  3 4 + sto 00 rcl 00 2 *              → 14
      TC-08-08  Cadena de operaciones con swap
                  10 2 swap /  (= 2/10)                → 0.2
    """

    def test_TC0801_classic_rpn(self):
        self.assertEqual(run("5 1 2 + 4 * + 3 -"), 14)

    def test_TC0802_hypotenuse(self):
        # √(3²+4²) = 5
        self.assertAlmostEqual(run("3 dup * 4 dup * + sqrt"), 5.0)

    def test_TC0803_celsius_to_fahrenheit(self):
        # 100°C → 212°F
        self.assertAlmostEqual(run("100 9 * 5 / 32 +"), 212.0)

    def test_TC0804_compound_interest(self):
        # 1000 * (1.1)^2 = 1210
        self.assertAlmostEqual(run("1000 1 0.1 + 2 yx *"), 1210.0)

    def test_TC0805_circle_area(self):
        # π * 5² ≈ 78.53981
        self.assertAlmostEqual(run("p 5 dup * *"), math.pi * 25, places=5)

    def test_TC0806_euclidean_distance(self):
        # dist((1,2),(4,6)) = √(9+16) = 5
        self.assertAlmostEqual(run("4 1 - dup * 6 2 - dup * + sqrt"), 5.0)

    def test_TC0807_memory_in_multistep(self):
        # Guarda 3+4=7, luego 7*2=14
        self.assertAlmostEqual(run("3 4 + sto 00 rcl 00 2 *"), 14.0)

    def test_TC0808_swap_in_division(self):
        # 10 2 swap /  → 2/10 = 0.2
        self.assertAlmostEqual(run("10 2 swap /"), 0.2)


# ===========================================================================
# TC-09  Formato de salida (format_result)
# ===========================================================================
class TC09_FormatResult(unittest.TestCase):
    """
    Verifica que format_result produce la representación textual esperada,
    eliminando artefactos de punto flotante y suprimiendo decimales
    innecesarios en valores enteros.

    Casos:
      TC-09-01  Entero positivo → "42"  (sin ".0")
      TC-09-02  Entero negativo → "-5"
      TC-09-03  Cero            → "0"
      TC-09-04  Float con artefacto: 0.1+0.2 → "0.3" (no "0.30000…4")
      TC-09-05  Float sin artefacto: 0.25    → "0.25"
      TC-09-06  1/3 no se convierte a entero → contiene "."
    """

    def test_TC0901_integer_positive(self):
        self.assertEqual(format_result(42.0), "42")

    def test_TC0902_integer_negative(self):
        self.assertEqual(format_result(-5.0), "-5")

    def test_TC0903_zero(self):
        self.assertEqual(format_result(0.0), "0")

    def test_TC0904_float_artifact(self):
        # 0.1 + 0.2 en flotante da 0.30000000000000004
        result = 0.1 + 0.2
        self.assertEqual(format_result(result), "0.3")

    def test_TC0905_float_exact(self):
        self.assertEqual(format_result(0.25), "0.25")

    def test_TC0906_repeating_decimal_is_float(self):
        self.assertIn(".", format_result(1/3))


# ===========================================================================
# TC-10  Errores semánticos esperados
# ===========================================================================
class TC10_Errors(unittest.TestCase):
    """
    Verifica que cada condición de error produce RPNError con un mensaje
    que identifica el problema. Se comprueba la presencia de una palabra
    clave en el mensaje (insensible a mayúsculas).

    Casos:
      TC-10-01  Token desconocido                → "inválido"
      TC-10-02  Pila vacía al operar con binaria → "insuficiente"
      TC-10-03  Pila con 1 elemento en binaria   → "insuficiente"
      TC-10-04  Pila vacía en unaria (sqrt)      → "insuficiente"
      TC-10-05  dup sin elementos                → "insuficiente"
      TC-10-06  swap con un solo elemento        → "insuficiente"
      TC-10-07  División por cero con /          → "cero"
      TC-10-08  1/x con cero                     → "cero"
      TC-10-09  sqrt de negativo                 → "negativo"
      TC-10-10  log de cero                      → "positivo"
      TC-10-11  log de negativo                  → "positivo"
      TC-10-12  ln de cero                       → "positivo"
      TC-10-13  ln de negativo                   → "positivo"
      TC-10-14  Pila con 0 elementos al final    → "exactamente 1"
      TC-10-15  Pila con 2 elementos al final    → "exactamente 1"
      TC-10-16  sto sin slot siguiente           → "requiere"
      TC-10-17  rcl sin slot siguiente           → "requiere"
      TC-10-18  Slot fuera de rango (99)         → "inválido"
      TC-10-19  sto con pila vacía               → "insuficiente"
      TC-10-20  Slot con texto no numérico       → "inválido"
    """

    def test_TC1001_unknown_token(self):
        assert_error(self, "3 4 foo", "inválido")

    def test_TC1002_binary_op_empty_stack(self):
        assert_error(self, "+", "insuficiente")

    def test_TC1003_binary_op_one_element(self):
        assert_error(self, "5 +", "insuficiente")

    def test_TC1004_unary_op_empty_stack(self):
        assert_error(self, "sqrt", "insuficiente")

    def test_TC1005_dup_empty_stack(self):
        assert_error(self, "dup", "insuficiente")

    def test_TC1006_swap_one_element(self):
        assert_error(self, "5 swap", "insuficiente")

    def test_TC1007_division_by_zero(self):
        assert_error(self, "3 0 /", "cero")

    def test_TC1008_inv_zero(self):
        assert_error(self, "0 1/x", "cero")

    def test_TC1009_sqrt_negative(self):
        assert_error(self, "-1 sqrt", "negativo")

    def test_TC1010_log_zero(self):
        assert_error(self, "0 log", "positivo")

    def test_TC1011_log_negative(self):
        assert_error(self, "-5 log", "positivo")

    def test_TC1012_ln_zero(self):
        assert_error(self, "0 ln", "positivo")

    def test_TC1013_ln_negative(self):
        assert_error(self, "-5 ln", "positivo")

    def test_TC1014_empty_stack_at_end(self):
        assert_error(self, "5 drop", "exactamente 1")

    def test_TC1015_too_many_values_at_end(self):
        assert_error(self, "3 4", "exactamente 1")

    def test_TC1016_sto_missing_slot(self):
        assert_error(self, "5 sto", "requiere")

    def test_TC1017_rcl_missing_slot(self):
        assert_error(self, "rcl", "requiere")

    def test_TC1018_invalid_slot_number(self):
        assert_error(self, "5 sto 99", "inválido")

    def test_TC1019_sto_empty_stack(self):
        assert_error(self, "sto 01", "insuficiente")

    def test_TC1020_slot_non_numeric_text(self):
        assert_error(self, "5 sto xx", "inválido")


# ===========================================================================
# TC-11  Interfaz CLI (main)
# ===========================================================================
class TC11_CLI(unittest.TestCase):
    """
    Verifica la interfaz de línea de comandos: argumentos posicionales,
    modo stdin y manejo de errores hacia stderr con código de salida 1.

    Casos:
      TC-11-01  Argumentos CLI: resultado correcto en stdout
      TC-11-02  Resultado entero impreso sin decimal
      TC-11-03  Resultado flotante impreso con decimales
      TC-11-04  Error imprime "Error" en stderr
      TC-11-05  Expresión válida por stdin
      TC-11-06  Expresión errónea por stdin imprime error en stderr
    """

    def test_TC1101_cli_args_correct(self):
        out, _ = run_main(["3", "4", "+"])
        self.assertEqual(out, "7")

    def test_TC1102_cli_integer_no_decimal(self):
        out, _ = run_main(["6", "7", "*"])
        self.assertEqual(out, "42")
        self.assertNotIn(".", out)

    def test_TC1103_cli_float_output(self):
        out, _ = run_main(["1", "3", "/"])
        self.assertIn("0.333", out)

    def test_TC1104_cli_error_to_stderr(self):
        out, err = run_main(["3", "0", "/"])
        self.assertEqual(out, "")
        self.assertIn("Error", err)

    def test_TC1105_stdin_valid_expression(self):
        out, _ = run_main([], stdin_text="5 3 +\n")
        self.assertEqual(out, "8")

    def test_TC1106_stdin_error_expression(self):
        out, err = run_main([], stdin_text="bad_token\n")
        self.assertEqual(out, "")
        self.assertIn("Error", err)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main(verbosity=2)