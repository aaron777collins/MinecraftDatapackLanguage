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
🎮 MDL (Minecraft Datapack Language) CLI - v{version}
====================================================

MDL is a simplified language for creating Minecraft datapacks with variables, 
control structures, and easy syntax. This CLI tool compiles MDL files into 
standard Minecraft datapacks.

📋 Available Commands:
=====================

🔨 build    - Compile MDL files into a Minecraft datapack
🔍 check    - Validate MDL files for syntax and semantic errors  
🆕 new      - Create a new MDL project with template files

📖 Detailed Help:
================

For detailed information about any command, use:
  mdl <command> --help

Examples:
  mdl build --help    - Show build command options
  mdl check --help    - Show check command options
  mdl new --help      - Show new project options

🚀 Quick Start:
==============

1. Create a new project:
   mdl new my_project

2. Build your datapack:
   mdl build --mdl my_project.mdl -o dist

3. Check for errors:
   mdl check my_project.mdl

📚 Documentation:
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

For support and bug reports, visit: https://www.mcmdl.com
""")


def show_build_help():
    """Display detailed help for the build command."""
    print("""
🔨 MDL Build Command - Compile MDL Files to Minecraft Datapacks
===============================================================

The build command compiles MDL files into standard Minecraft datapacks that can 
be loaded directly into Minecraft.

📋 Usage:
========

  mdl build --mdl <input> -o <output> [options]

📁 Arguments:
============

  --mdl, -m <input>     Input MDL file or directory containing .mdl files
                        Examples: --mdl project.mdl, --mdl src/, --mdl .

  -o, --output <output> Output directory for the generated datapack
                        Example: -o dist, -o build/my_pack

🔧 Options:
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

📝 Examples:
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

📂 Output Structure:
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

🎯 Features:
===========

• Multi-file compilation - Merge multiple .mdl files into one datapack
• Variable system - Automatic scoreboard objective creation
• Control structures - If/else statements and while loops
• Function calls - Call other functions within your datapack
• Raw commands - Use native Minecraft commands with $variable$ substitution
• Error handling - Detailed error reporting with suggestions
• Progress tracking - Verbose mode shows build progress

🔍 Error Handling:
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
🔍 MDL Check Command - Validate MDL Files for Errors
====================================================

The check command validates MDL files for syntax errors, semantic issues, and 
potential problems without generating any output files.

📋 Usage:
========

  mdl check <input> [options]

📁 Arguments:
============

  <input>               Input MDL file or directory containing .mdl files
                        Examples: project.mdl, src/, .

🔧 Options:
==========

  --verbose, -v         Enable verbose output with detailed validation information
                        Shows parsing steps, token analysis, and detailed error context

  --ignore-warnings     Suppress warning messages during check
                        Only show errors, hide all warnings

📝 Examples:
===========

1. Check a single MDL file:
   mdl check hello_world.mdl

2. Check all MDL files in a directory:
   mdl check src/

3. Check current directory with verbose output:
   mdl check . --verbose

4. Check multiple files:
   mdl check examples/ --verbose

🔍 Validation Types:
===================

The check command performs comprehensive validation:

📝 Syntax Validation:
• Lexical analysis - Token recognition and validation
• Parsing - AST construction and syntax structure
• Grammar validation - Language rule compliance

🔧 Semantic Validation:
• Variable declarations - Proper variable naming and scope
• Function definitions - Valid function signatures
• Control structures - Proper if/else and while loop syntax
• Command validation - Minecraft command syntax checking

⚠️  Error Detection:
• Missing semicolons and braces
• Invalid variable names or references
• Unclosed strings and comments
• Malformed control structures
• Invalid selector syntax
• Undefined function calls

📊 Error Reporting:
==================

The check command provides detailed error information:

🎯 Error Details:
• File path and exact location (line, column)
• Error type and description
• Context lines showing the problematic code
• Helpful suggestions for fixing issues

📋 Error Types:
• MDLSyntaxError - Basic syntax violations
• MDLLexerError - Token recognition issues
• MDLParserError - Parsing and structure problems
• MDLValidationError - Semantic validation failures
• MDLFileError - File access and I/O issues

💡 Example Error Output:
========================

  Error 1: MDLSyntaxError in test.mdl:15:8
  Missing closing brace for if statement
  Context:
    13:   if (score > 10) {
    14:     say "High score!"
    15:     score = 0
    16:   }
  
  Suggestion: Add closing brace '}' after line 15

🔍 Advanced Features:
====================

• Multi-file validation - Check entire projects at once
• Directory support - Recursively check all .mdl files
• Error collection - Report all errors, not just the first one
• Context preservation - Show surrounding code for better debugging
• Suggestion system - Provide helpful fix recommendations

🚀 Integration:
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
    print("""
🆕 MDL New Command - Create New MDL Projects
============================================

The new command creates a new MDL project with template files and proper 
structure to get you started quickly.

📋 Usage:
========

  mdl new <project_name> [options]

📁 Arguments:
============

  <project_name>        Name for your new MDL project
                        This will be used for the project directory and pack name
                        Example: my_awesome_pack, hello_world, magic_system

🔧 Options:
==========

  --pack-name <name>    Custom name for the datapack (defaults to project name)
                        This appears in the pack.mcmeta description
                        Example: --pack-name "My Awesome Magic Pack"

  --pack-format <num>   Pack format number for Minecraft version compatibility
                        Default: 82 (Minecraft 1.20+)
                        Example: --pack-format 15 (for older versions)

📝 Examples:
===========

1. Create a basic project:
   mdl new hello_world

2. Create project with custom pack name:
   mdl new magic_system --pack-name "Epic Magic Pack"

3. Create project for older Minecraft version:
   mdl new retro_pack --pack-format 15

4. Create project with all custom options:
   mdl new my_project --pack-name "My Project" --pack-format 82

📂 Generated Structure:
======================

The new command creates a complete project structure:

  <project_name>/
  ├── README.md                    # Project documentation
  └── <project_name>.mdl          # Main MDL file with template code

📄 Template Content:
===================

The generated MDL file includes:

📋 Pack Declaration:
```mdl
pack {
  name: "project_name"
  format: 82
  description: "Generated by MDL CLI"
}
```

🔧 Example Functions:
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

🎯 Features:
===========

• Complete project setup - Ready-to-use structure
• Template code - Working examples to learn from
• Proper pack metadata - Correct pack.mcmeta configuration
• Documentation - README with usage instructions
• Best practices - Follows MDL conventions

🚀 Getting Started:
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

💡 Tips:
========

• Use descriptive project names - They become your namespace
• Start with the template code - It demonstrates key MDL features
• Check your code regularly - Use `mdl check` during development
• Use version control - Git is great for tracking changes
• Read the documentation - Learn about all available features

📚 Next Steps:
=============

• Language Reference: https://www.mcmdl.com/docs/language-reference
• Examples: https://www.mcmdl.com/docs/examples
• CLI Reference: https://www.mcmdl.com/docs/cli-reference

For more information, visit: https://www.mcmdl.com/docs/cli-reference#new
""")
