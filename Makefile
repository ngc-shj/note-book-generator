# Define phony targets (non-file targets)
.PHONY: all articles cover frontmatter mainmatter back-cover book toc reflections qrcodes clean clean-articles clean-reflections clean-qrcodes clean-outputs

# Project structure
SRC_DIR     := src
CONFIG_DIR  := config
TEMPLATE_DIR:= templates
INPUT_DIR   := input
STYLE_DIR   := styles
ARTICLES_DIR:= articles
QR_DIR      := qrcodes
REFLECTIONS_DIR:= reflections
OUTPUT_DIR  := output
OUTPUT_MD_DIR:= $(OUTPUT_DIR)/md
OUTPUT_PDF_DIR:= $(OUTPUT_DIR)/pdf

# Input files
INPUT_XML   := $(INPUT_DIR)/note-ngc_shj-1.xml
EXCLUDE_LIST:= $(CONFIG_DIR)/exclude_articles.txt
INCLUDE_LIST:= $(CONFIG_DIR)/include_articles.txt
PDF_CONFIG  := $(CONFIG_DIR)/pdf_options.yaml
COVER_HTML  := $(TEMPLATE_DIR)/cover.md
BACK_COVER_HTML  := $(TEMPLATE_DIR)/back_cover.md
TOC_MD      := $(TEMPLATE_DIR)/toc.md
SEPARATOR   := $(TEMPLATE_DIR)/separator.md
INTRO_MD    := $(TEMPLATE_DIR)/introduction.md
CONCLUSION_MD := $(TEMPLATE_DIR)/conclusion.md
REFLECTION_TEMPLATE := $(TEMPLATE_DIR)/reflection.md.template
STYLE_BASE  := $(STYLE_DIR)/style-base.css
STYLE_COVER := $(STYLE_DIR)/cover-style.css
STYLE_FRONT := $(STYLE_DIR)/frontmatter-style.css
STYLE_MAIN  := $(STYLE_DIR)/mainmatter-style.css

# Output files
OUTPUT_NAME := note-book
OUTPUT_PDF  := $(OUTPUT_DIR)/$(OUTPUT_NAME).pdf

# Output md files for parts of the book
OUTPUT_COVER:= $(OUTPUT_MD_DIR)/cover.md
OUTPUT_BACK_COVER:= $(OUTPUT_MD_DIR)/back_cover.md
OUTPUT_TOC  := $(OUTPUT_MD_DIR)/toc.md
OUTPUT_FRONTMATTER := $(OUTPUT_MD_DIR)/frontmatter.md
OUTPUT_MAINMATTER := $(OUTPUT_MD_DIR)/mainmatter.md

# Output pdf files for parts of the book
COVER_PDF   := $(OUTPUT_PDF_DIR)/cover.pdf
BACK_COVER_PDF := $(OUTPUT_PDF_DIR)/back_cover.pdf
FRONTMATTER_PDF := $(OUTPUT_PDF_DIR)/frontmatter.pdf
MAINMATTER_PDF := $(OUTPUT_PDF_DIR)/mainmatter.pdf

# Scripts
WXR_TO_MD   := $(SRC_DIR)/wxr_to_md.py
MD_MERGER   := $(SRC_DIR)/merge_md_files.py
REFLECTION_GENERATOR:= $(SRC_DIR)/generate_reflections.py
TOC_GENERATOR := $(SRC_DIR)/generate_toc.py
QR_GENERATOR := $(SRC_DIR)/generate_qr_codes.py
PDF_MERGER  := $(SRC_DIR)/merge_pdf_files.py

# Tools and commands
PYTHON      := python3
MD_TO_PDF   := md-to-pdf

# Default status (set to public)
FILTER_STATUS := publish

# Default target
# all: articles qr merge html pdf 
all: book

# Generate markdown files from WXR
articles: $(ARTICLES_DIR)/articles.csv

$(ARTICLES_DIR)/articles.csv: $(WXR_TO_MD) $(INPUT_XML)
	mkdir -p $(ARTICLES_DIR)
	$(PYTHON) $(WXR_TO_MD) $(INPUT_XML) $(ARTICLES_DIR) --status $(FILTER_STATUS)
	touch $(ARTICLES_DIR)

# Generate QR codes
qrcodes: $(QR_DIR)

$(QR_DIR): $(ARTICLES_DIR)/articles.csv
	mkdir -p $(QR_DIR)
	$(PYTHON) $(QR_GENERATOR) \
		--csv $< \
		--output-dir $(QR_DIR)
	touch $@

# Optional reflections generation
reflections: $(REFLECTIONS_DIR)

$(REFLECTIONS_DIR): $(ARTICLES_DIR)/articles.csv $(REFLECTION_TEMPLATE)
	$(PYTHON) $(REFLECTION_GENERATOR) $< \
		--template $(REFLECTION_TEMPLATE) \
		--output-dir $(REFLECTIONS_DIR) \
		$(if $(wildcard $(EXCLUDE_LIST)),--exclude-file $(EXCLUDE_LIST)) \
		$(if $(wildcard $(INCLUDE_LIST)),--include-file $(INCLUDE_LIST))
	touch $(ARTICLES_DIR)
	touch $@

# Generate Cover
cover: $(COVER_PDF)

$(COVER_PDF): $(OUTPUT_COVER) $(STYLE_COVER) $(STYLE_BASE)
	$(MD_TO_PDF) \
		--stylesheet $(STYLE_BASE) \
		--stylesheet $(STYLE_COVER) \
		$<
	mkdir -p $(OUTPUT_PDF_DIR)
	mv $(OUTPUT_COVER:.md=.pdf) $@

$(OUTPUT_COVER): $(COVER_HTML) $(PDF_CONFIG) $(MD_MERGER)
	mkdir -p $(OUTPUT_MD_DIR)
	$(PYTHON) $(MD_MERGER) \
		--pdf-options $(PDF_CONFIG) \
		--cover-design $< \
		--output $@

# Generate Back Cover
back-cover: $(BACK_COVER_PDF)

$(BACK_COVER_PDF): $(OUTPUT_BACK_COVER) $(STYLE_COVER) $(STYLE_BASE)
	$(MD_TO_PDF) \
		--stylesheet $(STYLE_BASE) \
		--stylesheet $(STYLE_COVER) \
		$<
	mkdir -p $(OUTPUT_PDF_DIR)
	mv $(OUTPUT_BACK_COVER:.md=.pdf) $@

$(OUTPUT_BACK_COVER): $(BACK_COVER_HTML) $(PDF_CONFIG) $(MD_MERGER)
	mkdir -p $(OUTPUT_MD_DIR)
	$(PYTHON) $(MD_MERGER) \
		--pdf-options $(PDF_CONFIG) \
		--back-cover $< \
		--output $@

# Front-matter
frontmatter: $(FRONTMATTER_PDF)

$(FRONTMATTER_PDF): $(OUTPUT_FRONTMATTER) $(STYLE_FRONT) $(STYLE_BASE)
	$(MD_TO_PDF) \
		--stylesheet $(STYLE_BASE) \
		--stylesheet $(STYLE_FRONT) \
		$<
	mkdir -p $(OUTPUT_PDF_DIR)
	mv $(OUTPUT_FRONTMATTER:.md=.pdf) $@

$(OUTPUT_FRONTMATTER): $(OUTPUT_TOC) $(PDF_CONFIG) $(MD_MERGER)
	$(PYTHON) $(MD_MERGER) \
		--pdf-options $(PDF_CONFIG) \
		--separator $(SEPARATOR) \
		--toc $(OUTPUT_TOC) \
		--output $@

# TOC
toc: $(OUTPUT_TOC)

$(OUTPUT_TOC): $(MAINMATTER_PDF)
	mkdir -p $(OUTPUT_MD_DIR)
	$(PYTHON) $(TOC_GENERATOR) \
		--pdf-file $< \
		--output $@

# Main-matter = introduction + articles + conclusion
mainmatter: $(MAINMATTER_PDF)

$(MAINMATTER_PDF): $(OUTPUT_MAINMATTER) $(STYLE_MAIN) $(STYLE_BASE)
	$(MD_TO_PDF) \
		--stylesheet $(STYLE_BASE) \
		--stylesheet $(STYLE_MAIN) \
		$<
	mkdir -p $(OUTPUT_PDF_DIR)
	mv $(OUTPUT_MAINMATTER:.md=.pdf) $@

$(OUTPUT_MAINMATTER): $(INTRO_MD) $(ARTICLES_DIR)/articles.csv $(CONCLUSION_MD) $(PDF_CONFIG) $(MD_MERGER)
	mkdir -p $(OUTPUT_MD_DIR)
	$(PYTHON) $(MD_MERGER) \
		--pdf-options $(PDF_CONFIG) \
		$(if $(wildcard $(EXCLUDE_LIST)),--exclude-file $(EXCLUDE_LIST)) \
		$(if $(wildcard $(INCLUDE_LIST)),--include-file $(INCLUDE_LIST)) \
		$(if $(wildcard $(REFLECTIONS_DIR)),--reflections-dir $(REFLECTIONS_DIR)) \
		--separator $(SEPARATOR) \
		--introduction $(INTRO_MD) \
		--articles-dir $(ARTICLES_DIR) \
		--conclusion $(CONCLUSION_MD) \
		--output $@

# Merge PDF files
book: $(OUTPUT_PDF)

$(OUTPUT_PDF): $(COVER_PDF) $(FRONTMATTER_PDF) $(MAINMATTER_PDF) $(BACK_COVER_PDF) $(PDF_MERGER)
	$(PYTHON) $(PDF_MERGER) \
		--cover-design $(COVER_PDF) \
		--frontmatter $(FRONTMATTER_PDF) \
		--mainmatter $(MAINMATTER_PDF) \
		--back-cover-design $(BACK_COVER_PDF) \
		--output $@

# Clean targets
clean: clean-articles clean-reflections clean-qrcodes clean-outputs

clean-articles:
	rm -rf $(ARTICLES_DIR)

clean-reflections:
	rm -rf $(REFLECTIONS_DIR)

clean-qrcodes:
	rm -rf $(QR_DIR)

clean-outputs:
	rm -rf $(OUTPUT_MD_DIR) $(OUTPUT_PDF_DIR)
