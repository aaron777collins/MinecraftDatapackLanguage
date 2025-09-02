"""
CLI Help System - Comprehensive help documentation for MDL CLI
"""

from .cli_colors import (
    print_header, print_title, print_section, print_separator,
    print_success, print_warning, print_info, print_bullet,
    print_code, print_command, print_option, color
)


def show_main_help():
    """Display the main help message for the MDL CLI."""
    try:
        from . import __version__
        version = __version__
    except ImportError:
        version = "unknown"
    
    print_header(f"MDL (Minecraft Datapack Language) CLI - v{version}")
    print_separator()
    print()
    
    print_info("MDL is a simplified language for creating Minecraft datapacks with variables, control structures, and easy syntax. This CLI tool compiles MDL files into standard Minecraft datapacks.")
    print()
    
    print_section("Available Commands")
    print()
    
    print_command("build")
    print_info("    - Compile MDL files into a Minecraft datapack")
    print()
    
    print_command("check")
    print_info("    - Validate MDL files for syntax and semantic errors")
    print()
    
    print_command("new")
    print_info("    - Create a new MDL project with template files")
    print()
    
    print_section("Detailed Help")
    print()
    
    print_info("For detailed information about any command, use:")
    print_code("  mdl <command> --help")
    print()
    
    print_info("Examples:")
    print_code("  mdl build --help")
    print_info("    - Show build command options")
    print_code("  mdl check --help")
    print_info("    - Show check command options")
    print_code("  mdl new --help")
    print_info("    - Show new project options")
    print()
    
    print_section("Quick Start")
    print()
    
    print_bullet("1. Create a new project:")
    print_code("   mdl new my_project")
    print()
    
    print_bullet("2. Build your datapack:")
    print_code("   mdl build --mdl my_project.mdl -o dist")
    print()
    
    print_bullet("3. Check for errors:")
    print_code("   mdl check my_project.mdl")
    print()
    
    print_section("Documentation")
    print()
    
    print_bullet("Language Reference: https://www.mcmdl.com/docs/language-reference")
    print_bullet("CLI Reference: https://www.mcmdl.com/docs/cli-reference")
    print_bullet("Examples: https://www.mcmdl.com/docs/examples")
    print()
    
    print_section("Error Reporting")
    print()
    
    print_info("MDL provides detailed error messages with:")
    print_bullet("Exact file location (line, column)")
    print_bullet("Context lines showing the problematic code")
    print_bullet("Helpful suggestions for fixing issues")
    print_bullet("Multiple error collection and reporting")
    print()
    
    print_info("For support and bug reports, visit:")
    print_code("https://github.com/aaron777collins/MinecraftDatapackLanguage")


def show_build_help():
    """Display detailed help for the build command."""
    print_title("MDL Build Command - Compile MDL Files to Minecraft Datapacks")
    print_separator()
    print()
    
    print_info("The build command compiles MDL files into standard Minecraft datapacks that can be loaded directly into Minecraft.")
    print()
    
    print_section("Usage")
    print()
    
    print_code("  mdl build --mdl <input> -o <output> [options]")
    print()
    
    print_section("Arguments")
    print()
    
    print_option("--mdl, -m <input>")
    print_info("     Input MDL file or directory containing .mdl files")
    print_info("     Examples: --mdl project.mdl, --mdl src/, --mdl .")
    print()
    
    print_option("-o, --output <output>")
    print_info("     Output directory for the generated datapack")
    print_info("     Example: -o dist, -o build/my_pack")
    print()
    
    print_section("Options")
    print()
    
    print_option("--verbose, -v")
    print_info("     Enable verbose output with detailed build information")
    print_info("     Shows file parsing, function generation, and progress")
    print()
    
    print_option("--pack-format <number>")
    print_info("     Override the pack format number (default: 82)")
    print_info("     Higher numbers support newer Minecraft versions")
    print()
    
    print_option("--wrapper <name>")
    print_info("     Create a zip file with the specified name")
    print_info("     Example: --wrapper my_pack.zip")
    print()
    
    print_option("--ignore-warnings")
    print_info("     Suppress warning messages during build")
    print_info("     Only errors will be shown")
    print()
    
    print_section("Examples")
    print()
    
    print_code("  mdl build --mdl my_project.mdl -o dist")
    print_info("     Build a single MDL file to dist/ directory")
    print()
    
    print_code("  mdl build --mdl src/ -o build/ --verbose")
    print_info("     Build all MDL files in src/ to build/ with verbose output")
    print()
    
    print_code("  mdl build --mdl . -o output --wrapper my_pack.zip")
    print_info("     Build current directory and create zip file")
    print()
    
    print_section("Output Structure")
    print()
    
    print_info("The build command generates a standard Minecraft datapack structure:")
    print_bullet("pack.mcmeta - Pack metadata and format information")
    print_bullet("data/ - Contains all generated functions and resources")
    print_bullet("data/<namespace>/function/ - Generated .mcfunction files")
    print_bullet("data/minecraft/tags/function/ - Function tags for load/tick")
    print()
    
    print_success("Build completed successfully! Your datapack is ready to use in Minecraft.")


def show_check_help():
    """Display detailed help for the check command."""
    print_title("MDL Check Command - Validate MDL Files")
    print_separator()
    print()
    
    print_info("The check command validates MDL files for syntax errors, semantic issues, and potential problems before building.")
    print()
    
    print_section("Usage")
    print()
    
    print_code("  mdl check <input> [options]")
    print()
    
    print_section("Arguments")
    print()
    
    print_option("<input>")
    print_info("     Input MDL file or directory to check")
    print_info("     Examples: project.mdl, src/, .")
    print()
    
    print_section("Options")
    print()
    
    print_option("--verbose, -v")
    print_info("     Enable verbose output with detailed validation information")
    print_info("     Shows parsing steps, variable analysis, and scope checking")
    print()
    
    print_option("--ignore-warnings")
    print_info("     Suppress warning messages during check")
    print_info("     Only errors will be shown")
    print()
    
    print_section("What Gets Checked")
    print()
    
    print_info("The check command validates:")
    print_bullet("Syntax correctness (proper MDL grammar)")
    print_bullet("Variable declarations and usage")
    print_bullet("Scope boundaries and function calls")
    print_bullet("Control structure validity")
    print_bullet("Resource file references")
    print_bullet("Pack configuration")
    print()
    
    print_section("Examples")
    print()
    
    print_code("  mdl check my_project.mdl")
    print_info("     Check a single MDL file")
    print()
    
    print_code("  mdl check src/ --verbose")
    print_info("     Check all MDL files in src/ with detailed output")
    print()
    
    print_code("  mdl check . --ignore-warnings")
    print_info("     Check current directory, showing only errors")
    print()
    
    print_section("Output")
    print()
    
    print_info("Check results show:")
    print_bullet("✓ Valid files with no issues")
    print_bullet("⚠ Warning messages for potential problems")
    print_bullet("✗ Error messages for issues that must be fixed")
    print_bullet("File locations and line numbers for all issues")
    print_bullet("Helpful suggestions for fixing problems")
    print()
    
    print_success("Use check before build to catch issues early!")


def show_new_help():
    """Display detailed help for the new command."""
    print_title("MDL New Command - Create New MDL Projects")
    print_separator()
    print()
    
    print_info("The new command creates a new MDL project with template files and proper structure.")
    print()
    
    print_section("Usage")
    print()
    
    print_code("  mdl new <project_name> [options]")
    print()
    
    print_section("Arguments")
    print()
    
    print_option("<project_name>")
    print_info("     Name for the new project (will create project_name/ directory)")
    print_info("     Examples: my_datapack, adventure_pack, minigame")
    print()
    
    print_section("Options")
    print()
    
    print_option("--pack-name <name>")
    print_info("     Custom pack name (default: same as project name)")
    print_info("     This appears in the pack.mcmeta file")
    print()
    
    print_option("--pack-format <number>")
    print_info("     Pack format number (default: 82)")
    print_info("     Higher numbers support newer Minecraft versions")
    print_info("     Common values: 15 (1.17+), 26 (1.18+), 82 (1.20+)")
    print()
    
    print_section("What Gets Created")
    print()
    
    print_info("The new command creates:")
    print_bullet("project_name/ directory")
    print_bullet("project_name.mdl - Main MDL source file")
    print_bullet("README.md - Project documentation template")
    print_bullet("Proper pack.mcmeta configuration")
    print_bullet("Basic function structure (load, main, tick)")
    print_bullet("Example variable and command usage")
    print()
    
    print_section("Examples")
    print()
    
    print_code("  mdl new my_datapack")
    print_info("     Create a basic project with default settings")
    print()
    
    print_code("  mdl new adventure_pack --pack-name \"Adventure Pack\"")
    print_info("     Create project with custom pack name")
    print()
    
    print_code("  mdl new minigame --pack-format 26")
    print_info("     Create project targeting Minecraft 1.18+")
    print()
    
    print_section("Project Structure")
    print()
    
    print_info("New projects include:")
    print_bullet("load function - Runs when datapack is loaded")
    print_bullet("main function - Main game logic")
    print_bullet("tick function - Runs every game tick")
    print_bullet("Example variables and scoreboard setup")
    print_bullet("Basic command structure")
    print()
    
    print_success("Project created! Start editing the .mdl file and use 'mdl build' to compile.")


def show_error_help():
    """Display help for common errors and troubleshooting."""
    print_title("MDL Error Help - Troubleshooting Common Issues")
    print_separator()
    print()
    
    print_info("This section helps you resolve common MDL compilation and runtime errors.")
    print()
    
    print_section("Common Syntax Errors")
    print()
    
    print_warning("Missing semicolon")
    print_info("     Ensure all commands end with semicolons")
    print_code("     tellraw @a \"Hello\"  // Missing semicolon")
    print_code("     tellraw @a \"Hello\"; // Correct")
    print()
    
    print_warning("Invalid variable syntax")
    print_info("     Variables must start with $ and use valid characters")
    print_code("     $playerScore  // Correct")
    print_code("     playerScore   // Missing $")
    print_code("     $player-score // Invalid character")
    print()
    
    print_warning("Scope mismatch")
    print_info("     Ensure all scopes are properly closed")
    print_code("     if $condition$ {")
    print_code("       tellraw @a \"True\";")
    print_code("     } // Missing closing brace")
    print()
    
    print_section("Build Errors")
    print()
    
    print_warning("File not found")
    print_info("     Check that the input file/directory exists")
    print_info("     Use absolute paths or verify relative paths")
    print()
    
    print_warning("Permission denied")
    print_info("     Ensure you have write access to the output directory")
    print_info("     Try running as administrator or change output location")
    print()
    
    print_section("Runtime Errors")
    print()
    
    print_warning("Function not found")
    print_info("     Check that all referenced functions exist")
    print_info("     Verify function names match exactly (case-sensitive)")
    print()
    
    print_warning("Scoreboard not found")
    print_info("     Ensure scoreboards are created before use")
    print_info("     Use scoreboard objectives add <name> <criteria>")
    print()
    
    print_section("Getting Help")
    print()
    
    print_info("If you're still having issues:")
    print_bullet("Check the error message carefully for file and line numbers")
    print_bullet("Use --verbose flag for more detailed output")
    print_bullet("Verify your MDL syntax against the language reference")
    print_bullet("Check the examples for correct usage patterns")
    print_bullet("Report bugs with detailed error information")
    print()
    
    print_success("Most errors can be resolved by checking syntax and following the error suggestions!")
