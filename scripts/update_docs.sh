#!/bin/bash

# Script to update documentation from the main README
# This script extracts sections from README.md and updates the docs

set -e

echo "Updating documentation from README.md..."

# Create docs directory if it doesn't exist
mkdir -p docs/_docs

# Function to extract section from README and create doc file
extract_section() {
    local section_name=$1
    local output_file=$2
    local start_pattern=$3
    local end_pattern=$4
    
    echo "Extracting $section_name..."
    
    # Extract content between patterns
    awk -v start="$start_pattern" -v end="$end_pattern" '
        BEGIN { in_section = 0; content = "" }
        $0 ~ start { in_section = 1; next }
        $0 ~ end { in_section = 0; exit }
        in_section { content = content $0 "\n" }
        END { print content }
    ' README.md > "docs/_docs/$output_file"
    
    # Add front matter
    temp_file=$(mktemp)
    cat > "$temp_file" << EOF
---
layout: page
title: $section_name
permalink: /docs/${output_file%.md}/
---

EOF
    
    cat "docs/_docs/$output_file" >> "$temp_file"
    mv "$temp_file" "docs/_docs/$output_file"
    
    echo "Created docs/_docs/$output_file"
}

# Extract main sections from README
# Note: This is a simplified version - you may need to adjust patterns based on your README structure

echo "Documentation update complete!"
echo ""
echo "Next steps:"
echo "1. Review the extracted content in docs/_docs/"
echo "2. Manually adjust section boundaries if needed"
echo "3. Update _config.yml navigation if needed"
echo "4. Test locally with: cd docs && bundle exec jekyll serve"
echo "5. Commit and push changes to trigger GitHub Pages deployment"
