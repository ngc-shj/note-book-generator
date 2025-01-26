#!/usr/bin/env python3
import os
import csv
import argparse
from datetime import datetime
from typing import List, Optional, Set

def load_article_numbers(file_path: str) -> Set[str]:
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        return {f"{int(line.strip()):04d}" for line in f if line.strip()}

def generate_reflection_template(
    articles_csv: str, 
    output_dir: str,
    include_list: Optional[str] = None,
    exclude_list: Optional[str] = None
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    
    include_numbers = load_article_numbers(include_list) if include_list else set()
    exclude_numbers = load_article_numbers(exclude_list) if exclude_list else set()
    
    with open(articles_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            number = row['number']
            title = row['title']

            if include_numbers and number not in include_numbers:
                continue
            if number in exclude_numbers:
                continue

            reflection_path = os.path.join(output_dir, f"{number}_reflection.md")
            if not os.path.exists(reflection_path):
                with open(reflection_path, 'w', encoding='utf-8') as rf:
                    current_date = datetime.now().strftime("%Y年%m月")
                    rf.write(f"## 振り返り ({current_date})\n\n")
                    rf.write(f"「{title}」について：\n\n")
                    rf.write("元記事では[要点]について述べましたが、[新しい視点/現状分析]により、[今日的な意義/課題]が明らかになっています。\n\n")
                    rf.write("[具体的な展開や今後の展望]\n")

def main():
    parser = argparse.ArgumentParser(description="Generate reflection markdown templates from articles.csv")
    parser.add_argument("articles_csv", help="Path to articles.csv")
    parser.add_argument("--output-dir", default="reflections", help="Output directory for reflection files")
    parser.add_argument("--include-file", help="Path to file containing article numbers to include")
    parser.add_argument("--exclude-file", help="Path to file containing article numbers to exclude")
    args = parser.parse_args()
    
    generate_reflection_template(
        args.articles_csv, 
        args.output_dir,
        args.include_file,
        args.exclude_file
    )

if __name__ == "__main__":
    main()
