# Dynamic Downloads System

The downloads page (`/downloads/`) is now dynamically generated and automatically updates with the latest version information.

## How It Works

### 1. GitHub Metadata Integration
- Uses the `jekyll-github-metadata` plugin to fetch release information from GitHub
- Automatically displays the latest release version and date
- Shows recent releases with descriptions and asset counts

### 2. Fallback Version Reading
- If GitHub metadata is unavailable, reads version from `minecraft_datapack_language/_version.py`
- Ensures the page always shows current version information
- Provides graceful degradation when GitHub API is not accessible

### 3. Dynamic Content
- **Version Number**: Automatically updates from GitHub releases or project version file
- **Release Date**: Shows actual release date from GitHub
- **Download Links**: Dynamically generates links to latest assets
- **Recent Releases**: Shows the 5 most recent releases with descriptions

## Configuration

### Required Plugins
Add to `_config.yml`:
```yaml
plugins:
  - jekyll-github-metadata

github:
  is_project_page: true
  show_downloads: false
```

### Custom Plugins
- `_plugins/version_reader.rb`: Reads version from project files
- `_plugins/test_version.rb`: Debug plugin for development

## Features

### Automatic Updates
- ✅ Version number from latest GitHub release
- ✅ Release date formatting
- ✅ Dynamic download links for VSIX files
- ✅ Recent releases list with descriptions
- ✅ Asset count display

### Fallback Support
- ✅ Reads version from `_version.py` when GitHub unavailable
- ✅ Graceful handling of missing metadata
- ✅ Always shows current version information

### Responsive Design
- ✅ Mobile-friendly layout
- ✅ Adaptive download buttons
- ✅ Clean, modern styling

## Testing

To test the dynamic system locally:

1. **Build the site**:
   ```bash
   cd docs
   bundle exec jekyll build
   ```

2. **Check version reading**:
   The test plugin will output version information during build

3. **Verify fallback**:
   Disconnect from internet and rebuild to test fallback behavior

## Maintenance

The system requires minimal maintenance:

- **Automatic**: Version updates happen automatically when new releases are published
- **No Manual Updates**: No need to manually edit version numbers or dates
- **Self-Healing**: Fallback system ensures the page always works

## Troubleshooting

### GitHub Metadata Not Loading
- Check internet connection
- Verify GitHub repository access
- Fallback system will provide basic version info

### Version Not Updating
- Ensure `_version.py` is being read correctly
- Check file permissions and paths
- Verify Jekyll plugin is loading

### Build Errors
- Check Jekyll plugin syntax
- Verify required gems are installed
- Review Jekyll build logs for errors
