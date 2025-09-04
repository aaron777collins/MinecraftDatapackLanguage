---
layout: page
title: Documentation Hub
permalink: /docs/docs-hub/
description: Search and browse all MDL documentation
---

Search and browse all available documentation for the Minecraft Datapack Language (MDL).

<div class="search-container">
  <input type="text" id="docSearch" placeholder="Search documentation..." class="search-input">
  <div class="search-icon">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
    </svg>
  </div>
</div>

<div class="docs-grid" id="docsGrid">
  <div class="doc-card" data-categories="getting-started beginner">
    <h3>🚀 Getting Started</h3>
    <p>Learn the basics of MDL and set up your development environment.</p>
    <div class="doc-meta">
      <span class="category">Beginner</span>
      <span class="category">Setup</span>
    </div>
    <a href="{{ site.baseurl }}/docs/getting-started/" class="doc-link">Get Started →</a>
  </div>
  
  <div class="doc-card" data-categories="language reference syntax">
    <h3>📚 Language Reference</h3>
    <p>Complete syntax reference, data types, functions, and language features.</p>
    <div class="doc-meta">
      <span class="category">Reference</span>
      <span class="category">Syntax</span>
    </div>
    <a href="{{ site.baseurl }}/docs/language-reference/" class="doc-link">View Reference →</a>
  </div>
  
  <div class="doc-card" data-categories="cli command-line tools">
    <h3>🔧 CLI Reference</h3>
    <p>Command-line interface for building, testing, and managing MDL projects.</p>
    <div class="doc-meta">
      <span class="category">Tools</span>
      <span class="category">CLI</span>
    </div>
    <a href="{{ site.baseurl }}/docs/cli-reference/" class="doc-link">CLI Guide →</a>
  </div>
  
  <div class="doc-card" data-categories="multi-file projects structure">
    <h3>📁 Multi-file Projects</h3>
    <p>Learn how to organize and structure larger, more complex MDL projects.</p>
    <div class="doc-meta">
      <span class="category">Advanced</span>
      <span class="category">Structure</span>
    </div>
    <a href="{{ site.baseurl }}/docs/multi-file-projects/" class="doc-link">Project Structure →</a>
  </div>
  
  <div class="doc-card" data-categories="python api programming">
    <h3>🐍 Python Bindings</h3>
    <p>Programmatic access to MDL functionality for automation and integration.</p>
    <div class="doc-meta">
      <span class="category">API</span>
      <span class="category">Python</span>
    </div>
    <a href="{{ site.baseurl }}/docs/python-api/" class="doc-link">API Reference →</a>
  </div>
  
  <div class="doc-card" data-categories="vscode extension ide">
    <h3>💻 VS Code Extension</h3>
    <p>Enhanced development experience with syntax highlighting and IntelliSense.</p>
    <div class="doc-meta">
      <span class="category">IDE</span>
      <span class="category">VS Code</span>
    </div>
    <a href="{{ site.baseurl }}/docs/vscode-extension/" class="doc-link">Extension Guide →</a>
  </div>
  
  <div class="doc-card" data-categories="examples code samples">
    <h3>🎯 Examples</h3>
    <p>Complete working examples to learn from and use as templates.</p>
    <div class="doc-meta">
      <span class="category">Examples</span>
      <span class="category">Code</span>
    </div>
    <a href="{{ site.baseurl }}/docs/examples/" class="doc-link">View Examples →</a>
  </div>
  
  <div class="doc-card" data-categories="contributing development">
    <h3>🤝 Contributing</h3>
    <p>How to contribute to the MDL project and development guidelines.</p>
    <div class="doc-meta">
      <span class="category">Community</span>
      <span class="category">Development</span>
    </div>
    <a href="{{ site.baseurl }}/docs/contributing/" class="doc-link">Contribute →</a>
  </div>
</div>

<div class="no-results" id="noResults" style="display: none;">
  <h3>No documentation found</h3>
  <p>Try searching with different keywords or browse all documentation above.</p>
</div>

<style>
.search-container {
  position: relative;
  margin: 2rem 0;
  max-width: 600px;
}

.search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  border: 2px solid #e1e4e8;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #0366d6;
  box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.1);
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #586069;
}

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

.doc-card.hidden {
  display: none;
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

.no-results {
  text-align: center;
  padding: 3rem;
  color: #586069;
}

.no-results h3 {
  margin-bottom: 0.5rem;
  color: #24292e;
}

@media (max-width: 768px) {
  .docs-grid {
    grid-template-columns: 1fr;
  }
  
  .search-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('docSearch');
  const docsGrid = document.getElementById('docsGrid');
  const docCards = docsGrid.querySelectorAll('.doc-card');
  const noResults = document.getElementById('noResults');
  
  searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase().trim();
    let visibleCount = 0;
    
    docCards.forEach(card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      const description = card.querySelector('p').textContent.toLowerCase();
      const categories = card.dataset.categories.toLowerCase();
      
      const matches = title.includes(searchTerm) || 
                     description.includes(searchTerm) || 
                     categories.includes(searchTerm);
      
      if (matches || searchTerm === '') {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });
    
    // Show/hide no results message
    if (visibleCount === 0 && searchTerm !== '') {
      noResults.style.display = 'block';
    } else {
      noResults.style.display = 'none';
    }
  });
  
  // Focus search input on page load
  searchInput.focus();
});
</script>
