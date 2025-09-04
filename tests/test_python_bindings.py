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
        assert '# Temporary variable operations:' in text

