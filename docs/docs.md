---
layout: page
title: Documentation
permalink: /docs/
---

# Documentation

Welcome to the Minecraft Datapack Language (MDL) documentation. Here you'll find everything you need to get started with creating Minecraft datapacks using MDL.

## Getting Started

<div class="doc-section">
  <h2>🚀 Getting Started</h2>
  <p>New to MDL? Start here to learn the basics and create your first datapack.</p>
  <a href="{{ site.baseurl }}/docs/getting-started/" class="doc-link">Get Started →</a>
</div>

## Core Documentation

<div class="doc-grid">
  <div class="doc-card">
    <h3>📖 Language Reference</h3>
    <p>Complete guide to MDL syntax, commands, and language features.</p>
    <a href="{{ site.baseurl }}/docs/language-reference/" class="doc-link">Learn MDL →</a>
  </div>
  
  <div class="doc-card">
    <h3>🐍 Python API</h3>
    <p>Programmatically create datapacks using the Python API.</p>
    <a href="{{ site.baseurl }}/docs/python-api/" class="doc-link">Python API →</a>
  </div>
  
  <div class="doc-card">
    <h3>💻 CLI Reference</h3>
    <p>Command-line tool usage and options.</p>
    <a href="{{ site.baseurl }}/docs/cli-reference/" class="doc-link">CLI Guide →</a>
  </div>
</div>

## Tools & Extensions

<div class="doc-grid">
  <div class="doc-card">
    <h3>🔧 VS Code Extension</h3>
    <p>IDE integration with syntax highlighting, linting, and build commands.</p>
    <a href="{{ site.baseurl }}/docs/vscode-extension/" class="doc-link">VS Code →</a>
  </div>
  
  <div class="doc-card">
    <h3>📁 Multi-file Projects</h3>
    <p>Organize large datapacks across multiple files with automatic merging.</p>
    <a href="{{ site.baseurl }}/docs/multi-file-projects/" class="doc-link">Multi-file →</a>
  </div>
</div>

## Examples & Resources

<div class="doc-section">
  <h2>📚 Examples</h2>
  <p>Complete working examples to learn from and use as templates.</p>
  <a href="{{ site.baseurl }}/docs/examples/" class="doc-link">View Examples →</a>
</div>

<div class="doc-section">
  <h2>🤝 Contributing</h2>
  <p>Want to contribute to MDL? Learn how to get involved.</p>
  <a href="{{ site.baseurl }}/docs/contributing/" class="doc-link">Contribute →</a>
</div>

## Quick Reference

### Installation
```bash
# Using pipx (recommended)
pipx install minecraft-datapack-language

# Or using pip
pip install minecraft-datapack-language
```

### Basic Usage
```bash
# Build from MDL file
mdl build --mdl mypack.mdl -o dist

# Build from Python script
mdl build --python mypack.py -o dist
```

### Key Features
- **Simple Language**: Write datapacks in `.mdl` files
- **Python API**: Programmatic datapack creation
- **Multi-file Support**: Organize large projects
- **VS Code Integration**: Syntax highlighting and build commands
- **1.21+ Ready**: Automatic handling of new datapack structure

<style>
.doc-section {
  margin: 2rem 0;
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background: #f6f8fa;
}

.doc-section h2 {
  margin-top: 0;
  color: #24292e;
}

.doc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.doc-card {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s;
}

.doc-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.doc-card h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.2rem;
}

.doc-card p {
  margin: 0.5rem 0 1rem 0;
  color: #586069;
}

.doc-link {
  display: inline-flex;
  align-items: center;
  color: #0366d6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.doc-link:hover {
  color: #0256b3;
  text-decoration: none;
}

@media (max-width: 768px) {
  .doc-grid {
    grid-template-columns: 1fr;
  }
  
  .doc-card {
    padding: 1rem;
  }
}
</style>
