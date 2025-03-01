#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract table of contents from PDF and generate styled markdown output.
Uses CSS-based dotted leaders for professional TOC appearance.
Includes 'はじめに' and 'あとがき' sections in the TOC.
"""

import re
import sys
import argparse
from typing import List, Tuple, Union
import unicodedata
from pathlib import Path
from PyPDF2 import PdfReader

# Constants for Japanese text patterns
PUBLICATION_DATE = "公開日"
TITLE_PATTERN = re.compile(r'^\[(\d+)\] (.+)')
INTRO_PATTERN = re.compile(r'^はじめに$')
CONCLUSION_PATTERN = re.compile(r'^あとがき$')

# パターンでページ番号を検出（ページ番号が単独であることを前提）
PAGE_NUMBER_PATTERN = re.compile(r'^\d+$')

def extract_toc_from_pdf(pdf_path: Path) -> List[Tuple[Union[str, int], str, int]]:
    """
    Extract article numbers, titles and page numbers from PDF.
    Also includes special sections like introduction and conclusion.
    
    Returns:
        List of tuples containing (section_id, title, page_number)
        section_id can be a number (for articles) or a special identifier like "intro" or "conclusion"
    """
    reader = PdfReader(str(pdf_path))
    toc = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue
            
        # テキストを正規化し、行に分割
        lines = [
            unicodedata.normalize("NFKC", line.strip()) 
            for line in text.splitlines() 
            if line.strip()
        ]

        # 前処理: ページ番号のみの行を除去（フッターのページ番号による影響を排除）
        cleaned_lines = []
        for line in lines:
            if not PAGE_NUMBER_PATTERN.match(line):
                # ページ番号で始まる行の場合、ページ番号を削除
                if re.match(r'^\d+\s*', line):
                    line = re.sub(r'^\d+\s*', '', line)
                cleaned_lines.append(line)
        
        lines = cleaned_lines

        for idx, line in enumerate(lines):
            # 通常の記事タイトルを検索
            match = TITLE_PATTERN.match(line)
            if match:
                article_num, title_text = match.groups()
                title = title_text.strip()
                found_date = False
                
                for j in range(idx + 1, min(idx + 3, len(lines))):
                    next_line = unicodedata.normalize("NFKC", lines[j])
                    if PUBLICATION_DATE in next_line:
                        found_date = True
                        toc.append((article_num, title, page_num))
                        break
                if not found_date and idx < len(lines) - 1:
                    title += " " + lines[idx + 1]
            
            # はじめにを検索
            elif INTRO_PATTERN.match(line):
                # 「はじめに」というテキストがある行を検出
                toc.append(("intro", line, page_num))
            
            # あとがきを検索
            elif CONCLUSION_PATTERN.match(line):
                # 「あとがき」というテキストがある行を検出
                toc.append(("conclusion", line, page_num))

    return toc

def generate_toc_markdown(toc: List[Tuple[Union[str, int], str, int]]) -> str:
    """
    Convert TOC entries to styled markdown with CSS-based dotted leaders.
    """

    toc_lines = [
        '<div class="toc-container">',
        '<div class="toc-title">目次</div>'
    ]

    for entry in toc:
        section_id, title, page_num = entry
        
        toc_lines.append(f'<div class="toc-entry">')
        
        # Handle different types of entries
        if section_id == "intro":
            # Introduction entry (no number)
            toc_lines.append(f'  <span class="toc-special"></span>')
            toc_lines.append(f'  <span class="toc-text">{title}</span>')
            toc_lines.append(f'  <span class="toc-page"><a href="#introduction">{page_num}</a></span>')
        elif section_id == "conclusion":
            # Conclusion entry (no number)
            toc_lines.append(f'  <span class="toc-special"></span>')
            toc_lines.append(f'  <span class="toc-text">{title}</span>')
            toc_lines.append(f'  <span class="toc-page"><a href="#conclusion">{page_num}</a></span>')
        else:
            # Regular article entry
            toc_lines.append(f'  <span class="toc-number">{section_id}.</span>')
            toc_lines.append(f'  <span class="toc-text">{title}</span>')
            if isinstance(section_id, int):
                article_id_padded = f"{section_id:04d}"
            else:
                try:
                    article_id_padded = f"{int(section_id):04d}"
                except (ValueError, TypeError):
                    article_id_padded = section_id
            toc_lines.append(f'  <span class="toc-page"><a href="#article-{article_id_padded}">{page_num}</a></span>')
        
        toc_lines.append(f'</div>')

    toc_lines.append("</div>")

    return "\n".join(toc_lines)

def setup_argument_parser():
    """Setup argument parser for command-line usage."""
    parser = argparse.ArgumentParser(description="Extract table of contents from PDF and generate styled markdown output.")
    parser.add_argument(
        "--pdf-file", type=str,
        default=None,
        help="Path to the PDF file."
    )
    parser.add_argument(
        "--output", type=str,
        default=None,
        help="Path to the output markdown file."
    )
    return parser

def main():
    """Process PDF and generate styled TOC markdown file."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    try:
        pdf_path = args.pdf_file
        output_path = Path(args.output)

        # Extract TOC and generate markdown
        toc = extract_toc_from_pdf(pdf_path)
        if not toc:
            print("No table of contents information found in PDF.")
            sys.exit(1)

        toc_md = generate_toc_markdown(toc)
        output_path.write_text(toc_md, encoding="utf-8")
        print(f"TOC has been generated in {output_path}")

    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()