---
layout: default
title: Minecraft Datapack Language (MDL)
---

# <img src="{{ site.baseurl }}/icons/icon-128.png" width="48" height="48" alt="MDL Icon" style="vertical-align: middle; margin-right: 12px;"> Minecraft Datapack Language (MDL)

A **modern JavaScript-style compiler** that lets you write Minecraft datapacks with **real control structures, variables, and expressions** that actually work.

## Quick Navigation

<div class="docs-grid">
  <div class="doc-card">
    <h3>📥 Downloads</h3>
    <p>Get the latest version and VS Code extension</p>
    <div class="doc-meta">
      <span class="category">Download</span>
      <span class="category">Install</span>
    </div>
    <a href="{{ site.baseurl }}/downloads/" class="doc-link">Download Now →</a>
  </div>
  <div class="doc-card">
    <h3>🚀 Getting Started</h3>
    <p>Install and create your first datapack</p>
    <div class="doc-meta">
      <span class="category">Beginner</span>
      <span class="category">Setup</span>
    </div>
    <a href="{{ site.baseurl }}/docs/getting-started/" class="doc-link">Get Started →</a>
  </div>
  <div class="doc-card">
    <h3>📖 Language Reference</h3>
    <p>Complete MDL syntax guide</p>
    <div class="doc-meta">
      <span class="category">Reference</span>
      <span class="category">Syntax</span>
    </div>
    <a href="{{ site.baseurl }}/docs/language-reference/" class="doc-link">Learn MDL →</a>
  </div>
  <div class="doc-card">
    <h3>📚 Examples</h3>
    <p>Working examples of all features</p>
    <div class="doc-meta">
      <span class="category">Examples</span>
      <span class="category">Code</span>
    </div>
    <a href="{{ site.baseurl }}/docs/examples/" class="doc-link">View Examples →</a>
  </div>
  <div class="doc-card">
    <h3>💻 CLI Reference</h3>
    <p>Command-line tool usage</p>
    <div class="doc-meta">
      <span class="category">Tools</span>
      <span class="category">CLI</span>
    </div>
    <a href="{{ site.baseurl }}/docs/cli-reference/" class="doc-link">CLI Guide →</a>
  </div>
  <div class="doc-card">
    <h3>🔧 VS Code Extension</h3>
    <p>IDE integration and features</p>
    <div class="doc-meta">
      <span class="category">IDE</span>
      <span class="category">VS Code</span>
    </div>
    <a href="{{ site.baseurl }}/docs/vscode-extension/" class="doc-link">VS Code →</a>
  </div>
  <div class="doc-card">
    <h3>📁 Multi-file Projects</h3>
    <p>Organize large projects</p>
    <div class="doc-meta">
      <span class="category">Advanced</span>
      <span class="category">Structure</span>
    </div>
    <a href="{{ site.baseurl }}/docs/multi-file-projects/" class="doc-link">Learn More →</a>
  </div>
  <div class="doc-card">
    <h3>🐍 Python Bindings</h3>
    <p>Programmatic datapack creation</p>
    <div class="doc-meta">
      <span class="category">API</span>
      <span class="category">Python</span>
    </div>
    <a href="{{ site.baseurl }}/docs/python-bindings/" class="doc-link">Python Bindings →</a>
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
    <p>Syntax highlighting, error checking, and quick compile with our VS Code extension</p>
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
pack "My First Pack" "A simple example" 82;
namespace "example";

var num counter<@s> = 0;

function example:hello {
    say "Hello, Minecraft!";
    tellraw @a {"text":"Welcome to my datapack!","color":"green"};
    counter<@s> = $counter<@s>$ + 1;
    say "Counter: $counter<@s>$";
}

on_load example:hello;
```

### Build and Run

```bash
# Build the datapack
mdl build --mdl hello.mdl -o dist

# Copy to Minecraft world
# Copy dist/my_first_pack/ to your world's datapacks folder
# Run /reload in-game
```

## Why MDL?

### Traditional Datapacks vs MDL

**Traditional Minecraft Functions:**
```mcfunction
# Hard to read and maintain
scoreboard players add @s counter 1
execute if score @s counter matches 5.. run say High counter!
execute unless score @s counter matches 5.. run say Low counter!
```

**MDL:**
```mdl
// Clean, readable, and maintainable
counter<@s> = $counter<@s>$ + 1;
if $counter<@s>$ > 5 {
    say "High counter!";
} else {
    say "Low counter!";
}
```

### Key Benefits

- **🎯 Familiar Syntax**: JavaScript-style with curly braces and semicolons
- **🔄 Real Control Flow**: If/else statements and loops that actually work
- **🔢 Variables**: Number variables with expressions and arithmetic
- **📁 Organization**: Multi-file projects with proper namespace separation
- **⚡ Performance**: Efficient compilation to optimized Minecraft commands
- **🔧 Tooling**: VS Code extension with syntax highlighting and error checking
- **📚 Documentation**: Comprehensive guides and working examples

## Features

### Control Structures

Write real if/else statements and while loops:

```mdl
if $health<@s>$ < 10 {
    say Health is low!;
    effect give @s minecraft:regeneration 10 1;
} else if "$health$ < 20" {
    say Health is moderate;
} else {
    say Health is good!;
}

while "$counter$ < 10" {
    say Counter: $counter$;
    counter = counter + 1;
}
```

### Variables and Expressions

Use number variables with arithmetic operations:

```mdl
var num player_health = 20;
var num damage = 5;
var num final_damage = damage * 2;

player_health = player_health - final_damage;
say Health: $player_health$;
```

### Multi-file Projects

Organize large projects across multiple files:

```mdl
// main.mdl
pack "My Game" description "A complete game" pack_format 82;
namespace "game";
// Main game logic

// ui.mdl (no pack declaration needed)
namespace "ui";
// User interface code

// combat.mdl (no pack declaration needed)
namespace "combat";
// Combat system code
```

### Registry Support

Reference external JSON files for all Minecraft registry types:

```mdl
recipe "custom_sword" "recipes/sword.json";
loot_table "treasure" "loot_tables/treasure.json";
advancement "first_sword" "advancements/sword.json";
```

## Getting Started

1. **Install MDL**: `pipx install minecraft-datapack-language`
2. **Create your first datapack**: Follow the [Getting Started Guide]({{ site.baseurl }}/docs/getting-started/)
3. **Learn the language**: Check the [Language Reference]({{ site.baseurl }}/docs/language-reference/)
4. **See examples**: Explore [Working Examples]({{ site.baseurl }}/docs/examples/)
5. **Build projects**: Use [Multi-file Projects]({{ site.baseurl }}/docs/multi-file-projects/)

## Community

- **Website**: [www.mcmdl.com](https://www.mcmdl.com)
- **GitHub**: [Source Code](https://github.com/aaron777collins/MinecraftDatapackLanguage)
- **Issues**: [Report Bugs](https://github.com/aaron777collins/MinecraftDatapackLanguage/issues)
- **Discussions**: [Ask Questions](https://github.com/aaron777collins/MinecraftDatapackLanguage/discussions)
- **Contributing**: [Help Improve MDL]({{ site.baseurl }}/docs/contributing/)

## License

MDL is open source software licensed under the MIT License. See the [LICENSE](https://github.com/aaron777collins/MinecraftDatapackLanguage/blob/main/LICENSE) file for details.

<style>
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.doc-card {
  background: #ffffff;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

.doc-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.doc-card h3 {
  margin: 0 0 0.5rem 0;
  color: #24292e;
  font-size: 1.1rem;
}

.doc-card p {
  margin: 0 0 1rem 0;
  color: #586069;
  line-height: 1.5;
}

.doc-meta {
  margin-bottom: 1rem;
}

.category {
  display: inline-block;
  background: #f1f3f4;
  color: #586069;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-right: 0.5rem;
  margin-bottom: 0.25rem;
}

.doc-link {
  display: inline-block;
  color: #0366d6;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: 1px solid #0366d6;
  border-radius: 6px;
  transition: background-color 0.2s, color 0.2s;
}

.doc-link:hover {
  background: #0366d6;
  color: #ffffff;
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
  border-radius: 8px;
  background: #f6f8fa;
  position: relative;
  transition: all 0.2s ease;
}

.feature:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
  .docs-grid {
    grid-template-columns: 1fr;
  }
}

[data-theme="dark"] .install-code code {
  background: #21262d;
}

</style>
