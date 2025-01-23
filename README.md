# note-book-generator

Convert note.com articles (WXR format) to PDF/HTML book.

## Requirements

- Python 3.8+
- md-to-pdf

## Installation

```bash
git clone https://github.com/your-username/note-book-generator.git
cd note-book-generator
pip install -r requirements.txt
```

## Usage

1. Export your note.com articles as WXR format
2. Copy config/template files:

```bash
cp config/exclude_articles.txt.example config/exclude_articles.txt
cp config/pdf_options.yaml.example config/pdf_options.yaml
cp templates/cover.html.example templates/cover.html
cp templates/separator.html.example templates/separator.html
```

3. Edit configuration files
4. Run make:

```bash
make pdf  # Generate PDF
make html # Generate HTML
```

## Configuration Files

- `exclude_articles.txt`: List of article numbers to exclude
- `pdf_options.yaml`: PDF generation options (page size, margins, etc.)
- `cover.html`: Book cover design
- `separator.html`: Separator between articles

## License

[Apache 2.0](LICENSE)
