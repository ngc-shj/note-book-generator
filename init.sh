#!/bin/bash

# Create directories
mkdir -p config templates styles export

# Copy example files if they don't exist
for example in \
    config/exclude_articles.txt.example \
    config/include_articles.txt.example \
    config/pdf_options.yaml.example \
    templates/cover.html.example \
    templates/separator.html.example \
    templates/reflection.md.template.example
do
    target="${example%.example}"
    if [ ! -f "$target" ]; then
        cp "$example" "$target"
        echo "Created: $target"
    else
        echo "Skipped: $target (already exists)"
    fi
done
