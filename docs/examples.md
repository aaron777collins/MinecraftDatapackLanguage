---
layout: page
title: Examples
description: Complete examples and templates for the Minecraft Datapack Language (MDL)
---

# Examples

Explore complete, working examples of MDL projects to learn from and use as templates for your own datapacks.

## Getting Started Examples

### Basic Datapack
A simple datapack that demonstrates the fundamental concepts of MDL.

```mdl
pack "basic_example" {
    description = "A basic MDL datapack example"
    pack_format = 21
}

function "load" {
    say "Basic datapack loaded!"
}

function "tick" {
    execute as @a at @s run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1
}
```

### Hello World
The classic "Hello World" example showing basic function creation.

```mdl
pack "hello_world" {
    description = "Simple hello world example"
    pack_format = 21
}

function "greet" {
    tellraw @a {"text": "Hello from MDL!", "color": "green"}
}
```

## Advanced Examples

### Multi-file Project
See how to organize larger projects across multiple files in the [multi-file example](/examples/multi_file_example/).

### Combat System
A complete combat enhancement system with multiple functions and features.

### Timer System
Demonstrates advanced timing and scheduling capabilities.

### UI System
Shows how to create custom user interfaces and HUD elements.

## Example Categories

<div class="example-grid">
  <div class="example-card">
    <h3>🎯 Basic Examples</h3>
    <p>Simple examples to get you started with MDL fundamentals.</p>
    <ul>
      <li>Hello World</li>
      <li>Basic Functions</li>
      <li>Simple Commands</li>
    </ul>
  </div>
  
  <div class="example-card">
    <h3>🏗️ Project Structure</h3>
    <p>Examples showing how to organize larger MDL projects.</p>
    <ul>
      <li>Multi-file Projects</li>
      <li>Modular Design</li>
      <li>File Organization</li>
    </ul>
  </div>
  
  <div class="example-card">
    <h3>⚔️ Gameplay Systems</h3>
    <p>Complete gameplay enhancement systems.</p>
    <ul>
      <li>Combat Systems</li>
      <li>Timer Systems</li>
      <li>Custom Mechanics</li>
    </ul>
  </div>
  
  <div class="example-card">
    <h3>🎨 User Interface</h3>
    <p>Custom UI and HUD examples.</p>
    <ul>
      <li>Custom HUDs</li>
      <li>Scoreboard Displays</li>
      <li>Interactive Menus</li>
    </ul>
  </div>
  
  <div class="example-card">
    <h3>🔧 Utility Functions</h3>
    <p>Reusable utility functions and helpers.</p>
    <ul>
      <li>Math Functions</li>
      <li>String Manipulation</li>
      <li>Data Structures</li>
    </ul>
  </div>
  
  <div class="example-card">
    <h3>🎮 Mini-Games</h3>
    <p>Complete mini-game implementations.</p>
    <ul>
      <li>Simple Games</li>
      <li>Score Systems</li>
      <li>Game States</li>
    </ul>
  </div>
</div>

## Running Examples

To run any of these examples:

1. **Download the example files**
2. **Build the datapack:**
   ```bash
   mdl build --mdl example.mdl -o dist
   ```
3. **Install in your Minecraft world:**
   - Copy the generated datapack to your world's `datapacks` folder
   - Enable it in-game with `/reload`

## Contributing Examples

Have a great example to share? We'd love to include it! See our [Contributing Guide](/docs/contributing/) for how to submit examples.

## Example Repository

All examples are available in our [GitHub repository](https://github.com/{{ site.github_username }}/{{ site.github_repo }}/tree/main/examples) where you can:

- Browse the source code
- Download complete examples
- Submit your own examples
- Report issues or suggest improvements

<style>
.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.example-card {
  background: #ffffff;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.example-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.example-card h3 {
  margin: 0 0 0.5rem 0;
  color: #24292e;
  font-size: 1.1rem;
}

.example-card p {
  margin: 0 0 1rem 0;
  color: #586069;
  line-height: 1.5;
}

.example-card ul {
  margin: 0;
  padding-left: 1.2rem;
  color: #586069;
}

.example-card li {
  margin: 0.25rem 0;
}

@media (max-width: 768px) {
  .example-grid {
    grid-template-columns: 1fr;
  }
}
</style>
