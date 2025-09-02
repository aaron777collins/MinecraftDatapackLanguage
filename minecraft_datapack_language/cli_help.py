"""
CLI Help System - Comprehensive help documentation for MDL CLI
"""


def show_main_help():
    """Display the main help message for the MDL CLI."""
    try:
        from . import __version__
        version = __version__
    except ImportError:
        version = "unknown"
    
    print(f"""
[GAME] MDL (Minecraft Datapack Language) CLI - v{version}
====================================================

MDL is a simplified language for creating Minecraft datapacks with variables, 
control structures, and easy syntax. This CLI tool compiles MDL files into 
standard Minecraft datapacks.

[CMD] Available Commands:
=====================

[BUILD] build    - Compile MDL files into a Minecraft datapack
[CHECK] check    - Validate MDL files for syntax and semantic errors  
[NEW] new      - Create a new MDL project with template files

[DOC] Detailed Help:
================

For detailed information about any command, use:
  mdl <command> --help

Examples:
  mdl build --help    - Show build command options
  mdl check --help    - Show check command options
  mdl new --help      - Show new project options

[NEXT] Quick Start:
==============

1. Create a new project:
   mdl new my_project

2. Build your datapack:
   mdl build --mdl my_project.mdl -o dist

3. Check for errors:
   mdl check my_project.mdl

[INFO] Documentation:
================

• Language Reference: https://www.mcmdl.com/docs/language-reference
• CLI Reference: https://www.mcmdl.com/docs/cli-reference
• Examples: https://www.mcmdl.com/docs/examples

🐛 Error Reporting:
==================

MDL provides detailed error messages with:
• Exact file location (line, column)
• Context lines showing the problematic code
• Helpful suggestions for fixing issues
• Multiple error collection and reporting

For support and bug reports, visit: https://github.com/aaron777collins/MinecraftDatapackLanguage
""")


def show_build_help():
    """Display detailed help for the build command."""
    print("""
[BUILD] MDL Build Command - Compile MDL Files to Minecraft Datapacks
===============================================================

The build command compiles MDL files into standard Minecraft datapacks that can 
be loaded directly into Minecraft.

[CMD] Usage:
========

  mdl build --mdl <input> -o <output> [options]

[DIR] Arguments:
============

  --mdl, -m <input>     Input MDL file or directory containing .mdl files
                        Examples: --mdl project.mdl, --mdl src/, --mdl .

  -o, --output <output> Output directory for the generated datapack
                        Example: -o dist, -o build/my_pack

[OPT] Options:
==========

  --verbose, -v         Enable verbose output with detailed build information
                        Shows file parsing, function generation, and progress

  --pack-format <num>   Override the pack format number in pack.mcmeta
                        Default: 82 (Minecraft 1.20+)
                        Example: --pack-format 15 (for older versions)

  --wrapper <name>      Create a zip file with the specified name
                        Example: --wrapper my_awesome_pack

  --ignore-warnings     Suppress warning messages during build
                        Only show errors, hide all warnings

[EX] Examples:
===========

1. Build a single MDL file:
   mdl build --mdl hello_world.mdl -o dist

2. Build all MDL files in a directory:
   mdl build --mdl src/ -o build/my_pack

3. Build current directory with verbose output:
   mdl build --mdl . -o dist --verbose

4. Build with custom pack format and zip wrapper:
   mdl build --mdl project.mdl -o dist --pack-format 15 --wrapper my_pack

5. Build multiple files in a directory:
   mdl build --mdl examples/ -o output --verbose

[OUT] Output Structure:
===================

The build command creates a standard Minecraft datapack structure:

  output/
  ├── pack.mcmeta              # Datapack metadata
  └── data/
      ├── <namespace>/         # Your datapack namespace
      │   └── function/        # Generated functions
      │       ├── load.mcfunction
      │       └── *.mcfunction
      └── minecraft/
          └── tags/
              └── function/    # Load/tick tags
                  ├── load.json
                  └── tick.json

[FEAT] Features:
===========

• Multi-file compilation - Merge multiple .mdl files into one datapack
• Variable system - Automatic scoreboard objective creation
• Control structures - If/else statements and while loops
• Function calls - Call other functions within your datapack
• Raw commands - Use native Minecraft commands with $variable$ substitution
• Error handling - Detailed error reporting with suggestions
• Progress tracking - Verbose mode shows build progress

[CHECK] Error Handling:
=================

The build command provides comprehensive error reporting:
• Syntax errors with exact line and column numbers
• Context lines showing the problematic code
• Helpful suggestions for fixing issues
• Multiple error collection (won't stop on first error)

For more information, visit: https://www.mcmdl.com/docs/cli-reference#build
""")


def show_check_help():
    """Display detailed help for the check command."""
    print("""
[CHECK] MDL Check Command - Validate MDL Files for Errors
====================================================

The check command validates MDL files for syntax errors, semantic issues, and 
potential problems without generating any output files.

[CMD] Usage:
========

  mdl check <input> [options]

[DIR] Arguments:
============

  <input>               Input MDL file or directory containing .mdl files
                        Examples: project.mdl, src/, .

[OPT] Options:
==========

  --verbose, -v         Enable verbose output with detailed validation information
                        Shows parsing steps, token analysis, and detailed error context

  --ignore-warnings     Suppress warning messages during check
                        Only show errors, hide all warnings

[EX] Examples:
===========

1. Check a single MDL file:
   mdl check hello_world.mdl

2. Check all MDL files in a directory:
   mdl check src/

3. Check current directory with verbose output:
   mdl check . --verbose

4. Check multiple files:
   mdl check examples/ --verbose

[CHECK] Validation Types:
===================

The check command performs comprehensive validation:

[EX] Syntax Validation:
• Lexical analysis - Token recognition and validation
• Parsing - AST construction and syntax structure
• Grammar validation - Language rule compliance

[OPT] Semantic Validation:
• Variable declarations - Proper variable naming and scope
• Function definitions - Valid function signatures
• Control structures - Proper if/else and while loop syntax
• Command validation - Minecraft command syntax checking

[WARN] Error Detection:
• Missing semicolons and braces
• Invalid variable names or references
• Unclosed strings and comments
• Malformed control structures
• Invalid selector syntax
• Undefined function calls

[REP] Error Reporting:
==================

The check command provides detailed error information:

[FEAT] Error Details:
• File path and exact location (line, column)
• Error type and description
• Context lines showing the problematic code
• Helpful suggestions for fixing issues

[CMD] Error Types:
• MDLSyntaxError - Basic syntax violations
• MDLLexerError - Token recognition issues
• MDLParserError - Parsing and structure problems
• MDLValidationError - Semantic validation failures
• MDLFileError - File access and I/O issues

[TIP] Example Error Output:
========================

  Error 1: MDLSyntaxError in test.mdl:15:8
  Missing closing brace for if statement
  Context:
    13:   if (score > 10) {
    14:     say "High score!"
    15:     score = 0
    16:   }
  
  Suggestion: Add closing brace '}' after line 15

[CHECK] Advanced Features:
====================

• Multi-file validation - Check entire projects at once
• Directory support - Recursively check all .mdl files
• Error collection - Report all errors, not just the first one
• Context preservation - Show surrounding code for better debugging
• Suggestion system - Provide helpful fix recommendations

[NEXT] Integration:
==============

The check command is perfect for:
• CI/CD pipelines - Automated validation
• Development workflows - Pre-commit checks
• Learning MDL - Understand syntax requirements
• Debugging - Identify and fix issues quickly

For more information, visit: https://www.mcmdl.com/docs/cli-reference#check
""")


def show_new_help():
    """Display detailed help for the new command."""
    try:
        from .cli_colors import color, print_header, print_title, print_section, print_separator, print_info, print_bullet, print_code
        
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
        print(color.info(f"For more information, visit: {color.file_path('https://www.mcmdl.com/docs/cli-reference#new')}"))
        print()
        
    except ImportError:
        # Fallback if colors aren't available
        print("""
[NEW] MDL New Command - Create New MDL Projects
============================================

The new command creates a new MDL project with template files and proper 
structure to get you started quickly.

[CMD] Usage:
========

  mdl new <project_name> [options]

[DIR] Arguments:
============

  <project_name>        Name for your new MDL project
                        This will be used for the project directory and pack name
                        Example: my_awesome_pack, hello_world, magic_system

[OPT] Options:
==========

  --pack-name <name>    Custom name for the datapack (defaults to project name)
                        This appears in the pack.mcmeta description
                        Example: --pack-name "My Awesome Magic Pack"

  --pack-format <num>   Pack format number for Minecraft version compatibility
                        Default: 82 (Minecraft 1.20+)
                        Example: --pack-format 15 (for older versions)

[EX] Examples:
===========

1. Create a basic project:
   mdl new hello_world

2. Create project with custom pack name:
   mdl new magic_system --pack-name "Epic Magic Pack"

3. Create project for older Minecraft version:
   mdl new retro_pack --pack-format 15

4. Create project with all custom options:
   mdl new my_project --pack-name "My Project" --pack-format 82

[OUT] Generated Structure:
======================

The new command creates a complete project structure:

  <project_name>/
  ├── README.md                    # Project documentation
  └── <project_name>.mdl          # Main MDL file with template code

[FILE] Template Content:
===================

The generated MDL file includes:

[CMD] Pack Declaration:
```mdl
pack {
  name: "project_name"
  format: 82
  description: "Generated by MDL CLI"
}
```

[OPT] Example Functions:
```mdl
function main {
  say "Hello from MDL!"
  
  // Variable example
  score = 10
  say "Score: $score$"
  
  // Conditional example
  if (score > 5) {
    say "High score!"
  } else {
    say "Try again!"
  }
}

function load {
  // This function runs when the datapack loads
  say "Datapack loaded successfully!"
}
```

[FEAT] Features:
===========

• Complete project setup - Ready-to-use structure
• Template code - Working examples to learn from
• Proper pack metadata - Correct pack.mcmeta configuration
• Documentation - README with usage instructions
• Best practices - Follows MDL conventions

[NEXT] Getting Started:
==================

After creating a new project:

1. Navigate to the project directory:
   cd <project_name>

2. Edit the MDL file:
   # Edit <project_name>.mdl with your code

3. Build the datapack:
   mdl build --mdl <project_name>.mdl -o dist

4. Check for errors:
   mdl check <project_name>.mdl

5. Load in Minecraft:
   # Copy the dist folder to your world's datapacks directory

[TIP] Tips:
========

• Use descriptive project names - They become your namespace
• Start with the template code - It demonstrates key MDL features
• Check your code regularly - Use `mdl check` during development
• Use version control - Git is great for tracking changes
• Read the documentation - Learn about all available features

[INFO] Next Steps:
=============

• Language Reference: https://www.mcmdl.com/docs/language-reference
• Examples: https://www.mcmdl.com/docs/examples
• CLI Reference: https://www.mcmdl.com/docs/cli-reference

For more information, visit: https://www.mcmdl.com/docs/cli-reference#new
""")
