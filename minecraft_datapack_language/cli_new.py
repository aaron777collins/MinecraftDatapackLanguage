"""
CLI New Project - Create new MDL projects with templates
"""

import os
import shutil
from pathlib import Path
from typing import Optional

from .cli_utils import _slugify


def create_new_project(project_name: str, pack_name: str = None, pack_format: int = 82) -> None:
    """Create a new MDL project with template files."""
    # Validate project name
    if not project_name or not project_name.strip():
        raise ValueError("Project name cannot be empty")
    
    # Clean and validate project name
    clean_name = _slugify(project_name.strip())
    if not clean_name:
        raise ValueError("Project name must contain valid characters")
    
    # Use pack_name if provided, otherwise use project name
    if pack_name is None:
        pack_name = project_name
    
    # Validate pack format
    if not isinstance(pack_format, int) or pack_format < 1:
        raise ValueError("Pack format must be a positive integer")
    
    # Create project directory
    project_dir = Path(clean_name)
    if project_dir.exists():
        raise ValueError(f"Project directory '{clean_name}' already exists")
    
    try:
        # Create the project directory
        project_dir.mkdir(parents=True, exist_ok=False)
        
        # Create the main MDL file
        mdl_file = project_dir / "main.mdl"
        
        # Generate template content
        template_content = _generate_mdl_template(clean_name, pack_name, pack_format)
        
        with open(mdl_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # Create README.md
        readme_content = _generate_readme_template(clean_name, pack_name)
        readme_file = project_dir / "README.md"
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"[OK] Successfully created new MDL project: {clean_name}")
        print(f"[DIR] Project directory: {project_dir.absolute()}")
        print(f"[FILE] Main file: {mdl_file}")
        print(f"[DOC] Documentation: {readme_file}")
        print()
        print("[NEXT] Next steps:")
        print(f"  1. cd {clean_name}")
        print(f"  2. Edit main.mdl with your code")
        print(f"  3. mdl build --mdl main.mdl -o dist")
        print(f"  4. mdl check main.mdl")
        print()
        print("[INFO] Learn more:")
        print("   • Language Reference: https://www.mcmdl.com/docs/language-reference")
        print("   • Examples: https://www.mcmdl.com/docs/examples")
        print("   • CLI Reference: https://www.mcmdl.com/docs/cli-reference")
    
    except Exception as e:
        # Clean up on error
        if project_dir.exists():
            shutil.rmtree(project_dir)
        raise ValueError(f"Failed to create project: {str(e)}")


def _generate_mdl_template(project_name: str, pack_name: str, pack_format: int) -> str:
    """Generate the MDL template content."""
    return f'''pack "{pack_name}" "A simple hello world datapack" {pack_format};
namespace "{project_name}";

function "main" {{
    say Hello, Minecraft!;
    tellraw @a {{"text":"Welcome to my datapack!","color":"green"}};
}}

on_load "{project_name}:main";
'''


def _generate_readme_template(project_name: str, pack_name: str) -> str:
    """Generate the README template content."""
    return f'''# {pack_name}

A Minecraft datapack created with MDL (Minecraft Datapack Language).

## [GAME] About

This datapack was generated using the MDL CLI tool. MDL is a simplified language for creating Minecraft datapacks with clean, readable syntax.

## [DIR] Project Structure

```
{project_name}/
├── README.md              # This file
└── main.mdl              # Main MDL source file with basic hello world example
```

## [NEXT] Getting Started

### Prerequisites

- Minecraft Java Edition (1.20+ recommended)
- MDL CLI tool installed (`pipx install minecraft-datapack-language`)

### Building the Datapack

1. **Build the project:**
   ```bash
   mdl build --mdl main.mdl -o dist
   ```

2. **Check for errors:**
   ```bash
   mdl check main.mdl
   ```

3. **Install in Minecraft:**
   - Copy the `dist` folder to your world's `datapacks` directory
   - Or use the `--wrapper` option to create a zip file:
     ```bash
     mdl build --mdl main.mdl -o dist --wrapper {project_name}
     ```

### Using the Datapack

1. Load your world in Minecraft
2. The datapack will automatically load
3. Run the main function: `/function {project_name}:main`

## [OPT] Development

### Editing the Code

Open `main.mdl` in your favorite text editor. The file contains:

- **Pack declaration** - Datapack metadata
- **Namespace** - Datapack namespace for organization
- **Functions** - The main logic of your datapack
- **on_load hook** - Automatically runs when the datapack loads

### Key Features

- **Functions**: Define reusable code blocks with `function "name" {{ ... }}`
- **Basic commands**: Use `say` and `tellraw` for player communication
- **Automatic loading**: The `on_load` hook runs your main function automatically
- **Clean syntax**: Simple, readable MDL syntax that compiles to Minecraft commands

### Example Code

```mdl
// Define a function
function "main" {{
    say Hello, Minecraft!;
    tellraw @a {{"text":"Welcome!","color":"green"}};
}}

// Hook it to run when loaded
on_load "{project_name}:main";
```

## [INFO] Resources

- **Language Reference**: https://www.mcmdl.com/docs/language-reference
- **CLI Reference**: https://www.mcmdl.com/docs/cli-reference
- **Examples**: https://www.mcmdl.com/docs/examples
- **Website**: https://www.mcmdl.com
- **GitHub**: https://github.com/aaron777collins/MinecraftDatapackLanguage

## 🐛 Troubleshooting

### Common Issues

1. **"No .mdl files found"**
   - Make sure you're in the correct directory
   - Check that the file has a `.mdl` extension

2. **Syntax errors**
   - Use `mdl check main.mdl` to find and fix errors
   - Check the error messages for line numbers and suggestions

3. **Datapack not loading**
   - Verify the pack format is correct for your Minecraft version
   - Check that the `dist` folder is in the right location

### Getting Help

- Check the error messages - they include helpful suggestions
- Visit the documentation: https://www.mcmdl.com/docs
- Report bugs: https://github.com/aaron777collins/MinecraftDatapackLanguage/issues

## [FILE] License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Happy coding! [GAME]
'''
