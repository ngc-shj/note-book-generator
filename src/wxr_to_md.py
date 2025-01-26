#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import re
import argparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import parsedate_to_datetime

################################################################################
# 1) 既存のコード言語判定・コードブロックエスケープ関数
################################################################################

def detect_code_language(code_content: str) -> str:
    """コードの内容から言語を判定する"""
    python_keywords = [">>> ", "def ", "import ", "from ", "class ", "else:", "try:", "except:", "print(", "return "]
    bash_keywords = ["$ ", "pip", "ls", "cat", "grep", "echo", "cd", "sudo", "chmod", "apt", "yum", "brew",
                     "python", "python3", "modular install", "curl", "wget"]

    content_lower = code_content.lower()

    # Python判定
    for keyword in python_keywords:
        if keyword.lower() in content_lower:
            return "python"
    # Bash判定
    for keyword in bash_keywords:
        if keyword.lower() in content_lower:
            return "bash"
    # 見つからなければ text
    return "text"

################################################################################
# 2) Main: WXR解析 → BeautifulSoupでHTML→Markdown変換
################################################################################

def parse_wxr_to_markdown(wxr_file, output_dir):
    """WXRファイルを読み込み、各<item>のcontentをMarkdown変換して保存"""
    os.makedirs(output_dir, exist_ok=True)
    tree = ET.parse(wxr_file)
    root = tree.getroot()

    # WordPressエクスポートで使用される名前空間
    namespace = {'content': 'http://purl.org/rss/1.0/modules/content/'}

    # 記事一覧ファイル用
    article_list = []
    counter = 1

    # 各<item>を走査
    for item in root.findall(".//item"):
        # 公開記事のみ
        status = item.find('./{http://wordpress.org/export/1.2/}status')
        if status is not None and status.text.strip() != "publish":
            continue

        title_elem = item.find('title')
        title = title_elem.text.strip() if title_elem is not None else "No Title"

        content_elem = item.find('content:encoded', namespace)
        content_html = content_elem.text if content_elem is not None else ""

        pub_date_elem = item.find('pubDate')
        if pub_date_elem is not None and pub_date_elem.text:
            dt = parsedate_to_datetime(pub_date_elem.text.strip())
            pub_date = dt.strftime('%Y年%-m月%-d日 %H:%M')
        else:
            pub_date = "No Date"

        # ベースパス: WXRファイルと同じディレクトリを起点に処理(例)
        base_path = os.path.dirname(wxr_file)

        # HTML→Markdown変換
        content_md = html_to_markdown_bs(content_html, base_path=base_path)

        # ファイル名に使えない文字を除去
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
        filename = f"{counter:04d}_{safe_title}.md"
        out_path = os.path.join(output_dir, filename)

        with open(out_path, 'w', encoding='utf-8') as md:
            md.write(f"# Title: {title}\n\n")
            md.write(f"**公開日**: {pub_date}\n\n")
            md.write(content_md.strip() + "\n\n")

        print(f"Saved: {out_path}")

        # 記事一覧に追加
        article_list.append({
            'number': f"{counter:04d}",
            'title': title,
            'filename': filename,
            'pub_date': pub_date
        })
        counter += 1

    # 記事一覧を出力
    list_path = os.path.join(output_dir, "articles.csv")
    with open(list_path, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['number', 'title', 'filename', 'pub_date'])
        writer.writeheader()
        writer.writerows(article_list)


################################################################################
# 3) BeautifulSoupによるノード単位のHTML→Markdown変換
################################################################################

def format_linebreaks_with_markdown(inner_md: str, markdown_format: str) -> str:
    """
    Markdownフォーマットを適用しながら改行コードを補正します。

    Args:
        inner_md (str): 処理対象の文字列
        markdown_format (str): Markdownの書式（例: "**", "_", "~~"）

    Returns:
        str: 改行コードを補正し、Markdownフォーマットが適用された文字列
    """
    if not inner_md:
        return ""  # 空の場合は何も返さない

    if inner_md == "__BR__":
        return "  \n"  # `__BR__` のみの場合は改行

    if "__BR__" in inner_md:
        # `__BR__` を改行 + マークダウン書式として処理
        parts = inner_md.split("__BR__")
        formatted_parts = []
        for idx, part in enumerate(parts):
            part = part.strip()
            if part:
                formatted_parts.append(f"{markdown_format}{part}{markdown_format}")
            # `__BR__` の位置に改行を挿入
            if idx < len(parts) - 1:
                formatted_parts.append("  \n")
        return "".join(formatted_parts)  # フォーマット済み文字列を結合

    # 通常のMarkdownフォーマット（日本語隣接対策の空白を含む）
    return f" {markdown_format}{inner_md}{markdown_format} "

def html_to_markdown_bs(html_text: str, base_path: str = ".") -> str:
    """BeautifulSoupでパース後、ノード単位でMarkdown変換"""
    soup = BeautifulSoup(html_text, "html.parser")

    md_fragments = []
    # soup.contents: 最上位のノードを列挙
    for elem in soup.contents:
        frag = bs_node_to_md(elem, level=0, base_path=base_path)
        if frag.strip():
            md_fragments.append(frag)

    return "\n".join(md_fragments)

def bs_node_to_md(node, level=0, base_path=".") -> str:
    """
    BeautifulSoupのノードを再帰的にMarkdown文字列へ。
      - level: リストのネスト等でインデントを増やす
      - base_path: /assets/画像パスの相対変換用
    """
    from bs4 import NavigableString, Tag

    # 1) 文字列の場合
    if isinstance(node, NavigableString):
        return node.strip()

    # 2) タグの場合
    if not isinstance(node, Tag):
        return ""

    tname = node.name.lower()

    # 見出し
    if tname in ("h1", "h2", "h3", "h4", "h5", "h6"):
        depth = int(tname[-1])  # h1->1, h2->2, ...
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        return f"\n{'#'*depth} {inner_md.strip()}\n"

    # 段落/汎用ブロック
    elif tname in ("p", "div"):
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        if inner_md.strip():
            return f"\n{inner_md.strip()}\n"
        return ""

    # 改行
    elif tname == "br":
        # 親タグが <strong>/<b>/<em>/<i>/<s> 等ならスペースにする
        parent_tag = node.parent.name.lower() if node.parent else ""
        if parent_tag in ("strong", "b", "em", "i", "s"):
            return "__BR__"  # インライン要素内の<br>は要チェック
        else:
            return "  \n"  # それ以外は通常のMarkdown改行

    # 水平線
    elif tname == "hr":
        return "\n---\n"

    # 太字
    elif tname in ("b", "strong"):
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        inner_md = inner_md.strip()
        return format_linebreaks_with_markdown(inner_md, "**")

    # イタリック
    elif tname in ("i", "em"):
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        inner_md = inner_md.strip()
        return format_linebreaks_with_markdown(inner_md, "*")

    # 取り消し線
    elif tname == "s":
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        inner_md = inner_md.strip()
        return format_linebreaks_with_markdown(inner_md, "~~")

    # リンク
    elif tname == "a":
        href = node.get("href", "")
        text_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children).strip()

        if node.parent:
            parent_tag = node.parent.parent.name.lower() if node.parent.parent else ""
            if parent_tag in ("blockquote"):
                if text_md == href:
                    return f" [{href}]({href}) "
                else:
                    return f" {text_md}({href}) "

        if href:
            if text_md == href:
                return f"[{href}]({href}) "
            else:
                return f"[{text_md}]({href})({href}) "
        else:
            return text_md

    # リスト (ul/ol)
    elif tname in ("ul", "ol"):
        is_ordered = (tname == "ol")
        md_list = []
        idx = 1
        # 直下の<li>のみ
        for li in node.find_all("li", recursive=False):
            li_md = "".join(bs_node_to_md(c, level+1, base_path) for c in li.children).strip()
            indent = "    " * level
            if is_ordered:
                md_list.append(f"{indent}{idx}. {li_md}")
                idx += 1
            else:
                md_list.append(f"{indent}- {li_md}")
        return "\n".join(md_list)

    # 画像
    elif tname == "img":
        src = node.get("src", "")
        alt = node.get("alt", "")
        # /assets/ → 相対パスへ置換
        if src.startswith("/assets/"):
            src = f"./{os.path.join(base_path, src.lstrip('/'))}"
        return f"![{alt}]({src})"

    # figure
    elif tname == "figure":
        sub_md = []
        for c in node.children:
            sub_md.append(bs_node_to_md(c, level, base_path))
        content = "\n".join(sub_md).strip()
        return f"\n{content}\n" if content else ""

    # figcaption
    elif tname == "figcaption":
        cap_text = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        if cap_text:
            previous_tag = node.previous_sibling.name.lower() if node.previous_sibling else ""
            if previous_tag in ("img"):
                return f"\n<p class=\"figure\">{cap_text.strip()}</p>\n"
            else:
                return f"\n<p class=\"source\">{cap_text.strip()}</p>\n"
        else:
            return ""

    # blockquote
    elif tname == "blockquote":
        block_lines = []
        for c in node.children:
            child_md = bs_node_to_md(c, level, base_path)
            for ln in child_md.split("\n"):
                if ln:
                    ln = ln.replace("<", "&lt;")
                    ln = ln.replace(">", "&gt;")
                    ln = f"\\{ln}" if re.match(r'^#+ ', ln) else ln
                    ln = f"\\{ln}" if re.match(r'^---', ln) else ln
                    ln = ln.replace("`", "\\`")
                    ln = ln.replace("[", "\\[")
                    ln = ln.replace("]", "\\]")
                    block_lines.append(f"> {ln}")
                #else:
                #    block_lines.append(">")
        return "\n".join(block_lines)

    # コード(インライン/ブロック)
    elif tname == "code":
        # もし親が<pre>なら、<pre>側でまとめて処理する
        # ここでは「インラインcode」として扱う
        code_text = node.get_text()
        return f"`{code_text.strip()}`"

    elif tname == "pre":
        # <pre> の中に <code> がある場合はコードブロック
        code_tag = node.find("code")
        if code_tag:
            raw_code = code_tag.get_text()
            # 言語判定
            lang = detect_code_language(raw_code)
            #return f"\n````{lang}\n{raw_code}\n````\n"
            # 行番号を追加
            numbered_lines = []
            for i, line in enumerate(raw_code.split('\n'), 1):
               numbered_lines.append(f"{i:03d} {line}")
            numbered_code = '\n'.join(numbered_lines)
            return f"\n````{lang}\n{numbered_code}\n````\n"
        else:
            # <pre> だけの場合もコードブロック
            raw_code = node.get_text()
            lang = detect_code_language(raw_code)
            return f"\n````{lang}\n{raw_code}\n````\n"

    # それ以外のタグは子ノードを連結して返す
    else:
        print(tname)
        inner_md = "".join(bs_node_to_md(c, level, base_path) for c in node.children)
        return inner_md

def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Convert WXR file to Markdown with code detection & image path fix.")

    # Required arguments
    required_group = parser.add_argument_group('required arguments') 
    required_group.add_argument("wxr_file", help="Path to the WXR file")
    required_group.add_argument("output_dir", help="Output directory for .md files")

    return parser

def main():
    parser = setup_argument_parser()
    args = parser.parse_args()

    parse_wxr_to_markdown(args.wxr_file, args.output_dir)

if __name__ == "__main__":
    main()

