---
layout: page
title: Downloads
permalink: /downloads/
---

# Downloads

Get the latest version of Minecraft Datapack Language (MDL) and the VS Code extension.

## Latest Release

<div class="download-section">
  <h2>🎯 Version {% if site.github.latest_release.tag_name %}{{ site.github.latest_release.tag_name | remove: 'v' }}{% else %}{{ site.current_version }}{% endif %}</h2>
  <p class="release-date">Released: {% if site.github.latest_release.published_at %}{{ site.github.latest_release.published_at | date: "%B %d, %Y" }}{% else %}Latest{% endif %}</p>
  
  <div class="download-grid">
    <div class="download-card">
      <h3>🐍 Python Package</h3>
      <p>Install via pip or pipx for command-line usage</p>
      <div class="download-buttons">
        <a href="https://pypi.org/project/minecraft-datapack-language/" class="btn btn-primary" target="_blank">
          📦 View on PyPI
        </a>
        <a href="{{ site.github.latest_release.html_url }}" class="btn btn-secondary" target="_blank">
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
        {% assign vsix_asset = site.github.latest_release.assets | where: "name", "minecraft-datapack-language-*.vsix" | first %}
        {% if vsix_asset %}
        <a href="{{ vsix_asset.browser_download_url }}" class="btn btn-primary">
          📥 Download VSIX
        </a>
        {% else %}
        <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest" class="btn btn-primary" target="_blank">
          📥 Download VSIX
        </a>
        {% endif %}
        <a href="{{ site.github.latest_release.html_url }}" class="btn btn-secondary" target="_blank">
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
# Clone repository
git clone https://github.com/aaron777collins/MinecraftDatapackLanguage.git
cd MinecraftDatapackLanguage

# Install in development mode
python -m pip install -e .
```

### VS Code Extension

#### Quick Install
1. **Download the VSIX file** from the latest release
2. **Open VS Code/Cursor**
3. **Go to Extensions** (Ctrl+Shift+X)
4. **Click "..." → "Install from VSIX..."**
5. **Choose the downloaded `.vsix` file**

#### Command Line Install
```bash
# Install directly from command line
code --install-extension minecraft-datapack-language-{% if site.github.latest_release.tag_name %}{{ site.github.latest_release.tag_name | remove: 'v' }}{% else %}{{ site.current_version }}{% endif %}.vsix
```

#### Features Included
- ✅ **Syntax highlighting** for `.mdl` files
- ✅ **Real-time linting** with error detection
- ✅ **Build commands**: `MDL: Build current file`
- ✅ **Workspace validation**: `MDL: Check Workspace`
- ✅ **Command palette integration**

## Recent Releases

<div class="releases-section">
  <h2>📋 Recent Releases</h2>
  
  <div class="release-list">
    {% if site.github.releases.size > 0 %}
      {% for release in site.github.releases limit:5 %}
      <div class="release-item">
        <h3>{{ release.tag_name }}</h3>
        <p class="release-date">{{ release.published_at | date: "%B %d, %Y" }}</p>
        <p>{{ release.body | strip_html | truncate: 150 }}</p>
        <div class="release-links">
          <a href="{{ release.html_url }}" target="_blank">View Release →</a>
          {% if release.assets.size > 0 %}
          <span class="asset-count">📦 {{ release.assets.size }} asset{{ release.assets.size | pluralize }}</span>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    {% else %}
      <div class="release-item">
        <h3>Latest Version</h3>
        <p class="release-date">Current</p>
        <p>Check GitHub for the latest releases and updates.</p>
        <div class="release-links">
          <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases" target="_blank">View All Releases →</a>
        </div>
      </div>
    {% endif %}
  </div>
  
  <div class="view-all">
    <a href="https://github.com/aaron777collins/MinecraftDatapackLanguage/releases" class="btn btn-outline" target="_blank">
      View All Releases
    </a>
  </div>
</div>

## System Requirements

### Python Package
- **Python**: 3.9 or higher
- **Platform**: Windows, macOS, Linux
- **Dependencies**: Automatically installed via pip

### VS Code Extension
- **VS Code**: 1.90.0 or higher
- **Cursor**: Compatible (based on VS Code)
- **Platform**: Windows, macOS, Linux
- **MDL**: Requires MDL to be installed on system

## Getting Started

After installation, you can:

1. **Create your first datapack**:
   ```bash
   mdl new my_pack --name "My First Pack" --pack-format 48
   ```

2. **Build from MDL file**:
   ```bash
   mdl build --mdl mypack.mdl -o dist
   ```

3. **Use VS Code extension**:
   - Open any `.mdl` file for syntax highlighting
   - Use `Ctrl+Shift+P` and type "MDL" for commands

## Support

- **Documentation**: [Complete guides and examples]({{ site.baseurl }}/docs/)
- **GitHub Issues**: [Report bugs or request features](https://github.com/aaron777collins/MinecraftDatapackLanguage/issues)
- **Discussions**: [Ask questions and share projects](https://github.com/aaron777collins/MinecraftDatapackLanguage/discussions)

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
