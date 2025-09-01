"""
CLI Check Functions - Validation and error checking for MDL files
"""

import sys
from pathlib import Path
from typing import Optional

from .mdl_errors import MDLErrorCollector, create_error, MDLFileError
from .mdl_linter import lint_mdl_file, lint_mdl_directory


def lint_mdl_file_wrapper(file_path: str, verbose: bool = False, ignore_warnings: bool = False):
    """Wrapper function for linting a single MDL file with error handling."""
    error_collector = MDLErrorCollector()
    
    try:
        path = Path(file_path)
        
        # Validate file exists
        if not path.exists():
            error_collector.add_error(create_error(
                MDLFileError,
                f"File does not exist: {file_path}",
                file_path=file_path,
                suggestion="Check the file path and ensure the file exists."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Validate file is an MDL file
        if path.suffix != '.mdl':
            error_collector.add_error(create_error(
                MDLFileError,
                f"File is not an MDL file: {file_path}",
                file_path=file_path,
                suggestion="Ensure the file has a .mdl extension."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Perform linting
        try:
            issues = lint_mdl_file(str(path))
            
            # Check if there are any errors
            errors = [issue for issue in issues if issue.severity == 'error']
            warnings = [issue for issue in issues if issue.severity == 'warning']
            
            if errors:
                # Report errors
                print(f"[CHECK] Found {len(errors)} error(s) in: {file_path}")
                for i, issue in enumerate(errors, 1):
                    print(f"Error {i}: {issue.message}")
                    if issue.suggestion:
                        print(f"  Suggestion: {issue.suggestion}")
                    if issue.code:
                        print(f"  Code: {issue.code}")
                    print()
                
                # Exit with error code
                sys.exit(1)
            elif warnings and not ignore_warnings:
                # Report warnings
                print(f"[CHECK] Found {len(warnings)} warning(s) in: {file_path}")
                for i, issue in enumerate(warnings, 1):
                    print(f"Warning {i}: {issue.message}")
                    if issue.suggestion:
                        print(f"  Suggestion: {issue.suggestion}")
                    if issue.code:
                        print(f"  Code: {issue.code}")
                    print()
            
            print(f"[CHECK] Successfully checked: {file_path}")
            print("[OK] No errors found!")
        
        except Exception as e:
            error_collector.add_error(create_error(
                MDLFileError,
                f"Error during linting: {str(e)}",
                file_path=file_path,
                suggestion="Check the file syntax and try again."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
    
    except Exception as e:
        error_collector.add_error(create_error(
            MDLFileError,
            f"Unexpected error: {str(e)}",
            file_path=file_path,
            suggestion="Check the file and try again. If the problem persists, report this as a bug."
        ))
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()


def lint_mdl_directory_wrapper(directory_path: str, verbose: bool = False, ignore_warnings: bool = False):
    """Wrapper function for linting a directory of MDL files with error handling."""
    error_collector = MDLErrorCollector()
    
    try:
        directory = Path(directory_path)
        
        # Validate directory exists
        if not directory.exists():
            error_collector.add_error(create_error(
                MDLFileError,
                f"Directory does not exist: {directory_path}",
                file_path=directory_path,
                suggestion="Check the directory path and ensure it exists."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Validate it's a directory
        if not directory.is_dir():
            error_collector.add_error(create_error(
                MDLFileError,
                f"Path is not a directory: {directory_path}",
                file_path=directory_path,
                suggestion="Provide a valid directory path."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
            return
        
        # Perform directory linting
        try:
            lint_mdl_directory(str(directory), verbose)
            print(f"[CHECK] Successfully checked directory: {directory_path}")
            print("[OK] No errors found!")
        
        except Exception as e:
            error_collector.add_error(create_error(
                MDLFileError,
                f"Error during directory linting: {str(e)}",
                file_path=directory_path,
                suggestion="Check the directory contents and try again."
            ))
            error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
    
    except Exception as e:
        error_collector.add_error(create_error(
            MDLFileError,
            f"Unexpected error: {str(e)}",
            file_path=directory_path,
            suggestion="Check the directory and try again. If the problem persists, report this as a bug."
        ))
        error_collector.print_errors(verbose=True, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()
