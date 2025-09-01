"""
MDL CLI - Simplified Minecraft Datapack Language Compiler
Handles basic control structures and number variables only
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .cli_build import build_mdl
from .cli_check import lint_mdl_file_wrapper, lint_mdl_directory_wrapper
from .cli_new import create_new_project
from .cli_help import show_main_help, show_build_help, show_check_help, show_new_help
from .mdl_errors import MDLErrorCollector, create_error, MDLConfigurationError


def main():
    """Main CLI entry point."""
    error_collector = MDLErrorCollector()
    
    try:
        # Check for help requests and determine command first
        has_help = '--help' in sys.argv or '-h' in sys.argv
        
        # Determine which command is being used for help
        help_command = None
        if has_help:
            for i, arg in enumerate(sys.argv[1:], 1):
                if arg in ['build', 'check', 'new']:
                    help_command = arg
                    break
        
        # Handle command-specific help before any parsing
        if has_help and help_command == 'build':
            show_build_help()
            return
        elif has_help and help_command == 'check':
            show_check_help()
            return
        elif has_help and help_command == 'new':
            show_new_help()
            return
        elif has_help:
            # General help request
            show_main_help()
            return
        
        # Create argument parser without built-in help
        parser = argparse.ArgumentParser(
            description="MDL (Minecraft Datapack Language) CLI",
            add_help=False
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Build command
        build_parser = subparsers.add_parser('build', add_help=False)
        build_parser.add_argument('--mdl', '-m', required=True, help='Input MDL file or directory')
        build_parser.add_argument('-o', '--output', required=True, help='Output directory')
        build_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        build_parser.add_argument('--pack-format', type=int, help='Pack format override')
        build_parser.add_argument('--wrapper', help='Create zip file with specified name')
        build_parser.add_argument('--ignore-warnings', action='store_true', help='Suppress warning messages during build')
        
        # Check command
        check_parser = subparsers.add_parser('check', add_help=False)
        check_parser.add_argument('input', help='Input MDL file or directory')
        check_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        check_parser.add_argument('--ignore-warnings', action='store_true', help='Suppress warning messages during check')
        
        # New command
        new_parser = subparsers.add_parser('new', add_help=False)
        new_parser.add_argument('project_name', help='Name for the new project')
        new_parser.add_argument('--pack-name', help='Custom pack name')
        new_parser.add_argument('--pack-format', type=int, default=82, help='Pack format number')
        
        try:
            args = parser.parse_args()
        except SystemExit:
            # Invalid arguments - show help
            show_main_help()
            return
        
        # Process commands
        if args.command == "build":
            try:
                build_mdl(
                    args.mdl, 
                    args.output, 
                    verbose=args.verbose,
                    pack_format_override=args.pack_format,
                    wrapper=args.wrapper,
                    ignore_warnings=args.ignore_warnings
                )
            except Exception as e:
                error_collector.add_error(create_error(
                    MDLConfigurationError,
                    f"Build command failed: {str(e)}",
                    suggestion="Check your arguments and try again."
                ))
        
        elif args.command == "check":
            try:
                input_path = Path(args.input)
                if input_path.is_file():
                    lint_mdl_file_wrapper(args.input, args.verbose, args.ignore_warnings)
                else:
                    lint_mdl_directory_wrapper(args.input, args.verbose, args.ignore_warnings)
            except Exception as e:
                error_collector.add_error(create_error(
                    MDLConfigurationError,
                    f"Check command failed: {str(e)}",
                    suggestion="Check your arguments and try again."
                ))
        
        elif args.command == "new":
            try:
                create_new_project(
                    args.project_name,
                    pack_name=args.pack_name,
                    pack_format=args.pack_format
                )
            except Exception as e:
                error_collector.add_error(create_error(
                    MDLConfigurationError,
                    f"New command failed: {str(e)}",
                    suggestion="Check your arguments and try again."
                ))
        
        elif args.command is None:
            # No command specified - show help
            show_main_help()
            return
        else:
            # Unknown command
            error_collector.add_error(create_error(
                MDLConfigurationError,
                f"Unknown command: {args.command}",
                suggestion="Use 'mdl --help' to see available commands."
            ))
        
        # Print any errors and exit
        error_collector.print_errors(verbose=True, ignore_warnings=False)
        error_collector.raise_if_errors()
    
    except Exception as e:
        error_collector.add_error(create_error(
            MDLConfigurationError,
            f"Unexpected error: {str(e)}",
            suggestion="If this error persists, please report it as a bug."
        ))
        error_collector.print_errors(verbose=True, ignore_warnings=False)
        error_collector.raise_if_errors()


if __name__ == "__main__":
    main()
