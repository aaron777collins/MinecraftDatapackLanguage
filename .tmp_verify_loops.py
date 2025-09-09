from pathlib import Path
import tempfile, glob
from minecraft_datapack_language.mdl_parser import MDLParser
from minecraft_datapack_language.mdl_compiler import MDLCompiler

def build(src: str):
    p = MDLParser()
    ast = p.parse(src)
    td = tempfile.TemporaryDirectory()
    out = Path(td.name)
    MDLCompiler().compile(ast, str(out))
    return out

D = '$'
# Regular while
src1 = (
    'pack "ns" "desc" 82;\n'
    'namespace "ns";\n'
    'var num c<@s> = 3;\n'
    'function ns:loop { while ' + D + 'c<@s>' + D + ' > 0 { c<@s> = ' + D + 'c<@s>' + D + ' - 1; } }\n'
)
out1 = build(src1)
main1 = (out1 / 'data' / 'ns' / 'function' / 'loop.mcfunction').read_text()
helper1 = sorted(glob.glob(str(out1 / 'data' / 'ns' / 'function' / 'loop__while_*.mcfunction')))[0]
body1 = Path(helper1).read_text()
print('=== while main ===')
print(main1)
print('=== while helper ===')
print(body1)

# Scheduled while
src2 = (
    'pack "ns" "desc" 82;\n'
    'namespace "ns";\n'
    'var num c<@s> = 0;\n'
    'function ns:loop { scheduledwhile ' + D + 'c<@s>' + D + ' < 2 { c<@s> = ' + D + 'c<@s>' + D + ' + 1; } }\n'
)
out2 = build(src2)
main2 = (out2 / 'data' / 'ns' / 'function' / 'loop.mcfunction').read_text()
helper2 = sorted(glob.glob(str(out2 / 'data' / 'ns' / 'function' / 'loop__while_*.mcfunction')))[0]
body2 = Path(helper2).read_text()
print('=== scheduledwhile main ===')
print(main2)
print('=== scheduledwhile helper ===')
print(body2)
