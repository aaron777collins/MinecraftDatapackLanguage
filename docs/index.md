---
layout: default
title: Minecraft Datapack Language (MDL)
---

# <img src="{{ site.baseurl }}/icons/icon-128.png" width="48" height="48" alt="MDL Icon" style="vertical-align: middle; margin-right: 12px;"> Minecraft Datapack Language (MDL)

A tiny compiler that lets you write Minecraft datapacks in a simple language (`.mdl`) **or** via a clean Python API, and then compiles to the correct 1.21+ datapack folder layout automatically.

## Quick Navigation

<div class="quick-nav">
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="Download" class="nav-icon">
    <h3>📥 Downloads</h3>
    <p>Get the latest version and VS Code extension</p>
    <a href="{{ site.baseurl }}/downloads/" class="nav-link">Download Now →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="Getting Started" class="nav-icon">
    <h3>🚀 Getting Started</h3>
    <p>Install and create your first datapack</p>
    <a href="{{ site.baseurl }}/docs/getting-started/" class="nav-link">Get Started →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="Language Reference" class="nav-icon">
    <h3>📖 Language Reference</h3>
    <p>Complete MDL syntax guide</p>
    <a href="{{ site.baseurl }}/docs/language-reference/" class="nav-link">Learn MDL →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="Python API" class="nav-icon">
    <h3>🐍 Python API</h3>
    <p>Programmatic datapack creation</p>
    <a href="{{ site.baseurl }}/docs/python-api/" class="nav-link">Python API →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="CLI Reference" class="nav-icon">
    <h3>💻 CLI Reference</h3>
    <p>Command-line tool usage</p>
    <a href="{{ site.baseurl }}/docs/cli-reference/" class="nav-link">CLI Guide →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="VS Code Extension" class="nav-icon">
    <h3>🔧 VS Code Extension</h3>
    <p>IDE integration and features</p>
    <a href="{{ site.baseurl }}/docs/vscode-extension/" class="nav-link">VS Code →</a>
  </div>
  <div class="nav-card">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="32" height="32" alt="Examples" class="nav-icon">
    <h3>📚 Examples</h3>
    <p>Complete working examples</p>
    <a href="{{ site.baseurl }}/docs/examples/" class="nav-link">View Examples →</a>
  </div>
</div>

<div class="features">
  <div class="feature">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="24" height="24" alt="Easy to Use" class="feature-icon">
    <h3>🚀 Easy to Use</h3>
    <p>Write datapacks in a simple, readable language or use a clean Python API</p>
  </div>
  <div class="feature">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="24" height="24" alt="1.21+ Ready" class="feature-icon">
    <h3>⚡ 1.21+ Ready</h3>
    <p>Handles directory renames from snapshots 24w19a and 24w21a automatically</p>
  </div>
  <div class="feature">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="24" height="24" alt="VS Code Support" class="feature-icon">
    <h3>🔧 VS Code Support</h3>
    <p>Syntax highlighting, linting, and quick compile with our VS Code extension</p>
  </div>
  <div class="feature">
    <img src="{{ site.baseurl }}/icons/icon-64.png" width="24" height="24" alt="Multi-file Support" class="feature-icon">
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
# hello.mdl
pack "My First Pack" description "A simple example" pack_format 48

namespace "example"

function "hello":
    say Hello, Minecraft!
    tellraw @a {"text":"Welcome to my datapack!","color":"green"}

on_load "example:hello"
```

### Build and Use

```bash
mdl build --mdl hello.mdl -o dist
# Copy dist/mypack/ to your world's datapacks folder
```

## Key Features

- **Simple Language**: Write datapacks in `.mdl` files with clear syntax
- **Python API**: Programmatically create datapacks using Python
- **Multi-file Projects**: Organize large datapacks across multiple files
- **VS Code Integration**: Syntax highlighting, linting, and build commands
- **1.21+ Compatibility**: Automatic handling of new datapack structure
- **Function Tags**: Easy integration with `minecraft:tick` and `minecraft:load`
- **Multiple Tag Types**: Support for function, item, block, entity, fluid, and game event tags

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

.nav-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.nav-card:hover .nav-icon {
  opacity: 1;
}

.nav-card h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.2rem;
  padding-right: 2.5rem;
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

.feature-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  opacity: 0.6;
}

.feature h3 {
  margin-top: 0;
  color: #24292e;
  padding-right: 2rem;
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
  
  .nav-icon {
    position: static;
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .nav-card h3 {
    padding-right: 0;
  }
  
  .feature-icon {
    position: static;
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .feature h3 {
    padding-right: 0;
  }
}
</style>
