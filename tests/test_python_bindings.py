from pathlib import Path
import tempfile

from minecraft_datapack_language import Pack
from minecraft_datapack_language.python_api import num, var_read, binop


def test_bindings_control_flow_and_vars():
    p = Pack("Bindings", "desc", 82)
    ns = p.namespace("game")

    def build(fb):
        fb.declare_var("counter", "<@s>", 0)
        fb.set("counter", "<@s>", binop(var_read("counter", "<@s>"), "PLUS", num(1)))
        cond = binop(var_read("counter", "<@s>"), "GREATER", num(0))
        fb.if_(cond, lambda t: t.say("gt0"), lambda e: e.say("le0"))
        wcond = binop(var_read("counter", "<@s>"), "LESS", num(2))
        fb.while_(wcond, lambda b: b.set("counter", "<@s>", binop(var_read("counter", "<@s>"), "PLUS", num(1))))

    ns.function("main", build)

    with tempfile.TemporaryDirectory() as td:
        p.build(td)
        func = Path(td) / 'data' / 'game' / 'function'
        # Expect generated sub-functions
        assert (func / 'main__if_1.mcfunction').exists()
        assert (func / 'main__else_1.mcfunction').exists()
        assert (func / 'main__while_1.mcfunction').exists()
        main = (func / 'main.mcfunction').read_text()
        assert 'execute if score @s counter matches 1.. run function game:main__if_1' in main
        assert 'function game:main__while_1' in main


def test_bindings_complex_expression():
    p = Pack("Bindings2", "desc", 82)
    ns = p.namespace("calc")

    def build(fb):
        fb.declare_var("x", "<@s>", 2)
        fb.declare_var("y", "<@s>", 3)
        expr = binop(
            binop(var_read("x", "<@s>"), "PLUS", num(5)),
            "MULTIPLY",
            binop(var_read("y", "<@s>"), "MINUS", num(1)),
        )
        expr = binop(expr, "DIVIDE", num(2))
        fb.set("x", "<@s>", expr)

    ns.function("math", build)

    with tempfile.TemporaryDirectory() as td:
        p.build(td)
        func = Path(td) / 'data' / 'calc' / 'function'
        text = (func / 'math.mcfunction').read_text()
        assert 'scoreboard players operation @s x = @s temp_' in text
        # Temp ops are inlined now; footer removed
        assert 'temp_' in text


def test_bindings_equality_and_inequality_symbols():
    p = Pack("Bindings3", "desc", 82)
    ns = p.namespace("cmp")

    def build(fb):
        fb.declare_var("a", "<@s>", 1)
        fb.declare_var("b", "<@s>", 1)
        # Use symbol operators that previously leaked into output
        cond_eq = binop(var_read("a", "<@s>"), "==", var_read("b", "<@s>"))
        fb.if_(cond_eq, lambda t: t.say("eq"), lambda e: e.say("neq"))
        cond_ne = binop(var_read("a", "<@s>"), "!=", var_read("b", "<@s>"))
        fb.if_(cond_ne, lambda t: t.say("ne_true"), lambda e: e.say("ne_false"))

    ns.function("main", build)

    with tempfile.TemporaryDirectory() as td:
        p.build(td)
        func = Path(td) / 'data' / 'cmp' / 'function'
        main = (func / 'main.mcfunction').read_text()
        # Equality should map to '=' and inequality should invert the execute
        assert 'execute if score @s a = @s b' in main
        assert 'execute unless score @s a = @s b' in main
        # Ensure invalid raw operators are not present
        assert '==' not in main
        assert '!=' not in main


def test_bindings_equality_literal_and_not_equal_word():
    p = Pack("Bindings4", "desc", 82)
    ns = p.namespace("lit")

    def build(fb):
        fb.declare_var("x", "<@s>", 5)
        # Symbol equality against literal and word-form NOT_EQUAL
        cond_eq = binop(var_read("x", "<@s>"), "==", num(5))
        fb.if_(cond_eq, lambda t: t.say("is5"))
        cond_ne = binop(var_read("x", "<@s>"), "NOT_EQUAL", num(7))
        fb.if_(cond_ne, lambda t: t.say("not7"))

    ns.function("main", build)

    with tempfile.TemporaryDirectory() as td:
        p.build(td)
        func = Path(td) / 'data' / 'lit' / 'function'
        main = (func / 'main.mcfunction').read_text()
        # Equality to literal uses matches N
        assert 'execute if score @s x matches 5' in main
        # Not equal to literal uses unless matches N
        assert 'execute unless score @s x matches 7' in main
        # Ensure invalid raw operators are not present
        assert '==' not in main
        assert '!=' not in main