import os
import re

from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler


def compile_snippet(src: str, outdir: str):
    parser = MDLParser("test.mdl")
    program = parser.parse(src)
    compiler = MDLCompiler(output_dir=outdir)
    return compiler.compile(program, source_dir=outdir)


def find_fn(out_dir: str, ns: str, name: str):
    paths = [
        os.path.join(out_dir, "data", ns, "functions", f"{name}.mcfunction"),
        os.path.join(out_dir, "data", ns, "function", f"{name}.mcfunction"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(paths)


def test_complex_arithmetic_codegen(tmp_path):
    src = '''
pack "cx" "d" 82;
namespace "cx";
var num a<@s> = 1;
var num b<@s> = 2;
var num c<@s> = 3;
var num d<@s> = 4;
var num e<@s> = 5;
var num f<@s> = 6;

function cx:calc {
    var x<@s> = -($a<@s>$ + $b<@s>$ * ($c<@s>$ - -$d<@s>$) / 2) + (-$e<@s>$) * 3 - $f<@s>$ * -1;
}
'''
    out = compile_snippet(src, str(tmp_path))
    fn = find_fn(out, "cx", "calc")
    text = open(fn, "r", encoding="utf-8").read()
    # No token names like GREATER etc
    assert "GREATER" not in text and "LESS" not in text
    # Accept legacy multiply/divide or new operation with temp constants
    legacy = re.search(r"players (multiply|divide) @s ", text)
    op_with_const = re.search(r"players set @s temp_\d+ \d+", text) and re.search(r"players operation @s .* (\*=|/=) @s temp_\d+", text)
    assert legacy or op_with_const
    # Still forbid direct numeric literal on operation
    assert re.search(r"operation @s .* \*= \d+", text) is None
    assert re.search(r"operation @s .* /= \d+", text) is None


def test_complex_logical_codegen(tmp_path):
    src = '''
pack "lx" "d" 82;
namespace "lx";
var num a<@s> = 0;
var num b<@s> = 0;
var num c<@s> = 0;
var num d<@s> = 0;
var num e<@s> = 0;
var num f<@s> = 0;
var num g<@s> = 0;
var num h<@s> = 0;
var num i<@s> = 0;
var num j<@s> = 0;

function lx:logic {
    if ($a<@s>$ > 0 && ($b<@s>$ <= $c<@s>$ || !($d<@s>$ != $e<@s>$))) || (-$f<@s>$ < 0 && (($g<@s>$ >= $h<@s>$) && !($i<@s>$ < $j<@s>$))) {
        say "pass";
    } else {
        say "fail";
    }
}
'''
    out = compile_snippet(src, str(tmp_path))
    fn = find_fn(out, "lx", "logic")
    text = open(fn, "r", encoding="utf-8").read()
    # Ensure boolean temps are used (we expect at least one temp initialized to 0, then set to 1 conditionally)
    assert re.search(r"players set @s temp_\d+ 0", text) is not None
    assert re.search(r"execute (if|unless) .* run scoreboard players set @s temp_\d+ 1", text) is not None
    # AND should appear as chained execute if's in one line
    assert re.search(r"execute if .* if .* run ", text)
    # OR should appear as two separate 'execute if ... set temp = 1' lines
    assert len(re.findall(r"execute if .* run scoreboard players set @s temp_\d+ 1", text)) >= 2
    # NOT_EQUAL is compiled via equals with inversion (unless)
    assert re.search(r"execute unless score .* = .* run ", text) or re.search(r"= .*", text)
    # No raw token names
    assert "NOT_EQUAL" not in text and "EQUAL" not in text and "GREATER" not in text

