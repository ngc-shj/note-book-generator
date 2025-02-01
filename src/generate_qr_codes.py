#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import qrcode
import pandas as pd
import argparse

def generate_qr_codes(csv_file, output_dir):
    """ 指定されたCSVファイルからURLを取得し、QRコードを生成 """

    # QRコード保存先フォルダの作成
    os.makedirs(output_dir, exist_ok=True)

    # 記事一覧を読み込む
    try:
        df = pd.read_csv(csv_file, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: ファイル {csv_file} が見つかりません。")
        return

    # 必要なカラムがあるかチェック
    if "filename" not in df.columns or "link" not in df.columns:
        print("Error: CSVファイルに 'filename' または 'link' のカラムがありません。")
        return

    # 記事ごとのQRコードを生成
    for index, row in df.iterrows():
        filename = row["filename"]
        link = row["link"]

        if pd.isna(link) or link.strip() == "" or link == "No Link":
            print(f"Skipping {filename} (no valid link)")
            continue

        # QRコードを作成
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        # QRコード画像を生成
        img = qr.make_image(fill="black", back_color="white")

        # `.md` 拡張子を除去し、安全なファイル名を生成
        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(output_dir, f"{base_filename}.png")

        # 画像を保存
        img.save(file_path)
        print(f"Saved QR Code: {file_path}")

    print("QRコードの生成が完了しました。")

def setup_argument_parser():
    """ コマンドライン引数を設定 """
    parser = argparse.ArgumentParser(description="Generate QR codes from a CSV file containing article URLs.")
    
    parser.add_argument(
        "--csv",
        type=str,
        default="articles/articles.csv",
        help="Path to the CSV file containing article URLs (default: articles/articles.csv)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="qrcodes",
        help="Directory where QR codes will be saved (default: qrcodes)"
    )

    return parser

def main():
    parser = setup_argument_parser()
    args = parser.parse_args()

    generate_qr_codes(args.csv, args.output_dir)

if __name__ == "__main__":
    main()

