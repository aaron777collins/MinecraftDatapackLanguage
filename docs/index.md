---
layout: default
title: Minecraft Datapack Language (MDL)
---

# <img src="{{ site.baseurl }}/icons/icon-128.png" width="48" height="48" alt="MDL Icon" style="vertical-align: middle; margin-right: 12px;"> Minecraft Datapack Language (MDL)

A **modern JavaScript-style compiler** that lets you write Minecraft datapacks with **real control structures, variables, and expressions** that actually work.

## Quick Navigation

<div class="quick-nav">
  <div class="nav-card">
    <h3>📥 Downloads</h3>
    <p>Get the latest version and VS Code extension</p>
    <a href="{{ site.baseurl }}/downloads/" class="nav-link">Download Now →</a>
  </div>
  <div class="nav-card">
    <h3>🚀 Getting Started</h3>
    <p>Install and create your first datapack</p>
    <a href="{{ site.baseurl }}/docs/getting-started/" class="nav-link">Get Started →</a>
  </div>
  <div class="nav-card">
    <h3>📖 Language Reference</h3>
    <p>Complete MDL syntax guide</p>
    <a href="{{ site.baseurl }}/docs/language-reference/" class="nav-link">Learn MDL →</a>
  </div>
  <div class="nav-card">
    <h3>🐍 Python API</h3>
    <p>Programmatic datapack creation</p>
    <a href="{{ site.baseurl }}/docs/python-api/" class="nav-link">Python API →</a>
  </div>
  <div class="nav-card">
    <h3>💻 CLI Reference</h3>
    <p>Command-line tool usage</p>
    <a href="{{ site.baseurl }}/docs/cli-reference/" class="nav-link">CLI Guide →</a>
  </div>
  <div class="nav-card">
    <h3>🔧 VS Code Extension</h3>
    <p>IDE integration and features</p>
    <a href="{{ site.baseurl }}/docs/vscode-extension/" class="nav-link">VS Code →</a>
  </div>
  <div class="nav-card">
    <h3>📚 Examples</h3>
    <p>Complete working examples</p>
    <a href="{{ site.baseurl }}/docs/examples/" class="nav-link">View Examples →</a>
  </div>
</div>

<div class="features">
  <div class="feature">
    <h3>🎯 JavaScript-Style Syntax</h3>
    <p>Write datapacks with modern curly braces, semicolons, and familiar syntax</p>
  </div>
  <div class="feature">
    <h3>🔄 Real Control Structures</h3>
    <p>Full if/else if/else statements and while loops that actually work</p>
  </div>
  <div class="feature">
    <h3>🔢 Variables & Expressions</h3>
    <p>Number variables with arithmetic operations and variable substitution</p>
  </div>
  <div class="feature">
    <h3>⚡ Modern Minecraft</h3>
    <p>Pack format 82 by default with latest Minecraft features</p>
  </div>
  <div class="feature">
    <h3>🔧 VS Code Support</h3>
    <p>Syntax highlighting, linting, and quick compile with our VS Code extension</p>
  </div>
  <div class="feature">
    <h3>📁 Multi-file Support</h3>
    <p>Organize large projects across multiple files with automatic merging</p>
  </div>
</div>

## Quick Start

### Install

```bash
# Using pipx (recommended)
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install minecraft-datapack-language

# Or using pip
pip install minecraft-datapack-language
```

### Create Your First Datapack

```mdl
// hello.mdl
pack "My First Pack" description "A simple example" pack_format 82;

namespace "example";

var num counter = 0;

function "hello" {
    say Hello, Minecraft!;
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter = counter + 1;
    say Counter: $counter$;
}

on_load "example:hello";
```

### Build and Use

```bash
mdl build --mdl hello.mdl -o dist
# Copy dist/mypack/ to your world's datapacks folder
```

## Key Features

- **🎯 JavaScript-Style Syntax**: Write datapacks with modern curly braces `{}` and semicolons `;`
- **🔄 Full Control Structures**: `if/else if/else` statements and `while` loops with method selection
- **🔢 Variables & Expressions**: Number variables with arithmetic operations and `$variable$` substitution
- **📝 Modern Comments**: Use `//` and `/* */` for comments
- **📁 Multi-file Projects**: Organize large datapacks across multiple files with automatic merging
- **🔧 VS Code Integration**: Syntax highlighting, linting, and build commands
- **⚡ Modern Minecraft**: Pack format 82 by default with latest features
- **🎨 Variable Optimization**: Automatic load function generation for initialization
- **🎯 Selector Optimization**: Proper `@a` usage for system commands
- **🏷️ Function Tags**: Easy integration with `minecraft:tick` and `minecraft:load`

## Documentation

- **[Getting Started]({{ site.baseurl }}/docs/getting-started/)** - Installation and first steps
- **[Language Reference]({{ site.baseurl }}/docs/language-reference/)** - Complete MDL syntax guide
- **[Python API]({{ site.baseurl }}/docs/python-api/)** - Programmatic datapack creation
- **[CLI Reference]({{ site.baseurl }}/docs/cli-reference/)** - Command-line tool usage
- **[VS Code Extension]({{ site.baseurl }}/docs/vscode-extension/)** - IDE integration
- **[Examples]({{ site.baseurl }}/docs/examples/)** - Complete working examples
- **[Multi-file Projects]({{ site.baseurl }}/docs/multi-file-projects/)** - Organizing large datapacks

## Community

- **GitHub**: [aaron777collins/MinecraftDatapackLanguage](https://github.com/aaron777collins/MinecraftDatapackLanguage)
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share your datapacks

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/LICENSE) file for details.

<style>
.quick-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.nav-card {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s;
  position: relative;
}

.nav-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.nav-card h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.2rem;
}

.nav-card p {
  margin: 0.5rem 0 1rem 0;
  color: #586069;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  color: #0366d6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #0256b3;
  text-decoration: none;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.feature {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  background: #f6f8fa;
  position: relative;
}

.feature h3 {
  margin-top: 0;
  color: #24292e;
}

.feature p {
  margin-bottom: 0;
  color: #586069;
}

@media (max-width: 768px) {
  .quick-nav {
    grid-template-columns: 1fr;
  }
  
  .nav-card {
    padding: 1rem;
  }
  

}
</style>
