# note-book-generator

Convert note.com articles exported in WordPress Extended RSS (WXR) format into PDF/HTML books with customizable formatting, reflections, and QR codes.

## Features

- Converts WXR exports to clean Markdown format
- Generates both PDF and HTML outputs
- Supports custom book cover and article separators
- Optional introduction and conclusion sections
- Optional reflection sections for each article
- Configurable article inclusion/exclusion
- Preserves code blocks with syntax highlighting
- Maintains image references and captions
- Customizable PDF formatting (page size, margins, headers/footers)
- Generates QR codes for article URLs

## Requirements

- Python 3.8+
- Node.js 12+ (for md-to-pdf)
- Required Python packages:
  - bs4 (BeautifulSoup4)
  - PyYAML
  - qrcode
  - pandas
  - pillow

**Note**: Before using the generator, edit `Makefile` to set the `INPUT_XML` variable to the path of your WXR export file:

```makefile
INPUT_XML := $(INPUT_DIR)/your-wxr-export.xml
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/note-book-generator.git
cd note-book-generator
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install md-to-pdf:

```bash
npm install -g md-to-pdf
```

4. Initialize project structure and copy configuration templates:

```bash
./init.sh
```

This script will:

- Create necessary directories (`config`, `templates`, `styles`, `input`, `qrcodes`)
- Copy example configuration files to their proper locations:
  - `config/exclude_articles.txt`
  - `config/include_articles.txt`
  - `config/pdf_options.yaml`
  - `templates/cover.md`
  - `templates/back_cover.md`
  - `templates/introduction.md`
  - `templates/conclusion.md`
  - `templates/separator.md`
  - `templates/reflection.md.template`
  - `styles/style.css`

5. Place note.com export files:
   - From note.com, export your articles in WordPress Extended RSS (WXR) format
   - Extract downloaded zip file (format: `[hash]_1.zip`)
   - Move contents to the `input` directory:

     ```bash
     mv note-ngc_shj-1.xml input/
     mv assets input/
     ```

   The `assets` directory contains your article images and media files.

## Project Structure

```text
note-book-generator/
├── config/                 # Configuration files
│   ├── exclude_articles.txt
│   ├── include_articles.txt
│   └── pdf_options.yaml
├── templates/             # Markdown templates
│   ├── cover.md          # Book front cover
│   ├── back_cover.md     # Book back cover
│   ├── introduction.md   # Introduction chapter
│   ├── conclusion.md     # Conclusion chapter
│   ├── separator.md      # Separator between articles
│   └── reflection.md.template
├── styles/                # Stylesheets
│   └── style.css
├── src/                   # Source code
│   ├── wxr_to_md.py
│   ├── merge_md_files.py
│   ├── generate_reflections.py
│   ├── generate_qr_codes.py
├── articles/             # Generated article files
├── reflections/         # Generated reflection templates
├── qrcodes/             # Generated QR codes
└── input/               # Input files (note.com WXR exports)
```

## Configuration

### Article Selection (`config/`)

Both exclude and include lists are optional:

- If neither is specified, all articles will be included in the output
- `exclude_articles.txt`: Optional list of article numbers to exclude
- `include_articles.txt`: Optional list of specific articles to include
- Format: One article number per line

To include only specific articles, list their numbers in `include_articles.txt`:

```text
1
2
```

### PDF Options (`config/pdf_options.yaml`)

Controls PDF output formatting:

- Page size and margins
- Header/footer templates
- Custom styling
- Font settings

### Templates (`templates/`)

- `cover.md`: Front cover design with title, subtitle, and author
- `back_cover.md`: Back cover design (optional)
- `introduction.md`: Introduction chapter
- `conclusion.md`: Conclusion chapter
- `separator.md`: Separator HTML/Markdown between articles
- `reflection.md.template`: Template for article reflections

Each template supports custom CSS classes defined in `styles/style.css` for consistent styling.

### CSS Styling (`styles/style.css`)

The stylesheet provides custom classes for:
- Cover layouts (`cover-container`, `cover-title`, etc.)
- Back cover layouts (`back-cover-container`, etc.)
- Introduction/conclusion styles
- Article and reflection formatting
- Code block and blockquote styling
- Image sizing and placement
- PDF-specific page layouts and margins

## Generated Files

### `articles.csv` Format

**Note**: `articles/articles.csv` is generated after running `make` for the first time, listing all articles found in your WXR file with their assigned numbers.

After `make` is executed, `articles.csv` is generated with the following format:

```csv
number,link,pub_date,status,title,filename
0000,https://note.com/user,"Sat, 01 Feb 2025 09:18:23 +0900",info,サイト情報,0000_Channel_Info.md
0001,https://note.com/user/n/xxx,2023-09-13 00:37,publish,Title,0001_Title.md
```

Fields:
- `number`: Unique article number
- `link`: Original article URL
- `pub_date`: Publication date
- `status`: Publication status (`publish`, `draft`, etc.)
- `title`: Article title
- `filename`: Corresponding Markdown file

## Usage

### Basic Usage

Generate markdown files from WXR:

```bash
make articles
```

Generate QR codes:

```bash
make qr
```

QR codes will be saved in the `qrcodes/` directory. Each file corresponds to an article's assigned filename.

Merge all content:

```bash
make merge
```

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


### Filtering Articles by Status

By default, only **publish** articles are processed (`FILTER_STATUS=publish`).  
To include **draft** articles, run:

```bash
make FILTER_STATUS=draft articles
```

To include both **publish** and **draft** articles:

```bash
make FILTER_STATUS="publish,draft" wxr_to_md
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
