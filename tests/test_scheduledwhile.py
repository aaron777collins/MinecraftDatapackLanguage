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


def test_scheduledwhile_generates_schedule_and_helper():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num c<@s> = 0;\n'
        'function ns:loop { scheduledwhile $c<@s>$ < 3 { c<@s> = $c<@s>$ + 1; } }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'

    # Main function schedules the helper for next tick
    loop_main = (func_dir / 'loop.mcfunction').read_text()
    assert 'schedule function ns:loop__while_' in loop_main

    # Helper exists and conditionally reschedules itself
    helper_files = sorted(p for p in func_dir.glob('loop__while_*.mcfunction'))
    assert helper_files, 'Expected generated scheduled helper function file'
    helper = helper_files[0].read_text()
    assert 'execute if score @s c <' in helper or 'execute if score @s c matches ..2' in helper
    assert 'schedule function ns:loop__while_' in helper


def test_scheduledwhile_breaks_out_without_reschedule_when_false():
    src = (
        'pack "ns" "desc" 82;\n'
        'namespace "ns";\n'
        'var num c<@s> = 5;\n'
        'function ns:loop { scheduledwhile $c<@s>$ > 10 { c<@s> = $c<@s>$ + 1; } }\n'
    )
    out, tmp = compile_source(src)
    func_dir = out / 'data' / 'ns' / 'function'
    helper_files = sorted(p for p in func_dir.glob('loop__while_*.mcfunction'))
    assert helper_files, 'Expected generated scheduled helper function file'
    helper = helper_files[0].read_text()
    # For > 10, continue condition is false initially; helper should still only schedule if condition true
    # Verify presence of conditional schedule, not unconditional schedule
    assert 'execute if ' in helper and 'schedule function ns:loop__while_' in helper

