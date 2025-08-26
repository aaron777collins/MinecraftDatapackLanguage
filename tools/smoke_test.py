# Simple programmatic smoke test
import os, shutil
from minecraft_datapack_language.mdl_parser import parse_mdl

SRC = '''
pack "Smoke" description "Test" pack_format 48
namespace "demo"
function "hello":
    say hello
on_tick "demo:hello"
'''
p = parse_mdl(SRC, default_pack_format=48)
OUT = "tmp_smoke"
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
p.build(OUT)
assert os.path.exists(os.path.join(OUT, "pack.mcmeta"))
assert os.path.exists(os.path.join(OUT, "data", "demo", "function", "hello.mcfunction"))
print("OK")
