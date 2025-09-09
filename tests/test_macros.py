import subprocess
import sys
import tempfile
from pathlib import Path


def test_function_macros_exec_and_macro_lines():
    with tempfile.TemporaryDirectory() as temp_dir:
        mdl = Path(temp_dir) / "macro_test.mdl"
        mdl.write_text(
            (
                'pack "macrotest" "Macro test" 82;\n'
                'namespace "macro";\n\n'
                'function macro:target {\n'
                '    $say "Hello $(name)"\n'
                '    say "Done";\n'
                '}\n\n'
                'function macro:caller {\n'
                "    exec macro:target '{name:\"purple elephant\"}';\n"
                '    exec macro:target with storage macro:ctx data.args;\n'
                '}\n'
            )
        )

        out_dir = Path(temp_dir) / "out"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "minecraft_datapack_language.cli",
                "build",
                "--mdl",
                str(mdl),
                "-o",
                str(out_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

        # Find target and caller mcfunction files regardless of singular/plural folder name
        target_files = list(out_dir.glob("data/macro/**/target.mcfunction"))
        caller_files = list(out_dir.glob("data/macro/**/caller.mcfunction"))
        assert target_files, f"target.mcfunction not found in {out_dir!s}"
        assert caller_files, f"caller.mcfunction not found in {out_dir!s}"

        target_content = target_files[0].read_text()
        caller_content = caller_files[0].read_text()

        # Macro line should be preserved verbatim
        assert "$say \"Hello $(name)\"" in target_content
        # Ensure there is no whitespace between '$' and the command token anywhere
        assert "$ say" not in target_content
        # Exec with inline JSON compound
        assert "function macro:target {name:\"purple elephant\"}" in caller_content
        # Exec with data source 'with' clause
        assert "function macro:target with storage macro:ctx data.args" in caller_content


