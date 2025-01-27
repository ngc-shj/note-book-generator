# Define phony targets (non-file targets)
.PHONY: all html pdf clean reflections

# Project structure
SRC_DIR     := src
CONFIG_DIR  := config
TEMPLATE_DIR:= templates
INPUT_DIR   := input
STYLE_DIR   := styles
ARTICLES_DIR:= articles
REFLECTIONS_DIR:= reflections

# Input files
INPUT_XML   := $(INPUT_DIR)/note-ngc_shj-1.xml
EXCLUDE_LIST:= $(CONFIG_DIR)/exclude_articles.txt
INCLUDE_LIST:= $(CONFIG_DIR)/include_articles.txt
PDF_CONFIG  := $(CONFIG_DIR)/pdf_options.yaml
COVER_HTML  := $(TEMPLATE_DIR)/cover.md
SEPARATOR   := $(TEMPLATE_DIR)/separator.md
INTRO_MD    := $(TEMPLATE_DIR)/introduction.md
OUTRO_MD    := $(TEMPLATE_DIR)/conclusion.md
REFLECTION_TEMPLATE := $(TEMPLATE_DIR)/reflection.md.template
STYLE_CSS   := $(STYLE_DIR)/style.css

# Scripts
WXR_TO_MD   := $(SRC_DIR)/wxr_to_md.py
MD_MERGER   := $(SRC_DIR)/merge_md_files.py
REFLECTION_GENERATOR:= $(SRC_DIR)/generate_reflections.py

# Output files
OUTPUT_NAME := note-book
OUTPUT_MD   := $(OUTPUT_NAME).md
OUTPUT_HTML := $(OUTPUT_NAME).html
OUTPUT_PDF  := $(OUTPUT_NAME).pdf

# Tools and commands
PYTHON      := python3
MD_TO_PDF   := md-to-pdf

# Default target
all: $(OUTPUT_MD) html pdf

# Generate markdown files from WXR
$(ARTICLES_DIR): $(WXR_TO_MD) $(INPUT_XML)
	rm -f $(OUTPUT_MD)
	mkdir -p $@
	$(PYTHON) $(WXR_TO_MD) $(INPUT_XML) $@
	touch $@

# Optional reflections generation
reflections: $(ARTICLES_DIR)/articles.csv $(REFLECTION_TEMPLATE)
	$(PYTHON) $(REFLECTION_GENERATOR) $< \
		--template $(REFLECTION_TEMPLATE) \
		--output-dir $(REFLECTIONS_DIR) \
		$(if $(wildcard $(EXCLUDE_LIST)),--exclude-file $(EXCLUDE_LIST)) \
		$(if $(wildcard $(INCLUDE_LIST)),--include-file $(INCLUDE_LIST))
	touch $(ARTICLES_DIR)

# Merge markdown files
$(OUTPUT_MD): $(MD_MERGER) $(ARTICLES_DIR) $(PDF_CONFIG) $(COVER_HTML) $(SEPARATOR) $(INTRO_MD) $(OUTRO_MD)
	$(PYTHON) $(MD_MERGER) \
		$(if $(wildcard $(EXCLUDE_LIST)),--exclude-file $(EXCLUDE_LIST)) \
		$(if $(wildcard $(INCLUDE_LIST)),--include-file $(INCLUDE_LIST)) \
		$(if $(wildcard $(REFLECTIONS_DIR)),--reflections-dir $(REFLECTIONS_DIR)) \
		--pdf-options $(PDF_CONFIG) \
		--cover-design $(COVER_HTML) \
		--separator $(SEPARATOR) \
		--introduction $(INTRO_MD) \
		--conclusion $(OUTRO_MD) \
		--output $@ \
		$(ARTICLES_DIR)

# Generate HTML
html: $(OUTPUT_MD) $(STYLE_CSS)
	$(MD_TO_PDF) --stylesheet $(STYLE_CSS) $< --as-html

# Generate PDF
pdf: $(OUTPUT_MD) $(STYLE_CSS)
	$(MD_TO_PDF) --stylesheet $(STYLE_CSS) $<

# Clean targets
clean: clean-outputs clean-reflections

clean-outputs:
	rm -f $(OUTPUT_PDF) $(OUTPUT_HTML)
	rm -rf $(ARTICLES_DIR) $(OUTPUT_MD)

clean-reflections:
	rm -rf $(REFLECTIONS_DIR)
