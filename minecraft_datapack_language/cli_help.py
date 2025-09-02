"""
CLI Help System - Comprehensive help documentation for MDL CLI
"""
from .cli_colors import color, print_header, print_title, print_section, print_separator, print_info, print_bullet, print_code

def show_main_help():
    """Display the main help message for the MDL CLI."""
    try:
        from . import __version__
        version = __version__
    except ImportError:
        version = "unknown"

    # Header
    print()
    print_header(f"MDL (Minecraft Datapack Language) CLI - v{version}")
    print_separator("=", 70)
    print()
    
    # Description
    print(color.info("MDL is a simplified language for creating Minecraft datapacks with variables,"))
    print(color.info("control structures, and easy syntax. This CLI tool compiles MDL files into"))
    print(color.info("standard Minecraft datapacks."))
    print()
    
    # Available Commands
    print_section("Available Commands")
    print()
    print(f"  {color.command('build')}    - Compile MDL files into a Minecraft datapack")
    print(f"  {color.command('check')}    - Validate MDL files for syntax and semantic errors")  
    print(f"  {color.command('new')}      - Create a new MDL project with template files")
    print()
    
    # Detailed Help
    print_section("Detailed Help")
    print()
    print(color.info("For detailed information about any command, use:"))
    print(f"  {color.code('mdl <command> --help')}")
    print()
    print(color.info("Examples:"))
    print(f"  {color.code('mdl build --help')}    - Show build command options")
    print(f"  {color.code('mdl check --help')}    - Show check command options")
    print(f"  {color.code('mdl new --help')}      - Show new project options")
    print()
    
    # Quick Start
    print_section("Quick Start")
    print()
    print(f"1. Create a new project:")
    print(f"   {color.code('mdl new my_project')}")
    print()
    print(f"2. Build your datapack:")
    print(f"   {color.code('mdl build --mdl my_project.mdl -o dist')}")
    print()
    print(f"3. Check for errors:")
    print(f"   {color.code('mdl check my_project.mdl')}")
    print()
    
    # Documentation
    print_section("Documentation")
    print()
    print_bullet(f"Language Reference: {color.file_path('https://www.mcmdl.com/docs/language-reference')}")
    print_bullet(f"CLI Reference: {color.file_path('https://www.mcmdl.com/docs/cli-reference')}")
    print_bullet(f"Examples: {color.file_path('https://www.mcmdl.com/docs/examples')}")
    print()
    
    # Error Reporting
    print_section("Error Reporting")
    print()
    print(color.info("MDL provides detailed error messages with:"))
    print_bullet("Exact file location (line, column)")
    print_bullet("Context lines showing the problematic code")
    print_bullet("Helpful suggestions for fixing issues")
    print_bullet("Multiple error collection and reporting")
    print()
    
    # Support
    print(color.info(f"For support and bug reports, visit: {color.file_path('https://github.com/aaron777collins/MinecraftDatapackLanguage')}"))
    print()

def show_build_help():
    """Display detailed help for the build command."""
    # Header
    print()
    print_header("MDL Build Command - Compile MDL Files to Minecraft Datapacks")
    print_separator("=", 75)
    print()
    
    # Description
    print(color.info("The build command compiles MDL files into standard Minecraft datapacks that can"))
    print(color.info("be loaded directly into Minecraft."))
    print()
    
    # Usage
    print_section("Usage")
    print()
    print(f"  {color.code('mdl build --mdl <input> -o <output> [options]')}")
    print()
    
    # Arguments
    print_section("Arguments")
    print()
    print(f"  {color.command('--mdl, -m')} {color.highlight('<input>')}     Input MDL file or directory containing .mdl files")
    print(f"                        Examples: {color.code('--mdl project.mdl')}, {color.code('--mdl src/')}, {color.code('--mdl .')}")
    print()
    print(f"  {color.command('-o, --output')} {color.highlight('<output>')} Output directory for the generated datapack")
    print(f"                        Example: {color.code('-o dist')}, {color.code('-o build/my_pack')}")
    print()
    
    # Options
    print_section("Options")
    print()
    print(f"  {color.command('--verbose, -v')}         Enable verbose output with detailed build information")
    print(f"                        Shows file parsing, function generation, and progress")
    print()
    print(f"  {color.command('--pack-format')} {color.highlight('<num>')}   Override the pack format number in pack.mcmeta")
    print(f"                        Default: {color.highlight('82')} (Minecraft 1.20+)")
    print(f"                        Example: {color.code('--pack-format 15')} (for older versions)")
    print()
    print(f"  {color.command('--wrapper')} {color.highlight('<name>')}      Create a zip file with the specified name")
    print(f"                        Example: {color.code('--wrapper my_awesome_pack')}")
    print()
    print(f"  {color.command('--ignore-warnings')}     Suppress warning messages during build")
    print(f"                        Only show errors, hide all warnings")
    print()
    
    # Examples
    print_section("Examples")
    print()
    print(f"1. Build a single MDL file:")
    print(f"   {color.code('mdl build --mdl hello_world.mdl -o dist')}")
    print()
    print(f"2. Build all MDL files in a directory:")
    print(f"   {color.code('mdl build --mdl src/ -o build/my_pack')}")
    print()
    print(f"3. Build current directory with verbose output:")
    print(f"   {color.code('mdl build --mdl . -o dist --verbose')}")
    print()
    print(f"4. Build with custom pack format and zip wrapper:")
    print(f"   {color.code('mdl build --mdl project.mdl -o dist --pack-format 15 --wrapper my_pack')}")
    print()
    print(f"5. Build multiple files in a directory:")
    print(f"   {color.code('mdl build --mdl examples/ -o output --verbose')}")
    print()
    
    # Output Structure
    print_section("Output Structure")
    print()
    print(color.info("The build command creates a standard Minecraft datapack structure:"))
    print()
    print(f"  {color.file_path('output/')}")
    print(f"  ├── {color.file_path('pack.mcmeta')}              # Datapack metadata")
    print(f"  └── {color.file_path('data/')}")
    print(f"      ├── {color.file_path('<namespace>/')}         # Your datapack namespace")
    print(f"      │   └── {color.file_path('function/')}        # Generated functions")
    print(f"      │       ├── {color.file_path('load.mcfunction')}")
    print(f"      │       └── {color.file_path('*.mcfunction')}")
    print(f"      └── {color.file_path('minecraft/')}")
    print(f"          └── {color.file_path('tags/')}")
    print(f"              └── {color.file_path('function/')}    # Load/tick tags")
    print(f"                  ├── {color.file_path('load.json')}")
    print(f"                  └── {color.file_path('tick.json')}")
    print()
    
    # Features
    print_section("Features")
    print()
    print_bullet("Multi-file compilation - Merge multiple .mdl files into one datapack")
    print_bullet("Variable system - Automatic scoreboard objective creation")
    print_bullet("Control structures - If/else statements and while loops")
    print_bullet("Function calls - Call other functions within your datapack")
    print_bullet("Raw commands - Use native Minecraft commands with $variable$ substitution")
    print_bullet("Error handling - Detailed error reporting with suggestions")
    print_bullet("Progress tracking - Verbose mode shows build progress")
    print()
    
    # Error Handling
    print_section("Error Handling")
    print()
    print(color.info("The build command provides comprehensive error reporting:"))
    print_bullet("Syntax errors with exact line and column numbers")
    print_bullet("Context lines showing the problematic code")
    print_bullet("Helpful suggestions for fixing issues")
    print_bullet("Multiple error collection (won't stop on first error)")
    print()
    
    # More Info
    print(color.info(f"For more information, visit: {color.file_path('https://www.mcmdl.com/docs/cli-reference/#basic-commands')}"))
    print()

def show_check_help():
    """Display detailed help for the check command."""
    # Header
    print()
    print_header("MDL Check Command - Validate MDL Files for Errors")
    print_separator("=", 70)
    print()
    
    # Description
    print(color.info("The check command validates MDL files for syntax errors, semantic issues, and"))
    print(color.info("potential problems without generating any output files."))
    print()
    
    # Usage
    print_section("Usage")
    print()
    print(f"  {color.code('mdl check <input> [options]')}")
    print()
    
    # Arguments
    print_section("Arguments")
    print()
    print(f"  {color.highlight('<input>')}               Input MDL file or directory containing .mdl files")
    print(f"                        Examples: {color.code('project.mdl')}, {color.code('src/')}, {color.code('.')}")
    print()
    
    # Options
    print_section("Options")
    print()
    print(f"  {color.command('--verbose, -v')}         Enable verbose output with detailed validation information")
    print(f"                        Shows parsing steps, token analysis, and detailed error context")
    print()
    print(f"  {color.command('--ignore-warnings')}     Suppress warning messages during check")
    print(f"                        Only show errors, hide all warnings")
    print()
    
    # Examples
    print_section("Examples")
    print()
    print(f"1. Check a single MDL file:")
    print(f"   {color.code('mdl check hello_world.mdl')}")
    print()
    print(f"2. Check all MDL files in a directory:")
    print(f"   {color.code('mdl check src/')}")
    print()
    print(f"3. Check current directory with verbose output:")
    print(f"   {color.code('mdl check . --verbose')}")
    print()
    print(f"4. Check multiple files:")
    print(f"   {color.code('mdl check examples/ --verbose')}")
    print()
    
    # Validation Types
    print_section("Validation Types")
    print()
    print(color.info("The check command performs comprehensive validation:"))
    print()
    
    print_section("Syntax Validation")
    print_bullet("Lexical analysis - Token recognition and validation")
    print_bullet("Parsing - AST construction and syntax structure")
    print_bullet("Grammar validation - Language rule compliance")
    print()
    
    print_section("Semantic Validation")
    print_bullet("Variable declarations - Proper variable naming and scope")
    print_bullet("Function definitions - Valid function signatures")
    print_bullet("Control structures - Proper if/else and while loop syntax")
    print_bullet("Command validation - Minecraft command syntax checking")
    print()
    
    print_section("Error Detection")
    print_bullet("Missing semicolons and braces")
    print_bullet("Invalid variable names or references")
    print_bullet("Unclosed strings and comments")
    print_bullet("Malformed control structures")
    print_bullet("Invalid selector syntax")
    print_bullet("Undefined function calls")
    print()
    
    # Error Reporting
    print_section("Error Reporting")
    print()
    print(color.info("The check command provides detailed error information:"))
    print()
    
    print_section("Error Details")
    print_bullet("File path and exact location (line, column)")
    print_bullet("Error type and description")
    print_bullet("Context lines showing the problematic code")
    print_bullet("Helpful suggestions for fixing issues")
    print()
    
    print_section("Error Types")
    print_bullet("MDLSyntaxError - Basic syntax violations")
    print_bullet("MDLLexerError - Token recognition issues")
    print_bullet("MDLParserError - Parsing and structure problems")
    print_bullet("MDLValidationError - Semantic validation failures")
    print_bullet("MDLFileError - File access and I/O issues")
    print()
    
    # Example Error Output
    print_section("Example Error Output")
    print()
    print(color.info("  Error 1: MDLSyntaxError in test.mdl:15:8"))
    print(color.info("  Missing closing brace for if statement"))
    print(color.info("  Context:"))
    print(f"     {color.line_number('13')}:   if (score > 10) {{")
    print(f"     {color.line_number('14')}:     say \"High score!\"")
    print(f"     {color.line_number('15')}:     score = 0")
    print(f"     {color.line_number('16')}:   }}")
    print()
    print(color.suggestion("  Suggestion: Add closing brace '}' after line 15"))
    print()
    
    # Advanced Features
    print_section("Advanced Features")
    print()
    print_bullet("Multi-file validation - Check entire projects at once")
    print_bullet("Directory support - Recursively check all .mdl files")
    print_bullet("Error collection - Report all errors, not just the first one")
    print_bullet("Context preservation - Show surrounding code for better debugging")
    print_bullet("Suggestion system - Provide helpful fix recommendations")
    print()
    
    # Integration
    print_section("Integration")
    print()
    print(color.info("The check command is perfect for:"))
    print_bullet("CI/CD pipelines - Automated validation")
    print_bullet("Development workflows - Pre-commit checks")
    print_bullet("Learning MDL - Understand syntax requirements")
    print_bullet("Debugging - Identify and fix issues quickly")
    print()
    
    # More Info
    print(color.info(f"For more information, visit: {color.file_path('https://www.mcmdl.com/docs/cli-reference#check-command')}"))
    print()

def show_new_help():
    """Display detailed help for the new command."""
    # Header
    print()
    print_header("MDL New Command - Create New MDL Projects")
    print_separator("=", 65)
    print()
    
    # Description
    print(color.info("The new command creates a new MDL project with template files and proper"))
    print(color.info("structure to get you started quickly."))
    print()
    
    # Usage
    print_section("Usage")
    print()
    print(f"  {color.code('mdl new <project_name> [options]')}")
    print()
    
    # Arguments
    print_section("Arguments")
    print()
    print(f"  {color.highlight('<project_name>')}        Name for your new MDL project")
    print(f"                        This will be used for the project directory and pack name")
    print(f"                        Example: {color.code('my_awesome_pack')}, {color.code('hello_world')}, {color.code('magic_system')}")
    print()
    
    # Options
    print_section("Options")
    print()
    print(f"  {color.command('--pack-name')} {color.highlight('<name>')}    Custom name for the datapack (defaults to project name)")
    print(f"                        This appears in the pack.mcmeta description")
    print(f"                        Example: {color.code('--pack-name "My Awesome Magic Pack"')}")
    print()
    print(f"  {color.command('--pack-format')} {color.highlight('<num>')}   Pack format number for Minecraft version compatibility")
    print(f"                        Default: {color.highlight('82')} (Minecraft 1.20+)")
    print(f"                        Example: {color.code('--pack-format 15')} (for older versions)")
    print()
    
    # Examples
    print_section("Examples")
    print()
    print(f"1. Create a basic project:")
    print(f"   {color.code('mdl new hello_world')}")
    print()
    print(f"2. Create project with custom pack name:")
    print(f"   {color.code('mdl new magic_system --pack-name "Epic Magic Pack"')}")
    print()
    print(f"3. Create project for older Minecraft version:")
    print(f"   {color.code('mdl new retro_pack --pack-format 15')}")
    print()
    print(f"4. Create project with all custom options:")
    print(f"   {color.code('mdl new my_project --pack-name "My Project" --pack-format 82')}")
    print()
    
    # Generated Structure
    print_section("Generated Structure")
    print()
    print(color.info("The new command creates a complete project structure:"))
    print()
    print(f"  {color.file_path('<project_name>/')}")
    print(f"  ├── {color.file_path('README.md')}                    # Project documentation")
    print(f"  └── {color.file_path('<project_name>.mdl')}          # Main MDL file with template code")
    print()
    
    # Template Content
    print_section("Template Content")
    print()
    print(color.info("The generated MDL file includes:"))
    print()
    
    print_section("Pack Declaration")
    print(f"{color.code('pack {')}")
    print(f"{color.code('  name: "project_name"')}")
    print(f"{color.code('  format: 82')}")
    print(f"{color.code('  description: "Generated by MDL CLI"')}")
    print(f"{color.code('}')}")
    print()
    
    print_section("Example Functions")
    print(f"{color.code('function main {')}")
    print(f"{color.code('  say "Hello from MDL!"')}")
    print(f"{color.code('  ')}")
    print(f"{color.code('  // Variable example')}")
    print(f"{color.code('  score = 10')}")
    print(f"{color.code('  say "Score: $score$"')}")
    print(f"{color.code('  ')}")
    print(f"{color.code('  // Conditional example')}")
    print(f"{color.code('  if (score > 5) {')}")
    print(f"{color.code('    say "High score!"')}")
    print(f"{color.code('  } else {')}")
    print(f"{color.code('    say "Try again!"')}")
    print(f"{color.code('  }')}")
    print(f"{color.code('}')}")
    print()
    print(f"{color.code('function load {')}")
    print(f"{color.code('  // This function runs when the datapack loads')}")
    print(f"{color.code('  say "Datapack loaded successfully!"')}")
    print(f"{color.code('}')}")
    print()
    
    # Features
    print_section("Features")
    print()
    print_bullet("Complete project setup - Ready-to-use structure")
    print_bullet("Template code - Working examples to learn from")
    print_bullet("Proper pack metadata - Correct pack.mcmeta configuration")
    print_bullet("Documentation - README with usage instructions")
    print_bullet("Best practices - Follows MDL conventions")
    print()
    
    # Getting Started
    print_section("Getting Started")
    print()
    print(color.info("After creating a new project:"))
    print()
    print(f"1. Navigate to the project directory:")
    print(f"   {color.code('cd <project_name>')}")
    print()
    print(f"2. Edit the MDL file:")
    print(f"   # Edit {color.file_path('<project_name>.mdl')} with your code")
    print()
    print(f"3. Build the datapack:")
    print(f"   {color.code('mdl build --mdl <project_name>.mdl -o dist')}")
    print()
    print(f"4. Check for errors:")
    print(f"   {color.code('mdl check <project_name>.mdl')}")
    print()
    print(f"5. Load in Minecraft:")
    print(f"   # Copy the dist folder to your world's datapacks directory")
    print()
    
    # Tips
    print_section("Tips")
    print()
    print_bullet("Use descriptive project names - They become your namespace")
    print_bullet("Start with the template code - It demonstrates key MDL features")
    print_bullet("Check your code regularly - Use `mdl check` during development")
    print_bullet("Use version control - Git is great for tracking changes")
    print_bullet("Read the documentation - Learn about all available features")
    print()
    
    # Next Steps
    print_section("Next Steps")
    print()
    print_bullet(f"Language Reference: {color.file_path('https://www.mcmdl.com/docs/language-reference')}")
    print_bullet(f"Examples: {color.file_path('https://www.mcmdl.com/docs/examples')}")
    print_bullet(f"CLI Reference: {color.file_path('https://www.mcmdl.com/docs/cli-reference')}")
    print()
    
    # More Info
    print(color.info(f"For more information, visit: {color.file_path('https://www.mcmdl.com/docs/cli-reference#new-command')}"))
    print()
