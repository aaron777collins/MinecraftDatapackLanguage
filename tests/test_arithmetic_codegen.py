import os
import re
import pytest
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler
from minecraft_datapack_language.mdl_errors import MDLCompilerError

def compile_snippet(src: str, outdir: str):
    parser = MDLParser("test.mdl")
    program = parser.parse(src)
    compiler = MDLCompiler(output_dir=outdir)
    return compiler.compile(program, source_dir=outdir)

def test_add_remove_literal(tmp_path):
    src = '''
pack "p" "d" 82;
namespace "p";
function p:f {
    var x<@s> = 1;
    x<@s> = $x<@s>$ + 5;
    x<@s> = $x<@s>$ + -3;
}
'''
    out = compile_snippet(src, str(tmp_path))
    # find function file under either 'functions' or 'function'
    candidates = [
        os.path.join(out, "data", "p", "functions", "f.mcfunction"),
        os.path.join(out, "data", "p", "function", "f.mcfunction"),
    ]
    for fn in candidates:
        if os.path.exists(fn):
            break
    else:
        raise FileNotFoundError("f.mcfunction not found in expected directories")
    text = open(fn, "r", encoding="utf-8").read()
    # We compile via temps: expect add/remove on a temp variable, not directly on x
    # Look for add/remove on any objective used as temp or x
    assert re.search(r"players add @s (temp_\\d+|x) 5", text) is not None or re.search(r"players add @s .* 5", text) is not None
    assert re.search(r"players (remove|add) @s (temp_\\d+|x) 3", text) is not None or re.search(r"players (remove|add) @s .* 3", text) is not None

def test_multiply_divide_literal(tmp_path):
    src = '''
pack "p" "d" 82;
namespace "p";
function p:f {
    var x<@s> = 2;
    x<@s> = $x<@s>$ * 3;
    x<@s> = $x<@s>$ * -1;
    x<@s> = $x<@s>$ / 2;
}
'''
    out = compile_snippet(src, str(tmp_path))
    candidates = [
        os.path.join(out, "data", "p", "functions", "f.mcfunction"),
        os.path.join(out, "data", "p", "function", "f.mcfunction"),
    ]
    for fn in candidates:
        if os.path.exists(fn):
            break
    else:
        raise FileNotFoundError("f.mcfunction not found in expected directories")
    text = open(fn, "r", encoding="utf-8").read()
    # Accept legacy multiply/divide forms or the new operation with temp constants
    legacy_mul = re.search(r"players multiply @s (temp_\\d+|x) 3", text) or re.search(r"players multiply @s .* 3", text)
    legacy_div = re.search(r"players divide @s (temp_\\d+|x) 2", text) or re.search(r"players divide @s .* 2", text)
    # Accept presence of operation with temp constant even if we don't explicitly match the prior set
    op_mul = re.search(r"players operation @s (temp_\\d+|x) \\*= @s temp_\\d+", text) or re.search(r"players operation @s x = @s temp_\\d+", text)
    op_div = re.search(r"players operation @s (temp_\\d+|x) /= @s temp_\\d+", text)
    assert legacy_mul or op_mul
    assert legacy_div or op_div

def test_divide_by_zero_error(tmp_path):
    src = '''
pack "p" "d" 82;
namespace "p";
function p:f {
    var x<@s> = 2;
    x<@s> = $x<@s>$ / 0;
}
'''
    with pytest.raises(MDLCompilerError) as ei:
        compile_snippet(src, str(tmp_path))
    msg = str(ei.value).lower()
    assert ("divide" in msg) or ("division" in msg) or ("integer" in msg)


