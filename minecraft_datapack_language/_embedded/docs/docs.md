---
layout: page
title: Documentation
description: Complete documentation for the Minecraft Datapack Language (MDL)
---

Welcome to the complete documentation for the Minecraft Datapack Language (MDL). This guide will help you get started and master all aspects of MDL development.

## Getting Started

{% assign getting_started = site.nav | where: "title", "Getting Started" | first %}
- **[Getting Started]({{ getting_started.url }})** - Learn the basics of MDL and set up your development environment

## Core Documentation

{% assign language_ref = site.nav | where: "title", "Language Reference" | first %}
{% assign multi_file = site.nav | where: "title", "Multi-file Projects" | first %}
{% assign cli_ref = site.nav | where: "title", "CLI Reference" | first %}
{% assign python_api = site.nav | where: "title", "Python Bindings" | first %}

- **[Language Reference]({{ language_ref.url }})** - Complete syntax and language features
- **[Multi-file Projects]({{ multi_file.url }})** - How to organize and structure larger MDL projects
- **[CLI Reference]({{ cli_ref.url }})** - Command-line interface usage and options
- **[Python Bindings]({{ python_api.url }})** - Programmatic access to MDL functionality

## Tools and Extensions

{% assign vscode = site.nav | where: "title", "VS Code Extension" | first %}

- **[VS Code Extension]({{ vscode.url }})** - Enhanced development experience with syntax highlighting and IntelliSense

## Contributing

{% assign contributing = site.nav | where: "title", "Contributing" | first %}

- **[Contributing]({{ contributing.url }})** - How to contribute to the MDL project

## Quick Navigation

<div class="doc-grid">
  <div class="doc-card">
    <h3>🚀 Getting Started</h3>
    <p>New to MDL? Start here to learn the fundamentals and set up your environment.</p>
    <a href="{{ getting_started.url }}" class="doc-link">Get Started →</a>
  </div>
  
  <div class="doc-card">
    <h3>📚 Language Reference</h3>
    <p>Complete syntax reference, data types, functions, and language features.</p>
    <a href="{{ language_ref.url }}" class="doc-link">View Reference →</a>
  </div>
  
  <div class="doc-card">
    <h3>🔧 CLI Tools</h3>
    <p>Command-line interface for building, testing, and managing MDL projects.</p>
    <a href="{{ cli_ref.url }}" class="doc-link">CLI Guide →</a>
  </div>
  
  <div class="doc-card">
    <h3>📁 Multi-file Projects</h3>
    <p>Learn how to organize and structure larger, more complex MDL projects.</p>
    <a href="{{ multi_file.url }}" class="doc-link">Project Structure →</a>
  </div>
  
  <div class="doc-card">
    <h3>🐍 Python Bindings</h3>
    <p>Programmatic access to MDL functionality for automation and integration.</p>
    <a href="{{ python_api.url }}" class="doc-link">API Reference →</a>
  </div>
  
  <div class="doc-card">
    <h3>💻 VS Code Extension</h3>
    <p>Enhanced development experience with syntax highlighting and IntelliSense.</p>
    <a href="{{ vscode.url }}" class="doc-link">Extension Guide →</a>
  </div>
</div>

<style>
.doc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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

@media (max-width: 768px) {
  .doc-grid {
    grid-template-columns: 1fr;
  }
}
</style>
