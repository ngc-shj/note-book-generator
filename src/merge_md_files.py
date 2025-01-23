import os
import re
import argparse
import yaml
from typing import List, Optional

def merge_md_files(
   directory: str,
   output_file: str,
   exclude_numbers: List[str],
   cover_design: Optional[str] = None,
   pdf_options: Optional[str] = None,
   separator: Optional[str] = None
) -> None:
    exclude_numbers = set(f"{int(num):04}" for num in exclude_numbers)  # ゼロ埋めした番号を生成
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

        for md_file in md_files:
            match = re.match(r"^(\d{4})_", md_file)
            if match:
                article_number = match.group(1)
                if article_number not in exclude_numbers:
                    file_path = os.path.join(directory, md_file)
                    with open(file_path, "r", encoding="utf-8") as input_file:
                        output.write(input_file.read())
                        if input_file != md_files[-1]:
                            output.write("\n\n")
                            output.write(sep)
                            output.write("\n\n")

def main():
    parser = argparse.ArgumentParser(description="Merge .md files in a directory with an optional cover page, excluding specified articles.")
    parser.add_argument("directory", type=str, help="Directory containing .md files to merge.")
    parser.add_argument(
        "--output", type=str,
        default="merged_output.md", 
        help="Output file name for the merged content. Default is 'merged_output.md'."
    )
    parser.add_argument(
        "--exclude-file", type=str,
        default=None,
        help="Path to file containing article numbers to exclude (one per line)"
    )
    parser.add_argument(
        "--cover-design", type=str,
        default=None,
        help="Path to the cover file (optional)."
    )
    parser.add_argument(
        "--pdf-options", type=str,
        default=None,
        help="YAML file with PDF options for md-to-pdf"
    )
    parser.add_argument(
        "--separator", type=str,
        default=None,
        help="HTML file containing separator between articles",
    )

    args = parser.parse_args()

    exclude_numbers = []
    if args.exclude_file:
        with open(args.exclude_file) as f:
            exclude_numbers.extend(line.strip() for line in f if line.strip())

    merge_md_files(
        directory=args.directory, 
        output_file=args.output, 
        exclude_numbers=exclude_numbers, 
        cover_design=args.cover_design,
        pdf_options=args.pdf_options,
        separator=args.separator
    )

if __name__ == "__main__":
    main()

