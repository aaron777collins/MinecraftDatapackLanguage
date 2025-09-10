#!/usr/bin/env python3
"""
MDL CLI - Command Line Interface for Minecraft Datapack Language
"""

import argparse
import sys
import os
from pathlib import Path
import shutil
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
        return 1
    
    try:
        if args.command == 'build':
            return build_command(args)
        elif args.command == 'check':
            return check_command(args)
        elif args.command == 'new':
            return new_command(args)
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
    
    print(f"Created new MDL project: {project_dir}/")
    print(f"  - {mdl_file}")
    print(f"  - {readme_file}")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. mdl build --mdl {project_name}.mdl -o dist")
    print(f"  3. Copy dist/{project_name}/ to your Minecraft world's datapacks folder")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
