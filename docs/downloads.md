---
layout: page
title: Downloads
permalink: /downloads/
---

# Downloads

Get the latest version of Minecraft Datapack Language (MDL) and the VS Code extension.

## Latest Release

<div class="download-section">
  {% assign latest_release = site.github.releases | first %}
  <h2>🎯 Version {% if latest_release and latest_release.tag_name %}{{ latest_release.tag_name | remove: 'v' }}{% elsif site.github.latest_release and site.github.latest_release.tag_name %}{{ site.github.latest_release.tag_name | remove: 'v' }}{% else %}{{ site.github.project_version | default: site.data.version.current | default: site.title }}{% endif %}</h2>
  <p class="release-date">Released: {% if latest_release and latest_release.published_at %}{{ latest_release.published_at | date: "%B %d, %Y" }}{% elsif site.github.latest_release and site.github.latest_release.published_at %}{{ site.github.latest_release.published_at | date: "%B %d, %Y" }}{% else %}Latest{% endif %}</p>
  
  <div class="download-grid">
    <div class="download-card">
      <h3>🐍 Python Package</h3>
      <p>Install via pip or pipx for command-line usage</p>
      <div class="download-buttons">
        <a href="https://pypi.org/project/minecraft-datapack-language/" class="btn btn-primary" target="_blank">
          📦 View on PyPI
        </a>
        <a href="{% if latest_release %}{{ latest_release.html_url }}{% else %}https://github.com/{{ site.github_username }}/{{ site.github_repo }}/releases/latest{% endif %}" class="btn btn-secondary" target="_blank">
          📥 Download Source
        </a>
      </div>
      <div class="install-code">
        <code>pipx install minecraft-datapack-language</code>
      </div>
    </div>
    
    <div class="download-card">
      <h3>🔧 VS Code Extension</h3>
      <p>Syntax highlighting, linting, and build commands for VS Code/Cursor</p>
      <div class="download-buttons">
        {% assign release = latest_release | default: site.github.latest_release %}
        {% assign vsix = nil %}
        {% if release and release.assets %}
        {% for asset in release.assets %}
        {% if asset.name contains '.vsix' %}
        {% assign vsix = asset %}
        {% break %}
        {% endif %}
        {% endfor %}
        {% endif %}
        {% if vsix %}
        <a href="{{ vsix.browser_download_url }}" class="btn btn-primary">
          📥 Download VSIX
        </a>
        {% else %}
        <a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/releases/latest" class="btn btn-primary" target="_blank">
          📥 Download VSIX
        </a>
        {% endif %}
        <a href="{% if latest_release %}{{ latest_release.html_url }}{% else %}https://github.com/{{ site.github_username }}/{{ site.github_repo }}/releases/latest{% endif %}" class="btn btn-secondary" target="_blank">
          📋 View Release
        </a>
      </div>
      <div class="install-code">
        <code>Install from VSIX in VS Code/Cursor</code>
      </div>
    </div>
  </div>
</div>

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
```

#### Option 3: From Source
```bash
# Clone the repository
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage

# Install in development mode
python -m pip install -e .
```

### VS Code Extension

1. Download the `.vsix` file from the latest release
2. In VS Code/Cursor, go to Extensions (Ctrl+Shift+X)
3. Click the "..." menu and select "Install from VSIX..."
4. Choose the downloaded file
5. Restart VS Code/Cursor

## Features

### Command Line Tool
- **Build datapacks**: `mdl build --mdl file.mdl -o dist`
- **Lint code**: `mdl lint file.mdl`
- **Create projects**: `mdl new project_name`
- **Multi-file support**: Build entire directories
- **Pack format support**: Modern and legacy formats

### VS Code Extension
- **Syntax highlighting**: MDL files with proper colors
- **Error detection**: Real-time linting and validation
- **Build commands**: Quick compile with Ctrl+Shift+P
- **IntelliSense**: Auto-completion and suggestions
- **Integrated terminal**: Run MDL commands directly

## System Requirements

- **Python**: 3.8 or higher
- **Minecraft**: 1.20+ (pack format 82) or 1.19+ (pack format 15)
- **Operating System**: Windows, macOS, or Linux
- **VS Code**: 1.60+ (for extension)

## Version History

### Recent Releases

- **v12.0.10** - Namespace mapping fixes, improved multi-file support
- **v12.0.9** - Bug fixes and performance improvements
- **v12.0.8** - Enhanced error handling and documentation
- **v12.0.7** - Control structure improvements
- **v12.0.6** - Variable system enhancements

### Major Features

- **Modern Syntax**: JavaScript-style with curly braces and semicolons
- **Control Structures**: Real if/else statements and while loops
- **Variables**: Number variables with expressions and arithmetic
- **Multi-file Projects**: Organize code across multiple files
- **Registry Support**: All Minecraft registry types
- **VS Code Integration**: Full IDE support with extension

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

.release-date {
  color: #586069;
  font-style: italic;
  margin-bottom: 1.5rem;
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
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.download-card h3 {
  margin-top: 0;
  color: #24292e;
  font-size: 1.3rem;
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
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.btn-secondary {
  background: #f6f8fa;
  color: #24292e;
  border: 1px solid #e1e4e8;
}

.btn-secondary:hover {
  background: #e1e4e8;
  text-decoration: none;
}

.btn-outline {
  background: transparent;
  color: #0366d6;
  border: 1px solid #0366d6;
}

.btn-outline:hover {
  background: #0366d6;
  color: white;
  text-decoration: none;
}

.install-code {
  background: #f6f8fa;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #e1e4e8;
  margin-top: 1rem;
}

.install-code code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  color: #24292e;
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
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
