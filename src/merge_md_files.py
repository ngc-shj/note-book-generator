#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import yaml
from typing import List, Optional

def merge_md_files(
   directory: str,
   output_file: str,
   qr_dir: Optional[str] = None,
   include_numbers: Optional[List[str]] = None,
   exclude_numbers: Optional[List[str]] = None,
   cover_design: Optional[str] = None,
   back_cover_design: Optional[str] = None,
   separator: Optional[str] = None,
   introduction: Optional[str] = None,
   conclusion: Optional[str] = None,
   reflections_dir: Optional[str] = None,
   pdf_options: Optional[str] = None
) -> None:
    exclude_set = set(f"{int(num):04}" for num in (exclude_numbers or []))
    include_set = set(f"{int(num):04}" for num in (include_numbers or []))

    md_files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".md")],
        key=lambda x: re.match(r"^\d{4}", x).group() if re.match(r"^\d{4}", x) else ""
    )

    sep = "\n\n"
    if separator:
        with open(separator) as f:
            sep = f"\n\n{f.read().strip()}\n\n"

    with open(output_file, "w", encoding="utf-8") as output:
        if pdf_options:
            with open(pdf_options, 'r', encoding="utf-8") as f:
                yaml_content = yaml.safe_load(f)
                output.write('---\npdf_options:\n')
                for key, value in yaml_content.items():
                    if isinstance(value, str) and '\n' in value:
                        # 複数行の文字列は | 記法を使用
                        output.write(f'  {key}: |\n')
                        for line in value.split('\n'):
                            output.write(f'    {line}\n')
                    else:
                        output.write(f'  {key}: {value}\n')
                output.write('---\n\n')

        if cover_design:
            if os.path.exists(cover_design):
                with open(cover_design, "r", encoding="utf-8") as f:
                    output.write(f.read())
                    output.write("\n\n")
            else:
                print(f"Warning: Cover file '{cover_design}' not found. Skipping cover page.\n")

        if introduction:
            if os.path.exists(introduction):
                with open(introduction, "r", encoding="utf-8") as f:
                    output.write(f.read())
                    output.write(sep)
            else:
                print(f"Warning: Introduction file '{introduction}' not found. Skipping introduction.\n")

        for md_file in md_files:
            match = re.match(r"^(\d{4})_", md_file)
            if match:
                article_number = match.group(1)
                should_include = (not include_set or article_number in include_set)
                should_exclude = (article_number in exclude_set)

                if should_include and not should_exclude:
                    file_path = os.path.join(directory, md_file)
                    with open(file_path, "r", encoding="utf-8") as input_file:
                        content = input_file.read()

                    if qr_dir:
                        qr_code_path = os.path.join(qr_dir, f"{md_file.replace('.md', '.png')}")
                        if qr_dir and os.path.exists(qr_code_path):
                            qr_code_md = f"\n![]({qr_code_path})\n"
                            content = content.replace("**公開日**:", qr_code_md + "**公開日**:", 1)

                    output.write(content)

                    if reflections_dir:
                        reflection_path = os.path.join(reflections_dir, f"{article_number}_reflection.md")
                        if os.path.exists(reflection_path):
                            with open(reflection_path, "r", encoding="utf-8") as ref_file:
                                output.write("\n\n")
                                output.write(ref_file.read())

                    if md_file != md_files[-1]:
                        output.write("\n\n")
                        output.write(sep)
                        output.write("\n\n")

        if conclusion:
            if os.path.exists(conclusion):
                with open(conclusion, "r", encoding="utf-8") as f:
                    output.write(sep)
                    output.write(f.read())
                    output.write("\n\n")
            else:
                print(f"Warning: Conclusion file '{conclusion}' not found. Skipping conclusion.\n")

        if back_cover_design:
            if os.path.exists(back_cover_design):
                with open(back_cover_design, "r", encoding="utf-8") as f:
                    output.write(sep)
                    output.write(f.read())
            else:
                print(f"Warning: Cover file '{back_cover_design}' not found. Skipping back cover page.\n")

def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Merge .md files in a directory with optional include/exclude filters.")
    
    # Required arguments
    parser.add_argument("directory", type=str, help="Directory containing .md files to merge.")
    
    # Output configuration
    output_group = parser.add_argument_group('output configuration')
    output_group.add_argument(
        "--output", type=str,
        default="merged_output.md",
        help="Output file name for the merged content. Default is 'merged_output.md'."
    )
    output_group.add_argument(
        "--pdf-options", type=str,
        default=None,
        help="YAML file with PDF options for md-to-pdf"
    )
    
    # Article filtering
    filter_group = parser.add_argument_group('article filtering')
    filter_group.add_argument(
        "--include-file", type=str,
        default=None,
        help="Path to file containing article numbers to include (one per line)"
    )
    filter_group.add_argument(
        "--exclude-file", type=str,
        default=None,
        help="Path to file containing article numbers to exclude (one per line)"
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
        "--introduction", type=str,
        default=None,
        help="Path to introduction markdown file"
    )
    structure_group.add_argument(
        "--conclusion", type=str,
        default=None,
        help="Path to conclusion markdown file"
    )
    structure_group.add_argument(
        "--separator", type=str,
        default=None,
        help="HTML file containing separator between articles"
    )
    structure_group.add_argument(
        "--reflections-dir", type=str,
        default=None,
        help="Directory containing reflection markdown files for each article"
    )
    structure_group.add_argument(
        "--qr-dir", type=str,
        default=None,
        help="Directory containing QR code images"
    )
    
    return parser

def main():
    parser = setup_argument_parser()
    args = parser.parse_args()

    exclude_numbers = None
    if args.exclude_file:
        with open(args.exclude_file) as f:
            exclude_numbers = [line.strip() for line in f if line.strip()]

    include_numbers = None
    if args.include_file:
        with open(args.include_file) as f:
            include_numbers = [line.strip() for line in f if line.strip()]

    merge_md_files(
        directory=args.directory,
        output_file=args.output,
        qr_dir=args.qr_dir,
        include_numbers=include_numbers,
        exclude_numbers=exclude_numbers,
        cover_design=args.cover_design,
        back_cover_design=args.back_cover_design,
        separator=args.separator,
        introduction=args.introduction,
        conclusion=args.conclusion,
        reflections_dir=args.reflections_dir,
        pdf_options=args.pdf_options
    )

if __name__ == "__main__":
    main()
