#!/bin/bash

# Create directories
mkdir -p input config templates styles qrcodes

# Copy example files if they don't exist
for example in \
    config/exclude_articles.txt.example \
    config/include_articles.txt.example \
    config/pdf_cover_options.yaml.example \
    config/pdf_frontmatter_options.yaml.example \
    config/pdf_mainmatter_options.yaml.example \
    styles/cover-style.css.example \
    styles/frontmatter-style.css.example \
    styles/mainmatter-style.css.example \
    styles/style-base.css.example \
    templates/cover.md.example \
    templates/back_cover.md.example \
    templates/introduction.md.example \
    templates/conclusion.md.example \
    templates/separator.md.example \
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
