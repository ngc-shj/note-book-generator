#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from typing import List, Optional
import PyPDF2
from pathlib import Path

def merge_pdf_files(
    output_file: str,
    cover_design: Optional[str] = None,
    back_cover_design: Optional[str] = None,
    frontmatter: Optional[str] = None,
    mainmatter: Optional[str] = None,
    toc: Optional[str] = None,
    introduction: Optional[str] = None,
    body: Optional[str] = None,
    conclusion: Optional[str] = None,
) -> None:
    pdf_paths = []
    if cover_design:
        pdf_paths.append(cover_design)
    if frontmatter:
        pdf_paths.append(frontmatter)
    else:
        if toc:
            pdf_paths.append(toc)
        if introduction:
            pdf_paths.append(introduction)
    if mainmatter:
        pdf_paths.append(mainmatter)
    else:
        if body:
            pdf_paths.append(body)
        if conclusion:
            pdf_paths.append(conclusion)
    if back_cover_design:
        pdf_paths.append(back_cover_design)

    pdf_writer = PyPDF2.PdfWriter()
    for path in pdf_paths:
        if not Path(path).exists():
            print(f"Warning: File '{path}' not found. Skipping.\n")
            pdf_paths.remove(path)
            continue
        pdf_reader = PyPDF2.PdfReader(str(path))
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    with open(output_file, "wb") as out:
        pdf_writer.write(out)

def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Merge .pdf files into a single document.")
    
    # Output configuration
    output_group = parser.add_argument_group('output configuration')
    output_group.add_argument(
        "--output", type=str,
        default="merged_output.pdf",
        help="Output file name for the merged content. Default is 'merged_output.pdf'."
    )
    
    # Document structure
    structure_group = parser.add_argument_group('document structure')
    structure_group.add_argument(
        "--cover-design", type=str,
        default=None,
        help="Path to the cover file (optional)."
    )
    structure_group.add_argument(
        "--back-cover-design", type=str,
        default=None,
        help="Path to the back cover file (optional)."
    )
    structure_group.add_argument(
        "--frontmatter", type=str,
        default=None,
        help="Path to the frontmatter file (contains TOC and introduction)."
    )
    structure_group.add_argument(
        "--toc", type=str,
        default=None,
        help="Path to the TOC file (optional)."
    )
    structure_group.add_argument(
        "--introduction", type=str,
        default=None,
        help="Path to introduction markdown file"
    )
    structure_group.add_argument(
        "--mainmatter", type=str,
        default=None,
        help="Path to the mainmatter file (contains body and conclusion)."
    )
    structure_group.add_argument(
        "--body", type=str,
        default=None,
        help="Path to body markdown file"
    )
    structure_group.add_argument(
        "--conclusion", type=str,
        default=None,
        help="Path to conclusion markdown file"
    )

    return parser

def main():
    parser = setup_argument_parser()
    args = parser.parse_args()

    merge_pdf_files(
        output_file=args.output,
        cover_design=args.cover_design,
        back_cover_design=args.back_cover_design,
        frontmatter=args.frontmatter,
        mainmatter=args.mainmatter,
        toc=args.toc,
        introduction=args.introduction,
        body=args.body,
        conclusion=args.conclusion,
    )

if __name__ == "__main__":
    main()
