import subprocess
import sys
from pathlib import Path


def test_build_macros_example(tmp_path: Path):
    # Build the macros example shipped in the repo
    proj_root = Path(__file__).resolve().parents[1]
    example = proj_root / "examples" / "macros_example.mdl"
    assert example.exists()

    out_dir = tmp_path / "out"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "minecraft_datapack_language.cli",
            "build",
            "--mdl",
            str(example),
            "-o",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    target_files = list(out_dir.glob("data/macros_ex/**/greeter.mcfunction"))
    runner_files = list(out_dir.glob("data/macros_ex/**/runner.mcfunction"))
    assert target_files, "greeter.mcfunction not found"
    assert runner_files, "runner.mcfunction not found"

    greeter = target_files[0].read_text()
    runner = runner_files[0].read_text()

    # Macro line should be present as raw
    assert '$say "Hello $(name)"' in greeter
    # Both exec forms should be emitted
    assert 'function macros_ex:greeter {name:"Casey"}' in runner
    assert 'function macros_ex:greeter with storage macros_ex:ctx player.profile' in runner


