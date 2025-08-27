# MDL Website Setup Guide

This guide will help you set up and deploy the comprehensive documentation website for Minecraft Datapack Language (MDL).

## What's Been Created

I've created a complete Jekyll-based documentation website with the following features:

### 📁 File Structure
```
docs/
├── _config.yml              # Jekyll configuration
├── _docs/                   # Documentation pages
│   ├── getting-started.md
│   ├── language-reference.md
│   ├── python-api.md
│   ├── cli-reference.md
│   ├── vscode-extension.md
│   ├── examples.md
│   ├── multi-file-projects.md
│   └── contributing.md
├── _layouts/                # Page layouts
│   ├── default.html
│   └── page.html
├── _includes/               # Reusable components
│   ├── head-custom.html
│   └── navigation.html
├── index.md                 # Homepage
├── 404.html                 # Error page
├── Gemfile                  # Ruby dependencies
└── README.md                # Docs README
```

### 🎨 Features
- **Responsive Design**: Works on desktop and mobile
- **Syntax Highlighting**: Code blocks with syntax highlighting
- **Navigation**: Easy navigation between pages
- **Search Engine Optimized**: SEO-friendly structure
- **GitHub Pages Ready**: Automatic deployment setup
- **Modern UI**: Clean, professional design

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository: https://github.com/aaron777collins/MinecraftDatapackLanguage
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Select **gh-pages** branch (will be created by GitHub Actions)
6. Click **Save**

### 2. Push the Changes

```bash
# Add all the new files
git add .

# Commit the changes
git commit -m "Add comprehensive documentation website"

# Push to GitHub
git push origin main
```

### 3. Monitor Deployment

1. Go to **Actions** tab in your repository
2. You should see a "Build and Deploy Documentation" workflow running
3. Wait for it to complete (usually takes 2-3 minutes)
4. Once complete, your site will be available at: https://aaron777collins.github.io/MinecraftDatapackLanguage/

## Local Development

### Prerequisites

- Ruby 3.0 or higher
- Bundler

### Setup Local Development

```bash
# Navigate to docs directory
cd docs

# Install Ruby dependencies
bundle install

# Start local development server
bundle exec jekyll serve

# Open browser to http://localhost:4000
```

## Customization

### Adding New Pages

1. Create a new `.md` file in `docs/_docs/`
2. Add front matter:
   ```markdown
   ---
   layout: page
   title: Your Page Title
   permalink: /docs/your-page/
   ---
   ```
3. Add to navigation in `docs/_config.yml`

### Updating Content

The documentation is based on your existing README.md. To keep it in sync:

1. **Manual Updates**: Edit the files in `docs/_docs/` directly
2. **Automatic Updates**: Use the script `scripts/update_docs.sh` (may need customization)

### Styling

- Custom styles are in `docs/_includes/head-custom.html`
- The site uses the Cayman theme with custom modifications
- Responsive design for mobile devices

## Content Overview

### 📚 Documentation Pages

1. **Getting Started** - Installation and first steps
2. **Language Reference** - Complete MDL syntax guide
3. **Python API** - Programmatic datapack creation
4. **CLI Reference** - Command-line tool usage
5. **VS Code Extension** - IDE integration
6. **Examples** - Complete working examples
7. **Multi-file Projects** - Organizing large datapacks
8. **Contributing** - How to contribute to MDL

### 🎯 Key Features

- **Comprehensive Coverage**: All aspects of MDL documented
- **Practical Examples**: Real-world examples that work
- **Step-by-step Guides**: Easy to follow tutorials
- **API Reference**: Complete Python API documentation
- **Best Practices**: Tips and recommendations

## Maintenance

### Keeping Documentation Updated

1. **Regular Reviews**: Review documentation monthly
2. **Version Updates**: Update when releasing new versions
3. **User Feedback**: Incorporate user suggestions
4. **Example Updates**: Keep examples current

### Automated Deployment

- GitHub Actions automatically builds and deploys on every push to main
- No manual deployment needed
- Build logs available in Actions tab

## Troubleshooting

### Common Issues

1. **Site not loading**: Check GitHub Actions for build errors
2. **Styling issues**: Verify CSS is loading correctly
3. **Broken links**: Test all internal links
4. **Build failures**: Check Ruby version and dependencies

### Getting Help

- Check the Actions tab for build logs
- Review Jekyll documentation for configuration issues
- Test locally before pushing changes

## Next Steps

### Immediate Actions

1. ✅ Push the changes to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Monitor the deployment
4. ✅ Test the live site

### Future Enhancements

1. **Search Functionality**: Add search to the site
2. **Interactive Examples**: Add interactive code examples
3. **User Feedback**: Add feedback forms
4. **Analytics**: Add usage analytics
5. **Dark Mode**: Add dark mode toggle

### Content Improvements

1. **More Examples**: Add more complex examples
2. **Video Tutorials**: Create video walkthroughs
3. **Community Showcase**: Feature user-created datapacks
4. **FAQ Section**: Add frequently asked questions

## Support

If you encounter any issues:

1. Check the GitHub Actions logs
2. Review the Jekyll documentation
3. Test locally to isolate issues
4. Create an issue in the repository

The website is now ready to provide comprehensive documentation for your Minecraft Datapack Language project! 🎉
