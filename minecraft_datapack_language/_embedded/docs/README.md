# MDL Documentation

This directory contains the documentation website for Minecraft Datapack Language (MDL).

## Local Development

### Prerequisites

- Ruby 3.0 or higher
- Bundler

### Setup

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Start the development server:
   ```bash
   bundle exec jekyll serve
   ```

3. Open your browser to `http://localhost:4000`

### Building for Production

```bash
bundle exec jekyll build
```

The built site will be in the `_site` directory.

## Structure

- `_config.yml` - Jekyll configuration
- `_docs/` - Documentation pages
- `_layouts/` - Page layouts
- `_includes/` - Reusable components
- `index.md` - Homepage
- `404.html` - Error page

## Adding Content

### New Documentation Pages

1. Create a new `.md` file in `_docs/`
2. Add front matter with title and permalink
3. Write your content in Markdown
4. Add the page to navigation in `_config.yml`

### Example

```markdown
---
layout: page
title: My New Page
permalink: /docs/my-new-page/
---

# My New Page

Content goes here...
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment is handled by the GitHub Actions workflow in `.github/workflows/docs.yml`.

## Customization

### Styling

Custom styles are in `_includes/head-custom.html`. The site uses the Cayman theme with custom modifications.

### Navigation

Navigation is configured in `_config.yml` under the `nav` section.

### Layouts

Custom layouts are in `_layouts/`. The main layouts are:
- `default.html` - Base layout
- `page.html` - Documentation page layout
