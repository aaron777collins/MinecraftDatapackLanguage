module Jekyll
  class TestVersion < Generator
    safe true
    priority :low

    def generate(site)
      puts "🔍 Version Reader Test:"
      puts "  Current version: #{site.config['current_version']}"
      puts "  GitHub latest release: #{site.config['github']['latest_release']['tag_name'] if site.config['github'] && site.config['github']['latest_release']}"
      puts "  GitHub releases count: #{site.config['github']['releases'].size if site.config['github'] && site.config['github']['releases']}"
    end
  end
end
