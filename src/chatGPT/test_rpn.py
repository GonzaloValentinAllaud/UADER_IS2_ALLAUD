import unittest, math, sys, io
from rpn import RPN, RPNError

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def run(expr):
    return RPN().run(expr)

# ---------------------------------------------------------------------------
# 1. Números y constantes
# ---------------------------------------------------------------------------
class TestNumbers(unittest.TestCase):

    def test_integer(self):
        self.assertEqual(run("42"), 42)

    def test_negative(self):
        self.assertEqual(run("-4"), -4)

    def test_float(self):
        self.assertAlmostEqual(run("2.5"), 2.5)

    def test_constant_pi(self):
        self.assertAlmostEqual(run("p"), math.pi)

    def test_constant_e(self):
        self.assertAlmostEqual(run("e"), math.e)

    def test_constant_phi(self):
        self.assertAlmostEqual(run("j"), (1 + 5**0.5) / 2)

# ---------------------------------------------------------------------------
# 2. Operaciones básicas
# ---------------------------------------------------------------------------
class TestBasicOps(unittest.TestCase):

    def test_add(self):
        self.assertEqual(run("3 4 +"), 7)

    def test_subtract(self):
        self.assertEqual(run("10 3 -"), 7)

    def test_multiply(self):
        self.assertEqual(run("3 4 *"), 12)

    def test_divide(self):
        self.assertAlmostEqual(run("10 4 /"), 2.5)

    def test_chain(self):
        self.assertEqual(run("5 1 2 + 4 * + 3 -"), 14)

    def test_chain2(self):
        self.assertEqual(run("2 3 4 * +"), 14)

    def test_float_ops(self):
        self.assertAlmostEqual(run("1.5 2.5 +"), 4.0)

    def test_negative_operands(self):
        self.assertAlmostEqual(run("-3 -4 *"), 12)

# ---------------------------------------------------------------------------
# 3. Funciones matemáticas
# ---------------------------------------------------------------------------
class TestMathFunctions(unittest.TestCase):

    def test_sqrt(self):
        self.assertAlmostEqual(run("9 sqrt"), 3.0)

    def test_log(self):
        self.assertAlmostEqual(run("100 log"), 2.0)

    def test_ln(self):
        self.assertAlmostEqual(run("1 ln"), 0.0)

    def test_ex(self):
        self.assertAlmostEqual(run("1 ex"), math.e)

    def test_10x(self):
        self.assertAlmostEqual(run("2 10x"), 100.0)

    def test_yx(self):
        self.assertAlmostEqual(run("2 10 yx"), 1024.0)

    def test_inv(self):
        self.assertAlmostEqual(run("4 1/x"), 0.25)

    def test_chs(self):
        self.assertAlmostEqual(run("5 chs"), -5.0)

    def test_chs_negative(self):
        self.assertAlmostEqual(run("-3 chs"), 3.0)

# ---------------------------------------------------------------------------
# 4. Trigonometría (grados)
# ---------------------------------------------------------------------------
class TestTrig(unittest.TestCase):

    def test_sin_90(self):
        self.assertAlmostEqual(run("90 sin"), 1.0)

    def test_cos_0(self):
        self.assertAlmostEqual(run("0 cos"), 1.0)

    def test_tg_45(self):
        self.assertAlmostEqual(run("45 tg"), 1.0)

    def test_asin(self):
        self.assertAlmostEqual(run("1 asin"), 90.0)

    def test_acos(self):
        self.assertAlmostEqual(run("1 acos"), 0.0)

    def test_atg(self):
        self.assertAlmostEqual(run("1 atg"), 45.0)

# ---------------------------------------------------------------------------
# 5. Comandos de pila
# ---------------------------------------------------------------------------
class TestStackCommands(unittest.TestCase):

    def test_dup(self):
        self.assertEqual(run("3 dup +"), 6)

    def test_swap(self):
        self.assertAlmostEqual(run("10 3 swap -"), -7)

    def test_drop(self):
        self.assertEqual(run("5 99 drop"), 5)

    def test_clear_then_push(self):
        self.assertEqual(run("9 8 7 clear 42"), 42)

# ---------------------------------------------------------------------------
# 6. Memoria STO / RCL
# ---------------------------------------------------------------------------
class TestMemory(unittest.TestCase):

    def test_sto_and_rcl(self):
        self.assertEqual(run("42 sto 05 8 rcl 05 +"), 50)

    def test_rcl_default_zero(self):
        self.assertAlmostEqual(run("rcl 00"), 0.0)

    def test_all_slots(self):
        for i in range(10):
            slot = f"{i:02d}"
            val  = float(i * 3)
            rpn  = RPN()
            # sto consume el valor; lo guardamos directamente en la memoria
            rpn.m[slot] = val
            result = rpn.run(f"rcl {slot}")
            self.assertAlmostEqual(result, val)

    def test_overwrite_slot(self):
        self.assertAlmostEqual(run("10 sto 01 20 sto 01 rcl 01"), 20)

# ---------------------------------------------------------------------------
# 7. Condiciones de error — todas con try/except
# ---------------------------------------------------------------------------
class TestErrors(unittest.TestCase):

    # a) Token inválido
    def test_invalid_token(self):
        try:
            run("3 4 foo")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("inválido", str(e).lower())

    # b) Pila insuficiente — operación binaria
    def test_stack_underflow_binary(self):
        try:
            run("3 +")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("insuficiente", str(e).lower())

    # b) Pila insuficiente — operación unaria
    def test_stack_underflow_unary(self):
        try:
            run("sqrt")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("insuficiente", str(e).lower())

    # b) Pila insuficiente — dup sin elementos
    def test_stack_underflow_dup(self):
        try:
            run("dup")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("insuficiente", str(e).lower())

    # b) Pila insuficiente — swap con un solo elemento
    def test_stack_underflow_swap(self):
        try:
            run("5 swap")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("insuficiente", str(e).lower())

    # c) División por cero con /
    def test_division_by_zero(self):
        try:
            run("3 0 /")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("cero", str(e).lower())

    # c) División por cero con 1/x
    def test_inv_by_zero(self):
        try:
            run("0 1/x")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("cero", str(e).lower())

    # d) Demasiados valores en la pila al final
    def test_too_many_values(self):
        try:
            run("3 4")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("exactamente 1", str(e).lower())

    # d) Pila vacía al final
    def test_empty_stack_at_end(self):
        try:
            run("5 drop")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("exactamente 1", str(e).lower())

    # sqrt de negativo
    def test_sqrt_negative(self):
        try:
            run("-1 sqrt")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("negativo", str(e).lower())

    # log de no-positivo
    def test_log_non_positive(self):
        try:
            run("0 log")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("positivo", str(e).lower())

    # ln de no-positivo
    def test_ln_non_positive(self):
        try:
            run("-5 ln")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("positivo", str(e).lower())

    # sto sin slot a continuación
    def test_sto_missing_slot(self):
        try:
            run("5 sto")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("requiere", str(e).lower())

    # rcl sin slot a continuación
    def test_rcl_missing_slot(self):
        try:
            run("rcl")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("requiere", str(e).lower())

    # slot fuera de rango
    def test_invalid_slot(self):
        try:
            run("5 sto 99")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("inválido", str(e).lower())

    # sto con pila vacía
    def test_sto_empty_stack(self):
        try:
            run("sto 01")
            self.fail("Debería haber lanzado RPNError")
        except RPNError as e:
            self.assertIn("insuficiente", str(e).lower())

# ---------------------------------------------------------------------------
# 8. main() — captura stdout/stderr
# ---------------------------------------------------------------------------
class TestMain(unittest.TestCase):

    def _run_main(self, args, stdin_text=None):
        from rpn import main
        old_argv  = sys.argv
        sys.argv  = ["rpn.py"] + args
        out, err  = io.StringIO(), io.StringIO()
        old_out, old_err, old_in = sys.stdout, sys.stderr, sys.stdin
        sys.stdout = out
        sys.stderr = err
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

    def test_main_ok(self):
        out, _ = self._run_main(["3", "4", "+"])
        self.assertEqual(out, "7")

    def test_main_float_result(self):
        out, _ = self._run_main(["1", "3", "/"])
        self.assertIn("0.333", out)

    def test_main_error(self):
        _, err = self._run_main(["3", "0", "/"])
        self.assertIn("Error", err)

    def test_main_stdin(self):
        out, _ = self._run_main([], stdin_text="5 3 +\n")
        self.assertEqual(out, "8")


if __name__ == "__main__":
    unittest.main(verbosity=2)