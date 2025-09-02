"""
CLI Build Module - Handles building MDL files into Minecraft datapacks
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional, List

from .cli_colors import (
    print_success, print_warning, print_error, print_info,
    print_section, print_separator, color
)
from .mdl_errors import MDLErrorCollector, create_error, MDLConfigurationError, MDLFileError
from .pack import MDLPack
from .utils import find_mdl_files


def build_mdl(input_path: str, output_path: str, verbose: bool = False, 
              pack_format_override: Optional[int] = None, wrapper: Optional[str] = None,
              ignore_warnings: bool = False) -> None:
    """Build MDL files into a Minecraft datapack.
    
    Args:
        input_path: Path to MDL file or directory
        output_path: Output directory for the datapack
        verbose: Enable verbose output
        pack_format_override: Override pack format number
        wrapper: Create zip file with specified name
        ignore_warnings: Suppress warning messages
    """
    error_collector = MDLErrorCollector()
    
    try:
        # Validate input path
        input_path_obj = Path(input_path)
        if not input_path_obj.exists():
            raise MDLFileError(
                message=f"Input path does not exist: {input_path}",
                suggestion="Check the path and try again."
            )
        
        # Find MDL files
        if input_path_obj.is_file():
            mdl_files = [input_path_obj] if input_path_obj.suffix == '.mdl' else []
        else:
            mdl_files = find_mdl_files(input_path_obj)
        
        if not mdl_files:
            raise MDLConfigurationError(
                message=f"No MDL files found in: {input_path}",
                suggestion="Ensure the path contains .mdl files or specify a single .mdl file."
            )
        
        if verbose:
            print_section("Building MDL Project")
            print_info(f"Input: {input_path}")
            print_info(f"Output: {output_path}")
            print_info(f"Found {len(mdl_files)} MDL file(s)")
            print_separator()
        
        # Create output directory
        output_path_obj = Path(output_path)
        if output_path_obj.exists():
            if verbose:
                print_warning(f"Output directory already exists: {output_path}")
                print_info("Removing existing directory...")
            shutil.rmtree(output_path_obj)
        
        output_path_obj.mkdir(parents=True, exist_ok=True)
        
        # Build the datapack
        pack = MDLPack()
        
        for mdl_file in mdl_files:
            if verbose:
                print_info(f"Processing: {color.file_path(mdl_file.name)}")
            
            try:
                pack.add_mdl_file(mdl_file)
                if verbose:
                    print_success(f"✓ Processed: {color.file_path(mdl_file.name)}")
            except Exception as e:
                error_collector.add_error(create_error(
                    MDLConfigurationError,
                    f"Failed to process {mdl_file.name}: {str(e)}",
                    file_path=str(mdl_file),
                    suggestion="Check the MDL file syntax and try again."
                ))
        
        # Check for errors before proceeding
        if error_collector.has_errors():
            error_collector.print_errors(verbose=verbose, ignore_warnings=ignore_warnings)
            error_collector.raise_if_errors()
        
        # Generate the datapack
        if verbose:
            print_separator()
            print_info("Generating datapack files...")
        
        try:
            pack.generate_datapack(output_path_obj, pack_format_override)
            if verbose:
                print_success("✓ Datapack generated successfully")
        except Exception as e:
            error_collector.add_error(create_error(
                MDLConfigurationError,
                f"Failed to generate datapack: {str(e)}",
                suggestion="Check the output directory permissions and try again."
            ))
        
        # Create wrapper if requested
        if wrapper:
            if verbose:
                print_info(f"Creating wrapper: {wrapper}")
            
            try:
                create_wrapper(output_path_obj, wrapper)
                if verbose:
                    print_success(f"✓ Wrapper created: {wrapper}")
            except Exception as e:
                error_collector.add_error(create_error(
                    MDLFileError,
                    f"Failed to create wrapper: {str(e)}",
                    suggestion="Check file permissions and disk space."
                ))
        
        # Final status
        if verbose:
            print_separator()
            print_success("Build completed successfully!")
            print_info(f"Output location: {color.file_path(output_path)}")
            if wrapper:
                print_info(f"Wrapper file: {color.file_path(wrapper)}")
        
        # Print any warnings if not ignored
        if not ignore_warnings and error_collector.has_warnings():
            error_collector.print_errors(verbose=verbose, ignore_warnings=False)
        
        # Raise if there are any errors
        error_collector.raise_if_errors()
        
    except Exception as e:
        if not isinstance(e, (MDLConfigurationError, MDLFileError)):
            error_collector.add_error(create_error(
                MDLConfigurationError,
                f"Unexpected build error: {str(e)}",
                suggestion="If this error persists, please report it as a bug."
            ))
        
        error_collector.print_errors(verbose=verbose, ignore_warnings=ignore_warnings)
        error_collector.raise_if_errors()


def create_wrapper(output_dir: Path, wrapper_name: str) -> None:
    """Create a zip wrapper around the output directory.
    
    Args:
        output_dir: Directory to wrap
        wrapper_name: Name of the zip file
    """
    wrapper_path = Path(wrapper_name)
    
    # Ensure .zip extension
    if not wrapper_path.suffix.lower() == '.zip':
        wrapper_path = wrapper_path.with_suffix('.zip')
    
    # Remove existing wrapper if it exists
    if wrapper_path.exists():
        wrapper_path.unlink()
    
    # Create the zip file
    with zipfile.ZipFile(wrapper_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in output_dir.rglob('*'):
            if file_path.is_file():
                # Calculate relative path within the zip
                arcname = file_path.relative_to(output_dir)
                zipf.write(file_path, arcname)


def build_single_file(mdl_file: Path, output_dir: Path, verbose: bool = False) -> None:
    """Build a single MDL file.
    
    Args:
        mdl_file: Path to the MDL file
        output_dir: Output directory
        verbose: Enable verbose output
    """
    if verbose:
        print_info(f"Building single file: {color.file_path(mdl_file.name)}")
    
    pack = MDLPack()
    pack.add_mdl_file(mdl_file)
    pack.generate_datapack(output_dir)
    
    if verbose:
        print_success(f"✓ Built: {color.file_path(mdl_file.name)}")


def build_directory(input_dir: Path, output_dir: Path, verbose: bool = False) -> None:
    """Build all MDL files in a directory.
    
    Args:
        input_dir: Input directory containing MDL files
        output_dir: Output directory
        verbose: Enable verbose output
    """
    if verbose:
        print_info(f"Building directory: {color.file_path(input_dir.name)}")
    
    mdl_files = find_mdl_files(input_dir)
    
    if not mdl_files:
        raise MDLConfigurationError(
            message=f"No MDL files found in directory: {input_dir}",
            suggestion="Ensure the directory contains .mdl files."
        )
    
    pack = MDLPack()
    
    for mdl_file in mdl_files:
        if verbose:
            print_info(f"Adding: {color.file_path(mdl_file.name)}")
        pack.add_mdl_file(mdl_file)
    
    pack.generate_datapack(output_dir)
    
    if verbose:
        print_success(f"✓ Built {len(mdl_files)} file(s) from {color.file_path(input_dir.name)}")
