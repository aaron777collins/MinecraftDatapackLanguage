import tempfile
from pathlib import Path

from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler


def compile_source(source: str):
    parser = MDLParser()
    ast = parser.parse(source)
    tmpdir = tempfile.TemporaryDirectory()
    out = Path(tmpdir.name)
    MDLCompiler().compile(ast, str(out))
    return out, tmpdir


def test_generated_if_function_names_unique_per_parent():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num a = 0;\n'  # default to <@s>
        'function ns:f1 { if $a$ > 1 { say "hi"; } }\n'
        'function ns:f2 { if $a$ > 1 { say "hi2"; } }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'

    # Distinct generated subfunctions
    assert (func_dir / 'f1__if_1.mcfunction').exists()
    assert (func_dir / 'f2__if_1.mcfunction').exists()

    f1 = (func_dir / 'f1.mcfunction').read_text()
    f2 = (func_dir / 'f2.mcfunction').read_text()
    assert 'execute if score @s a matches 2.. run function ns:f1__if_1' in f1
    assert 'execute if score @s a matches 2.. run function ns:f2__if_1' in f2


def test_while_loop_generates_recursive_function_and_condition():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num c = 0;\n'
        'function ns:loop { while $c$ < 3 { c = $c$ + 1; } }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'

    # Main calls the while function
    loop_main = (func_dir / 'loop.mcfunction').read_text()
    assert 'function ns:loop__while_1' in loop_main

    # While body recurses while condition holds
    loop_body = (func_dir / 'loop__while_1.mcfunction').read_text()
    assert 'execute if score @s c matches ..2 run function ns:loop__while_1' in loop_body


def test_complex_expression_temp_operations_present():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num x = 2;\n'
        'var num y = 3;\n'
        'function ns:math { x = ($x$ + 5) * ($y$ - 1) / 2; }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'

    math = (func_dir / 'math.mcfunction').read_text()
    # Assigned from temp
    assert 'scoreboard players operation @s x = @s temp_' in math
    # Temp ops are now inlined directly within function bodies
    assert 'scoreboard players add @s temp_' in math or '+= ' in math
    assert 'scoreboard players remove @s temp_' in math or '-= ' in math
    assert ('scoreboard players multiply @s temp_' in math) or ('*= ' in math)
    assert ('scoreboard players divide @s temp_' in math) or ('/= ' in math)


def test_else_branch_written_separately():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num a = 0;\n'
        'function ns:f { if $a$ > 1 { say "high"; } else { say "low"; } }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'

    # Else file exists and contains the else body
    else_files = sorted(func_dir.glob('f__else_*.mcfunction'))
    assert else_files, 'Expected generated else function file for f'
    content = else_files[0].read_text()
    assert 'tellraw @a {"text":"low"}' in content


