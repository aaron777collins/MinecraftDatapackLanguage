module Jekyll
  class VersionReader < Generator
    safe true
    priority :normal

    def generate(site)
      # Read version from the project's version file for development builds
      version_file = File.join(site.source, '..', 'minecraft_datapack_language', '_version.py')
      
      if File.exist?(version_file)
        content = File.read(version_file)
        if content =~ /__version__\s*=\s*version\s*=\s*['"]([^'"]+)['"]/
          site.config['current_version'] = $1
        elsif content =~ /__version__\s*=\s*['"]([^'"]+)['"]/
          site.config['current_version'] = $1
        end
      end
      
      # Set GitHub metadata defaults - these will be overridden by jekyll-github-metadata if available
      unless site.config['github']
        site.config['github'] = {}
      end
      
      unless site.config['github']['latest_release']
        site.config['github']['latest_release'] = {
          'tag_name' => site.config['current_version'] ? "v#{site.config['current_version']}" : 'Latest',
          'published_at' => Time.now.strftime('%Y-%m-%d'),
          'html_url' => "https://github.com/aaron777collins/MinecraftDatapackLanguage/releases/latest"
        }
      end
      
      unless site.config['github']['releases']
        site.config['github']['releases'] = []
      end
    end
  end
end
