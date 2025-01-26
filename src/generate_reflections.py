#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import argparse
from datetime import datetime
from string import Template
from typing import List, Optional, Set

def load_article_numbers(file_path: str) -> Set[str]:
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        return {f"{int(line.strip()):04d}" for line in f if line.strip()}

def read_template(template_path: str) -> Template:
    with open(template_path, 'r', encoding='utf-8') as f:
        return Template(f.read())

def generate_reflection_template(
    articles_csv: str, 
    output_dir: str,
    template_path: str,
    include_list: Optional[str] = None,
    exclude_list: Optional[str] = None
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    
    include_numbers = load_article_numbers(include_list) if include_list else set()
    exclude_numbers = load_article_numbers(exclude_list) if exclude_list else set()
    
    template = read_template(template_path)
    current_date = datetime.now().strftime("%Y年%m月")
    
    with open(articles_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            number = row['number']
            title = row['title']
            pub_date = row['pub_date']

            if include_numbers and number not in include_numbers:
                continue
            if number in exclude_numbers:
                continue

            reflection_path = os.path.join(output_dir, f"{number}_reflection.md")
            if not os.path.exists(reflection_path):
                with open(reflection_path, 'w', encoding='utf-8') as rf:
                    content = template.substitute(
                        date=current_date,
                        title=title,
                        pub_date=pub_date
                    )
                    rf.write(content)

def main():
    parser = argparse.ArgumentParser(description="Generate reflection markdown templates from articles.csv")
    parser.add_argument("articles_csv", help="Path to articles.csv")
    parser.add_argument("--output-dir", default="reflections", help="Output directory for reflection files")
    parser.add_argument("--template", required=True, help="Path to template file")
    parser.add_argument("--include-file", help="Path to file containing article numbers to include")
    parser.add_argument("--exclude-file", help="Path to file containing article numbers to exclude")
    args = parser.parse_args()
    
    generate_reflection_template(
        args.articles_csv,
        args.output_dir,
        args.template,
        args.include_file,
        args.exclude_file
    )

if __name__ == "__main__":
    main()

