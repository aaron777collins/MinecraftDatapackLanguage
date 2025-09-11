#!/usr/bin/env python3
"""
MDL CLI - Command Line Interface for Minecraft Datapack Language
"""

import argparse
import sys
import os
from pathlib import Path
import shutil
from typing import Optional
try:
    # Python 3.9+
    from importlib.resources import files as importlib_resources_files
except Exception:  # pragma: no cover
    import importlib_resources  # type: ignore
    importlib_resources_files = importlib_resources.files  # type: ignore
from .mdl_lexer import MDLLexer
from .mdl_parser import MDLParser
from .mdl_compiler import MDLCompiler
from .mdl_errors import MDLLexerError, MDLParserError, MDLCompilerError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MDL (Minecraft Datapack Language) - Compile MDL files to Minecraft datapacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mdl build                                 # Build all MDL files in current directory (to ./dist)
  mdl build --mdl main.mdl                  # Build a single MDL file (to ./dist)
  mdl build -o out                          # Build current directory to custom output
  mdl check                                 # Check all .mdl files in current directory
  mdl check main.mdl                        # Check a single file
  mdl new my_project                        # Create a new project
        """
    )
    # Global options
    parser.add_argument('--version', action='store_true', help='Show version and exit')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build MDL files into a datapack')
    build_parser.add_argument('--mdl', default='.', help='MDL file(s) or directory to build (default: .)')
    build_parser.add_argument('-o', '--output', default='dist', help='Output directory for the datapack (default: dist)')
    build_parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    build_parser.add_argument('--wrapper', help='Optional wrapper directory name for the datapack output')
    build_parser.add_argument('--no-zip', action='store_true', help='Do not create a zip archive (zip is created by default)')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check MDL files for syntax errors')
    check_parser.add_argument('files', nargs='*', help='MDL files or directories to check (default: current directory)')
    check_parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    
    # New command
    new_parser = subparsers.add_parser('new', help='Create a new MDL project')
    new_parser.add_argument('project_name', help='Name of the new project')
    new_parser.add_argument('--pack-name', help='Custom name for the datapack')
    new_parser.add_argument('--pack-format', type=int, default=82, help='Pack format number (default: 82)')
    new_parser.add_argument('--output', help='Directory to create the project in (defaults to current directory)')
    new_parser.add_argument('--exclude-local-docs', action='store_true', help='Do not copy packaged docs into the project')

    # Completion command
    completion_parser = subparsers.add_parser('completion', help='Shell completion utilities')
    completion_sub = completion_parser.add_subparsers(dest='completion_cmd', help='Completion subcommands')
    comp_print = completion_sub.add_parser('print', help='Print completion script for a shell')
    comp_print.add_argument('shell', nargs='?', choices=['bash', 'zsh', 'fish', 'powershell'], help='Target shell (default: auto-detect)')
    comp_install = completion_sub.add_parser('install', help='Install completion for current user shell')
    comp_install.add_argument('shell', nargs='?', choices=['bash', 'zsh', 'fish', 'powershell'], help='Target shell (default: auto-detect)')
    comp_uninstall = completion_sub.add_parser('uninstall', help='Uninstall completion from current user shell')
    comp_uninstall.add_argument('shell', nargs='?', choices=['bash', 'zsh', 'fish', 'powershell'], help='Target shell (default: auto-detect)')
    completion_sub.add_parser('doctor', help='Diagnose completion install status')

    # Docs command
    docs_parser = subparsers.add_parser('docs', help='Open or serve docs')
    docs_sub = docs_parser.add_subparsers(dest='docs_cmd', help='Docs subcommands')
    docs_sub.add_parser('open', help='Open the MDL Getting Started docs in your browser')
    docs_serve = docs_sub.add_parser('serve', help='Serve project docs locally')
    docs_serve.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    docs_serve.add_argument('--dir', default='docs', help='Docs directory to serve (default: docs)')
    
    args = parser.parse_args()
    
    if args.version and not args.command:
        # Print version and exit
        try:
            from . import __version__
        except Exception:
            __version__ = "0.0.0"
        print(__version__)
        return 0

    if not args.command:
        parser.print_help()
        print("")
        print("Tip: Create a new project with: mdl new <project_name>")
        print("     Then open the Getting Started guide in your browser: mdl docs")
        return 0
    
    try:
        if args.command == 'build':
            return build_command(args)
        elif args.command == 'check':
            return check_command(args)
        elif args.command == 'new':
            return new_command(args)
        elif args.command == 'completion':
            return completion_command(args)
        elif args.command == 'docs':
            return docs_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def build_command(args):
    """Build MDL files into a datapack."""
    mdl_path = Path(args.mdl)
    output_dir = Path(args.output)
    
    if not mdl_path.exists():
        print(f"Error: MDL path '{mdl_path}' does not exist")
        return 1
    
    # Determine what to build
    if mdl_path.is_file():
        mdl_files = [mdl_path]
    elif mdl_path.is_dir():
        mdl_files = list(mdl_path.glob("**/*.mdl"))
        if not mdl_files:
            print(f"Error: No .mdl files found in directory '{mdl_path}'")
            return 1
    else:
        print(f"Error: Invalid MDL path '{mdl_path}'")
        return 1
    
    if args.verbose:
        print(f"Building {len(mdl_files)} MDL file(s)...")
        for f in mdl_files:
            print(f"  {f}")
    
    # Parse and compile each file
    all_asts = []
    for mdl_file in mdl_files:
        try:
            with open(mdl_file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            if args.verbose:
                print(f"Parsing {mdl_file}...")
            
            parser = MDLParser(str(mdl_file))
            ast = parser.parse(source)
            all_asts.append(ast)
            # Indicate per-file success
            print(f"[OK] {mdl_file}")
            
        except (MDLLexerError, MDLParserError) as e:
            print(f"Error in {mdl_file}: {e}")
            return 1
    
    # Merge all ASTs if multiple files
    if len(all_asts) == 1:
        final_ast = all_asts[0]
    else:
        # Merge multiple ASTs
        final_ast = all_asts[0]
        for ast in all_asts[1:]:
            final_ast.variables.extend(ast.variables)
            final_ast.functions.extend(ast.functions)
            final_ast.tags.extend(ast.tags)
            final_ast.hooks.extend(ast.hooks)
            final_ast.statements.extend(ast.statements)
    
    # Compile
    try:
        if args.verbose:
            print(f"Compiling to {output_dir}...")
        
        # Support optional wrapper directory
        if getattr(args, 'wrapper', None):
            output_dir = output_dir / args.wrapper
        compiler = MDLCompiler()
        output_path = compiler.compile(final_ast, str(output_dir))

        # Zip the datapack by default unless disabled
        if not getattr(args, 'no_zip', False):
            base_name = str(Path(output_path))
            # Create archive next to the output directory (base_name.zip)
            archive_path = shutil.make_archive(base_name, 'zip', root_dir=str(Path(output_path)))
            if args.verbose:
                print(f"Created archive: {archive_path}")
        
        print(f"Successfully built datapack: {output_path}")
        return 0
        
    except MDLCompilerError as e:
        print(f"Compilation error: {e}")
        return 1


def check_command(args):
    """Check MDL files for syntax errors."""
    all_errors = []

    # If no files provided, default to scanning current directory
    input_paths = args.files if getattr(args, 'files', None) else ['.']

    # Collect .mdl files from provided files/directories
    mdl_files = []
    for input_path in input_paths:
        path_obj = Path(input_path)
        if path_obj.is_dir():
            mdl_files.extend(path_obj.glob('**/*.mdl'))
        elif path_obj.is_file():
            if path_obj.suffix.lower() == '.mdl':
                mdl_files.append(path_obj)
        else:
            print(f"Error: Path '{path_obj}' does not exist")

    if not mdl_files:
        print("Error: No .mdl files found to check")
        return 1

    for file_path in mdl_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            if args.verbose:
                print(f"Checking {file_path}...")

            # Lex and parse to check for errors
            lexer = MDLLexer(str(file_path))
            tokens = list(lexer.lex(source))

            parser = MDLParser(str(file_path))
            ast = parser.parse(source)

            if args.verbose:
                print(f"  ✓ {file_path} - {len(ast.functions)} functions, {len(ast.variables)} variables")
            # Indicate per-file success
            print(f"[OK] {file_path}")

        except MDLLexerError as e:
            print(f"Lexer error in {file_path}: {e}")
            all_errors.append(e)
        except MDLParserError as e:
            print(f"Parser error in {file_path}: {e}")
            all_errors.append(e)
        except Exception as e:
            print(f"Unexpected error in {file_path}: {e}")
            all_errors.append(e)

    if all_errors:
        print(f"\nFound {len(all_errors)} error(s)")
        return 1
    else:
        print("All files passed syntax check!")
        return 0


def new_command(args):
    """Create a new MDL project."""
    project_name = args.project_name
    pack_name = args.pack_name or project_name
    pack_format = args.pack_format
    base_dir = Path(args.output) if getattr(args, 'output', None) else Path('.')
    project_dir = base_dir / project_name
    
    # Create project directory
    if project_dir.exists():
        print(f"Error: Project directory '{project_name}' already exists")
        return 1
    
    project_dir.mkdir(parents=True)
    
    # Create main MDL file
    mdl_file = project_dir / f"{project_name}.mdl"
    
    template_content = f'''pack "{pack_name}" "Generated by MDL CLI" {pack_format};
namespace "{project_name}";

function {project_name}:main {{
    say "Hello from {project_name}!";
}}

function {project_name}:init {{
    say "Datapack initialized!";
}}

on_load {project_name}:init;
'''
    
    with open(mdl_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    # Create README
    readme_file = project_dir / "README.md"
    readme_content = f'''# {project_name}

A Minecraft datapack created with MDL (Minecraft Datapack Language).

## Getting Started

1. **Build the datapack:**
   ```bash
   mdl build --mdl {project_name}.mdl -o dist
   ```

2. **Install in Minecraft:**
   - Copy `dist/{project_name}/` to your world's `datapacks/` folder
   - Run `/reload` in-game

3. **Run the main function:**
   ```
   /function {project_name}:main
   ```
'''
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Copy packaged docs unless excluded
    if not getattr(args, 'exclude_local_docs', False):
        try:
            copied = copy_packaged_docs_into(project_dir)
            if copied:
                print(f"  - docs/ (local docs copied)")
            else:
                print(f"  - docs/ (skipped: no embedded docs found)")
        except FileExistsError:
            print("  - docs/ already exists (skipped). Use --exclude-local-docs to suppress this step.")
        except Exception as e:
            print(f"  - docs/ copy failed: {e}")

    # Add simple serve scripts
    try:
        create_docs_serve_scripts(project_dir)
        print("  - serve_docs.sh, serve_docs.ps1")
    except Exception as e:
        print(f"  - serve script creation failed: {e}")

    print(f"Created new MDL project: {project_dir}/")
    print(f"  - {mdl_file}")
    print(f"  - {readme_file}")
    if (project_dir / 'docs').exists():
        print("  - docs/ (local docs)")
    if (project_dir / 'docs_site').exists():
        print("  - docs_site/ (prebuilt HTML docs)")
    print("  - serve_docs.sh, serve_docs.ps1")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. mdl build --mdl {project_name}.mdl -o dist")
    print(f"  3. Copy dist/{project_name}/ to your Minecraft world's datapacks folder")
    
    return 0


def copy_packaged_docs_into(project_dir: Path) -> bool:
    """Copy embedded docs folder into the given project directory.
    Returns True if copied, False if no embedded docs packaged.
    Raises FileExistsError if destination exists.
    """
    embedded_root = importlib_resources_files("minecraft_datapack_language").joinpath("_embedded", "docs")
    embedded_site = importlib_resources_files("minecraft_datapack_language").joinpath("_embedded", "docs_site")
    try:
        # Some importlib.resources implementations require as_file for files; for dirs, check existence
        if not Path(str(embedded_root)).exists():
            return False
    except Exception:
        return False

    # Copy raw docs
    dest = project_dir / "docs"
    if dest.exists():
        raise FileExistsError("docs directory already exists")
    shutil.copytree(str(embedded_root), str(dest))
    # Copy prebuilt HTML site if available
    try:
        if Path(str(embedded_site)).exists():
            site_dest = project_dir / "docs_site"
            if not site_dest.exists():
                shutil.copytree(str(embedded_site), str(site_dest))
    except Exception:
        pass
    return True


def create_docs_serve_scripts(project_dir: Path) -> None:
    """Create convenience scripts to serve the project's docs."""
    bash_script = project_dir / "serve_docs.sh"
    bash_script.write_text("""#!/usr/bin/env bash
set -e
PORT=${PORT:-8000}
DIR=${1:-}
if [ -z "$DIR" ]; then
  if [ -d docs_site ]; then DIR=docs_site; else DIR=docs; fi
fi
if [ ! -d "$DIR" ]; then
  echo "Error: docs directory '$DIR' not found"; exit 1
fi
# Prefer Jekyll if available and Gemfile exists
if command -v bundle >/dev/null 2>&1 && [ -f "$DIR/Gemfile" ] || [ -f "Gemfile" ]; then
  (cd "$DIR" && bundle exec jekyll serve --livereload --port "$PORT")
else
  (cd "$DIR" && python -m http.server "$PORT")
fi
""", encoding='utf-8')
    try:
        os.chmod(bash_script, 0o755)
    except Exception:
        pass

    ps1_script = project_dir / "serve_docs.ps1"
    ps1_script.write_text("""
param(
  [int]$Port = 8000,
  [string]$Dir = ""
)
if (-not $Dir) { if (Test-Path 'docs_site') { $Dir = 'docs_site' } else { $Dir = 'docs' } }
if (-not (Test-Path $Dir)) { Write-Host "Error: docs directory '$Dir' not found"; exit 1 }
# Prefer Jekyll if available and Gemfile exists
$gemfile = (Test-Path (Join-Path $Dir 'Gemfile')) -or (Test-Path 'Gemfile')
if ($gemfile -and (Get-Command bundle -ErrorAction SilentlyContinue)) {
  Push-Location $Dir
  & bundle exec jekyll serve --livereload --port $Port
  Pop-Location
} else {
  Push-Location $Dir
  python -m http.server $Port
  Pop-Location
}
""", encoding='utf-8')


def completion_command(args) -> int:
    """Handle completion subcommands: print/install/uninstall/doctor."""
    cmd = args.completion_cmd
    if not cmd:
        print("Usage: mdl completion [print|install|uninstall|doctor] [shell]")
        return 1

    shell = getattr(args, 'shell', None)
    if cmd == 'print':
        return print_completion(shell)
    elif cmd == 'install':
        return install_completion(shell)
    elif cmd == 'uninstall':
        return uninstall_completion(shell)
    elif cmd == 'doctor':
        return doctor_completion()
    else:
        print(f"Unknown completion subcommand: {cmd}")
        return 1


def detect_shell() -> str:
    sh = os.environ.get('SHELL', '')
    if 'zsh' in sh:
        return 'zsh'
    if 'bash' in sh:
        return 'bash'
    # Windows PowerShell detection
    if os.name == 'nt' or os.environ.get('ComSpec', '').endswith('cmd.exe'):
        return 'powershell'
    return 'bash'


def _read_completion_text(shell: str) -> Optional[str]:
    base = importlib_resources_files("minecraft_datapack_language").joinpath("completions")
    mapping = {
        'bash': 'mdl.bash',
        'zsh': 'mdl.zsh',
        'fish': 'mdl.fish',
        'powershell': 'mdl.ps1',
    }
    name = mapping.get(shell)
    if not name:
        return None
    path = Path(str(base)) / name
    if not path.exists():
        return None
    return path.read_text(encoding='utf-8')


def print_completion(shell: Optional[str]) -> int:
    sh = shell or detect_shell()
    text = _read_completion_text(sh)
    if not text:
        print(f"No completion script packaged for shell: {sh}")
        return 1
    print(text)
    return 0


def install_completion(shell: Optional[str]) -> int:
    sh = shell or detect_shell()
    text = _read_completion_text(sh)
    if not text:
        print(f"No completion script packaged for shell: {sh}")
        return 1
    home = Path.home()
    target_dir = home / ".mdl" / "completion"
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = {
        'bash': 'mdl.bash',
        'zsh': 'mdl.zsh',
        'fish': 'mdl.fish',
        'powershell': 'mdl.ps1',
    }[sh]
    target_path = target_dir / filename
    target_path.write_text(text, encoding='utf-8')

    if sh == 'bash':
        rc = home / ".bashrc"
        _ensure_line_in_file(rc, f"source {target_path.as_posix()}")
        print(f"Installed bash completion. Restart your shell or 'source {rc}'.")
    elif sh == 'zsh':
        rc = home / ".zshrc"
        _ensure_line_in_file(rc, f"source {target_path.as_posix()}")
        print(f"Installed zsh completion. Restart your shell or 'source {rc}'.")
    elif sh == 'fish':
        fish_dir = home / ".config" / "fish" / "completions"
        fish_dir.mkdir(parents=True, exist_ok=True)
        (fish_dir / "mdl.fish").write_text(text, encoding='utf-8')
        print("Installed fish completion. Restart your shell.")
    elif sh == 'powershell':
        print(f"Saved PowerShell completion to {target_path}. Add this line to your $PROFILE:")
        print(f". {target_path}")
    else:
        print(f"Unknown shell: {sh}")
        return 1
    return 0


def uninstall_completion(shell: Optional[str]) -> int:
    sh = shell or detect_shell()
    home = Path.home()
    target_dir = home / ".mdl" / "completion"
    filename = {
        'bash': 'mdl.bash',
        'zsh': 'mdl.zsh',
        'fish': 'mdl.fish',
        'powershell': 'mdl.ps1',
    }.get(sh)
    if not filename:
        print(f"Unknown shell: {sh}")
        return 1
    try:
        (target_dir / filename).unlink(missing_ok=True)  # type: ignore[arg-type]
    except TypeError:
        # Python < 3.8 fallback
        path = target_dir / filename
        if path.exists():
            path.unlink()
    if sh == 'bash':
        _remove_line_from_file(home / ".bashrc", "source ~/.mdl/completion/mdl.bash")
    elif sh == 'zsh':
        _remove_line_from_file(home / ".zshrc", "source ~/.mdl/completion/mdl.zsh")
    elif sh == 'fish':
        fish_path = home / ".config" / "fish" / "completions" / "mdl.fish"
        if fish_path.exists():
            fish_path.unlink()
    elif sh == 'powershell':
        pass
    print(f"Uninstalled {sh} completion.")
    return 0


def doctor_completion() -> int:
    sh = detect_shell()
    print(f"Detected shell: {sh}")
    print("Check if 'mdl' completion activates after restarting your shell. If not, re-run: 'mdl completion install'.")
    return 0


def _ensure_line_in_file(path: Path, line: str) -> None:
    try:
        if not path.exists():
            path.write_text(f"# Added by MDL CLI\n{line}\n", encoding='utf-8')
            return
        content = path.read_text(encoding='utf-8')
        if line not in content:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"\n{line}\n")
    except Exception:
        pass


def _remove_line_from_file(path: Path, line: str) -> None:
    try:
        if not path.exists():
            return
        lines = path.read_text(encoding='utf-8').splitlines()
        new_lines = [l for l in lines if l.strip() != line.strip()]
        if new_lines != lines:
            path.write_text("\n".join(new_lines) + "\n", encoding='utf-8')
    except Exception:
        pass


def docs_command(args) -> int:
    cmd = args.docs_cmd
    # Default action: open website getting started page
    if cmd is None or cmd == 'open':
        try:
            import webbrowser
            webbrowser.open('https://www.mcmdl.com/docs/getting-started/')
            print("Opened MDL Getting Started in your default browser.")
            return 0
        except Exception as e:
            print(f"Failed to open browser: {e}")
            return 1
    if cmd == 'serve':
        port = getattr(args, 'port', 8000)
        directory = getattr(args, 'dir', 'docs')
        docs_dir = Path(directory)
        if not docs_dir.exists() or not docs_dir.is_dir():
            print(f"Error: docs directory '{docs_dir}' not found")
            return 1
        print(f"Serving docs on http://localhost:{port} from {docs_dir}")
        try:
            # Prefer Jekyll if Gemfile exists and 'bundle' is available
            use_jekyll = (docs_dir / 'Gemfile').exists() or Path('Gemfile').exists()
            has_bundle = shutil.which('bundle') is not None
            if use_jekyll and has_bundle:
                import subprocess
                subprocess.run(['bundle', 'exec', 'jekyll', 'serve', '--livereload', '--port', str(port)], cwd=str(docs_dir), check=True)
                return 0
        except Exception as e:
            print(f"Jekyll serve failed or unavailable: {e}")
            print("Falling back to Python static server.")
        # Fallback to Python HTTP server
        try:
            import http.server
            import socketserver
            os.chdir(str(docs_dir))
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(('', port), handler) as httpd:
                print("Press Ctrl+C to stop...")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")
            return 0
        except Exception as e:
            print(f"Failed to serve docs: {e}")
            return 1
        return 0
    else:
        print("Usage: mdl docs serve [--dir DIR] [--port PORT]")
        return 1


if __name__ == '__main__':
    sys.exit(main())
