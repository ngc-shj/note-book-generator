# note-book-generator

Convert note.com articles exported in WordPress Extended RSS (WXR) format into PDF/HTML books with customizable formatting and reflections.

## Features

- Converts WXR exports to clean Markdown format
- Generates both PDF and HTML outputs
- Supports custom book cover and article separators
- Optional reflection sections for each article
- Configurable article inclusion/exclusion
- Preserves code blocks with syntax highlighting
- Maintains image references and captions
- Customizable PDF formatting (page size, margins, headers/footers)

## Requirements

- Python 3.8+
- md-to-pdf
- Required Python packages:
  - bs4 (BeautifulSoup4)
  - PyYAML

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/note-book-generator.git
cd note-book-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy configuration templates:

```bash
cp config/exclude_articles.txt.example config/exclude_articles.txt
cp config/pdf_options.yaml.example config/pdf_options.yaml
cp templates/cover.html.example templates/cover.html
cp templates/separator.html.example templates/separator.html
```

## Project Structure

```
note-book-generator/
├── config/                 # Configuration files
│   ├── exclude_articles.txt
│   ├── include_articles.txt
│   └── pdf_options.yaml
├── templates/             # HTML templates
│   ├── cover.html
│   └── separator.html
├── src/                   # Source code
│   ├── wxr_to_md.py
│   ├── merge_md_files.py
│   └── generate_reflections.py
├── articles/             # Generated article files
├── reflections/         # Generated reflection templates
└── input/               # Input files (note.com WXR exports)
```

## Configuration

### Article Selection (`config/`)

- `exclude_articles.txt`: List of article numbers to exclude
- `include_articles.txt`: Optional list of specific articles to include
- Format: One article number per line

### PDF Options (`config/pdf_options.yaml`)

Controls PDF output formatting:
- Page size and margins
- Header/footer templates
- Custom styling
- Font settings

### Templates (`templates/`)

- `cover.html`: Custom book cover design
- `separator.html`: Separator HTML between articles

## Usage

### Basic Usage

Generate PDF output:

```bash
make pdf
```

Generate HTML output:

```bash
make html
```

Generate both formats:

```bash
make all
```

### Working with Reflections

1. Generate reflection templates:

```bash
make reflections
```

2. Edit generated templates in `reflections/` directory
3. Include reflections in final output:

```bash
make pdf REFLECTIONS_DIR=reflections
```

### Cleaning Up

Remove generated files:

```bash
make clean
```

Remove only reflection files:

```bash
make clean-reflections
```

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details

