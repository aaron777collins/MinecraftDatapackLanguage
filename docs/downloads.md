---
layout: page
title: Downloads
permalink: /downloads/
---

Get the latest version of Minecraft Datapack Language (MDL) and the VS Code extension.

## Latest Release

<div class="download-section">
  <h2>🎯 Latest Version</h2>
  <p class="release-date">Check GitHub for the most up-to-date version information</p>
  
  <div class="download-grid">
    <div class="download-card">
      <h3>🐍 Python Package</h3>
      <p>Install via pip or pipx for command-line usage</p>
      <div class="download-buttons">
        <a href="https://pypi.org/project/minecraft-datapack-language/" class="btn btn-primary" target="_blank">
          📦 View on PyPI
        </a>
        <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest" class="btn btn-secondary" target="_blank">
          📥 Download Source
        </a>
      </div>
      <div class="install-code">
        <code>pipx install minecraft-datapack-language</code>
      </div>
    </div>
    
    <div class="download-card">
      <h3>🔧 VS Code Extension</h3>
      <p>Syntax highlighting, error checking, and build commands for VS Code/Cursor</p>
      <div class="download-buttons">
        <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest" class="btn btn-primary" target="_blank">
          📥 Download VSIX
        </a>
        <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases" class="btn btn-secondary" target="_blank">
          📋 View All Releases
        </a>
      </div>
      <div class="install-code">
        <code>Install from VSIX in VS Code/Cursor</code>
      </div>
    </div>
  </div>
</div>

## How to Get the Latest Version

### For Python Package
1. **Check PyPI**: Visit [PyPI project page](https://pypi.org/project/minecraft-datapack-language/) for the latest version
2. **Install**: Use `pipx install minecraft-datapack-language` to get the latest version
3. **Update**: Use `pipx upgrade minecraft-datapack-language` to update to the latest version

### For VS Code Extension
1. **Check Releases**: Visit [GitHub Releases](https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest)
2. **Download**: Look for the `.vsix` file in the latest release
3. **Install**: Follow the installation instructions below

## Installation Methods

### Python Package

#### Option 1: pipx (Recommended)
```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install MDL
pipx install minecraft-datapack-language

# Verify installation
mdl --help

# Update to latest version
pipx upgrade minecraft-datapack-language
```

#### Option 2: pip (Virtual Environment)
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1

# Install MDL
pip install minecraft-datapack-language

# Verify installation
mdl --help

# Update to latest version
pip install --upgrade minecraft-datapack-language
```

#### Option 3: From Source
```bash
# Clone the repository
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage

# Install in development mode
python -m pip install -e .

# Update from source
git pull origin main
```

### VS Code Extension

1. **Download**: Go to [GitHub Releases](https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest) and download the `.vsix` file
2. **Install**: In VS Code/Cursor, go to Extensions (Ctrl+Shift+X)
3. **Install from VSIX**: Click the "..." menu and select "Install from VSIX..."
4. **Choose file**: Select the downloaded `.vsix` file
5. **Restart**: Restart VS Code/Cursor to activate the extension

## Features

### Command Line Tool
- **Build datapacks**: `mdl build --mdl file.mdl -o dist`
- **Check code**: `mdl check file.mdl`
- **Create projects**: `mdl new project_name`
- **Multi-file support**: Build entire directories
- **Pack format support**: Modern and legacy formats

### VS Code Extension
- **Syntax highlighting**: MDL files with proper colors
- **Error detection**: Real-time error checking and validation
- **Build commands**: Quick compile with Ctrl+Shift+P
- **IntelliSense**: Auto-completion and suggestions
- **Integrated terminal**: Run MDL commands directly

## System Requirements

- **Python**: 3.8 or higher
- **Minecraft**: 1.20+ (pack format 82) or 1.19+ (pack format 15)
- **Operating System**: Windows, macOS, or Linux
- **VS Code**: 1.60+ (for extension)

## Version Information

To check the current version you have installed:

```bash
# Check Python package version
mdl --version

# Or check via pip
pip show minecraft-datapack-language
```

For the latest version information and release notes, visit:
- **GitHub Releases**: [Latest Release](https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest)
- **PyPI**: [Package Page](https://pypi.org/project/minecraft-datapack-language/)

## Getting Started

After installation, create your first datapack:

```bash
# Create a new project
mdl new my_first_pack

# Build it
mdl build --mdl my_first_pack.mdl -o dist

# Install in Minecraft
# Copy dist/my_first_pack/ to your world's datapacks folder
# Run /reload in-game
```

## Support

- **Documentation**: [Getting Started]({{ site.baseurl }}/docs/getting-started/)
- **Examples**: [Working Examples]({{ site.baseurl }}/docs/examples/)
- **Language Reference**: [Complete Syntax]({{ site.baseurl }}/docs/language-reference/)
- **Website**: [www.mcmdl.com](https://www.mcmdl.com)
- **GitHub Issues**: [Report Bugs](https://github.com/aaron777collins/MinecraftDatapackLanguage/issues)
- **Discussions**: [Ask Questions](https://github.com/aaron777collins/MinecraftDatapackLanguage/discussions)

## Contributing

Want to help improve MDL? Check out our [Contributing Guide]({{ site.baseurl }}/docs/contributing/) for:

- Development setup
- Code style guidelines
- Testing procedures
- Release process

## License

MDL is open source software licensed under the MIT License. See the [LICENSE](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/LICENSE) file for details.

<style>
.download-section {
  margin: 2rem 0;
  padding: 2rem;
  background: #f6f8fa;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
}

[data-theme="dark"] .download-section {
  background: #161b22;
  border-color: #30363d;
}

.release-date {
  color: #586069;
  font-style: italic;
  margin-bottom: 1.5rem;
}

[data-theme="dark"] .release-date {
  color: #8b949e;
}

.download-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.download-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

[data-theme="dark"] .download-card {
  background: #21262d;
  border-color: #30363d;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.download-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

[data-theme="dark"] .download-card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.download-card h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.3rem;
}

[data-theme="dark"] .download-card h3 {
  color: #e6edf3;
}

.download-card p {
  color: #586069;
}

[data-theme="dark"] .download-card p {
  color: #c9d1d9;
}

.download-buttons {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #0366d6;
  color: white;
}

.btn-primary:hover {
  background: #0256b3;
  text-decoration: none;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

.btn-secondary {
  background: #f6f8fa;
  color: #24292e;
  border: 1px solid #e1e4e8;
}

[data-theme="dark"] .btn-secondary {
  background: #21262d;
  color: #e6edf3;
  border-color: #30363d;
}

.btn-secondary:hover {
  background: #e1e4e8;
  text-decoration: none;
}

[data-theme="dark"] .btn-secondary:hover {
  background: #30363d;
}

.btn-outline {
  background: transparent;
  color: #0366d6;
  border: 1px solid #0366d6;
}

[data-theme="dark"] .btn-outline {
  color: #58a6ff;
  border-color: #58a6ff;
}

.btn-outline:hover {
  background: #0366d6;
  color: white;
  text-decoration: none;
}

[data-theme="dark"] .btn-outline:hover {
  background: #58a6ff;
  color: #0d1117;
}

.install-code {
  background: #f6f8fa;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #e1e4e8;
  margin-top: 1rem;
}

[data-theme="dark"] .install-code {
  background: #21262d;
  border-color: #30363d;
}

.install-code code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  color: #24292e;
}

[data-theme="dark"] .install-code code {
  color: #e6edf3;
}

.releases-section {
  margin: 3rem 0;
}

.release-list {
  display: grid;
  gap: 1rem;
  margin: 1.5rem 0;
}

.release-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

.release-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.release-item h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.2rem;
}

.release-item a {
  color: #0366d6;
  text-decoration: none;
  font-weight: 500;
}

.release-item a:hover {
  text-decoration: underline;
}

.release-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.asset-count {
  color: #586069;
  font-size: 0.9rem;
}

.view-all {
  text-align: center;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .download-grid {
    grid-template-columns: 1fr;
  }
  
  .download-buttons {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
  
  .release-links {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
}
</style>
