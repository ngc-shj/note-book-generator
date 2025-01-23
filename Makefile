.PHONY: html pdf clean all clean_html clean_pdf

# Input/Output
INPUT_XML=./export/note-ngc_shj-1.xml
ARTICLES_DIR=articles
OUTPUT_BOOK=note-book

# Config files
CONFIG_DIR=config
EXCLUDE_LIST=$(CONFIG_DIR)/exclude_articles.txt
SEPARATOR=$(CONFIG_DIR)/separator.html
PDF_CONFIG=$(CONFIG_DIR)/pdf_options.yaml
COVER_TEMPLATE=templates/cover.html
STYLE_CSS=styles/style.css

# Scripts
SRC_DIR=src
WXR_CONVERTER=$(SRC_DIR)/wxr_to_md.py
MD_MERGER=$(SRC_DIR)/merge_md_files.py

# Tools
MD_TO_PDF=md-to-pdf
PYTHON=python3

# Default target
all: html pdf

# Generated files
$(ARTICLES_DIR): $(WXR_CONVERTER) $(INPUT_XML)
	$(PYTHON) $(WXR_CONVERTER) $(INPUT_XML) $(ARTICLES_DIR)

$(OUTPUT_BOOK).md: $(MD_MERGER) $(ARTICLES_DIR) $(PDF_CONFIG) $(COVER_TEMPLATE) $(SEPARATOR) $(EXCLUDE_LIST)
	$(PYTHON) $(MD_MERGER) \
		--exclude-file $(EXCLUDE_LIST) \
		--pdf-options $(PDF_CONFIG) \
		--cover-design $(COVER_TEMPLATE) \
		--separator $(SEPARATOR) \
		--output $@ \
		$(ARTICLES_DIR)

html: clean_html $(OUTPUT_BOOK).md $(STYLE_CSS)
	$(MD_TO_PDF) --stylesheet $(STYLE_CSS) $(OUTPUT_BOOK).md --as-html

pdf: clean_pdf $(OUTPUT_BOOK).md $(STYLE_CSS)
	$(MD_TO_PDF) --stylesheet $(STYLE_CSS) $(OUTPUT_BOOK).md

clean_html:
	rm -f $(OUTPUT_BOOK).html

clean_pdf:
	rm -f $(OUTPUT_BOOK).pdf

clean: clean_html clean_pdf
	rm -rf $(ARTICLES_DIR) $(OUTPUT_BOOK).md

