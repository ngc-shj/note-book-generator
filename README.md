# Note Book Generator

ブログ記事や技術メモをPDF形式の電子書籍に変換するためのツールキットです。WordPress Export (WXR) ファイルから記事を抽出し、整形されたPDF書籍を生成します。

## 概要

Note Book Generator は、以下のような機能を提供します：

- WordPress エクスポート (WXR) ファイルからMarkdownへの変換
- 記事の選択的なフィルタリング（含める/除外する記事の指定）
- 目次 (TOC) の自動生成
- コードブロックの言語検出と行番号付与
- QRコードの自動生成（記事のオリジナルURLへのリンク用）
- 表紙、前付け、本文、あとがき、裏表紙などの構造化されたPDF生成
- 記事ごとのリフレクションの統合機能

## インストール方法

### 前提条件

- Python 3.7以上
- Node.js と npm（md-to-pdfのインストールに必要）

### 依存パッケージのインストール

```bash
# Python 依存パッケージのインストール
pip install -r requirements.txt

# md-to-pdfのインストール
npm install -g md-to-pdf
```

### リポジトリのクローン

```bash
git clone https://github.com/ngc-shj/note-book-generator.git
cd note-book-generator
```

### 初期設定

```bash
# 初期設定スクリプトの実行
./init.sh
```

このスクリプトは必要なディレクトリを作成し、設定ファイルのテンプレートをコピーします。

## 使い方

### 基本的な使い方

1. WordPressのエクスポートファイル（XML）を`input`ディレクトリに配置します
2. 必要に応じて設定ファイルを編集します
   - `config/exclude_articles.txt` - 除外する記事番号のリスト
   - `config/include_articles.txt` - 含める記事番号のリスト（指定すると、これだけが含まれます）
   - `config/pdf_options.yaml` - PDF変換のオプション設定
3. テンプレートファイルを編集します
   - `templates/cover.md` - 表紙のデザイン
   - `templates/toc.md` - 目次のテンプレート（通常は自動生成されます）
   - `templates/introduction.md` - 序論のテンプレート
   - `templates/conclusion.md` - 結論のテンプレート
   - `templates/back_cover.md` - 裏表紙のデザイン
   - `templates/separator.md` - 記事間のセパレータ
   - `templates/reflection.md.template` - リフレクションのテンプレート
4. CSSスタイルを編集します（必要に応じて）
   - `styles/style.css` - PDFのスタイル定義

### Makefileの使用

プロジェクトは `make` コマンドを使用して実行できます：

```bash
# 全工程を実行してPDFを生成
make

# 特定のタスクだけを実行
make articles        # WXRからMarkdownへの変換
make qrcodes         # QRコードの生成
make reflections     # リフレクションの生成
make cover           # 表紙の生成
make frontmatter     # 前付け（目次）の生成
make mainmatter      # 序論＋本文＋結論の生成
make back-cover      # 裏表紙の生成
make book            # 最終PDFの生成

# クリーンアップ
make clean           # 全ての生成ファイルを削除
make clean-articles  # 生成された記事ファイルのみ削除
make clean-outputs   # 出力ディレクトリのみ削除
```

### 設定項目の詳細

#### 記事の選択

`config/include_articles.txt` と `config/exclude_articles.txt` ファイルを使用して、含めたい/除外したい記事を指定できます。各ファイルには、記事番号を1行に1つずつ記述します。

#### PDF設定

`config/pdf_options.yaml` ファイルでPDFの基本設定を行います：

```yaml
format: A5                 # PDFサイズ（A5, A4など）
displayHeaderFooter: true  # ヘッダーとフッターを表示するかどうか
printBackground: true      # 背景色を印刷するかどうか
outlineStyle: auto         # アウトラインのスタイル
outlineOffset: 0           # アウトラインのオフセット
outlineMaxLevel: 3         # アウトラインの最大レベル
```

## ディレクトリ構造

```
note-book-generator/
├── config/                  # 設定ファイル
│   ├── exclude_articles.txt # 除外する記事番号
│   ├── include_articles.txt # 含める記事番号
│   └── pdf_options.yaml     # PDF変換の設定
├── input/                   # 入力ファイル（WXRファイルなど）
├── styles/                  # CSSスタイル定義
│   ├── style-base.css       # スタイルシート
│   ├── cover-style.css      # 表紙、裏表紙のスタイルシート
│   ├── frontmatter-style.css # 前付け（目次）のスタイルシート
│   └── mainmatter-style.css # 序論＋本文＋結論のスタイルシート
├── templates/               # テンプレートファイル
│   ├── cover.md             # 表紙
│   ├── introduction.md      # 序論
│   ├── conclusion.md        # 結論
│   ├── back_cover.md        # 裏表紙
│   ├── separator.md         # 記事間のセパレータ
│   └── reflection.md.template # リフレクションのテンプレート
├── src/                     # ソースコード
│   ├── wxr_to_md.py         # WXRからMarkdownへの変換
│   ├── merge_md_files.py    # Markdownファイルの結合
│   ├── generate_qr_codes.py # QRコードの生成
│   ├── generate_reflections.py # リフレクションの生成
│   ├── generate_toc.py      # 目次の生成
│   └── merge_pdf_files.py   # PDFファイルの結合
├── articles/                # 生成された記事
├── qrcodes/                 # 生成されたQRコード
├── reflections/             # 生成されたリフレクション
├── output/                  # 出力ディレクトリ
│   ├── md/                  # 中間Markdownファイル
│   ├── md/                  # 中間PDFファイル
│   └── note-book.pdf        # 生成されたPDFファイル
├── Makefile                 # makeコマンド定義
├── init.sh                  # 初期設定スクリプト
└── README.md                # このファイル
```

## カスタマイズ

### スタイルのカスタマイズ

ファイルを編集して、PDF出力のスタイルをカスタマイズできます：

- `styles/style-base.css` - 基本的なスタイル定義
- `styles/cover-style.css` - 表紙、裏表紙のスタイル定義
- `styles/frontmatter-style.css` - 前付け（目次）のスタイル定義
- `styles/mainmatter-style.css` - 序論、本文、結論のスタイル定義

主なスタイル定義には以下が含まれます：

- 本文、見出し、リンク、画像などの基本スタイル
- 表紙、裏表紙、目次、章区切りなどの特別なセクションのスタイル
- ページフォーマットやページブレークの制御

### テンプレートのカスタマイズ

各種テンプレートファイルを編集して、書籍の各部分をカスタマイズできます：

- `templates/cover.md` - 表紙のデザインとコンテンツ
- `templates/back_cover.md` - 裏表紙のデザインとコンテンツ
- `templates/introduction.md` - 序論のコンテンツ
- `templates/conclusion.md` - 結論のコンテンツ
- `templates/separator.md` - 記事間のセパレータのデザイン
- `templates/reflection.md.template` - リフレクションのテンプレート（変数置換が利用可能）

## トラブルシューティング

### よくある問題

- **エラー：md-to-pdfコマンドが見つかりません**
  - Node.jsとnpmが正しくインストールされているか確認してください
  - `npm install -g md-to-pdf` を実行してグローバルにインストールしてください

- **QRコードが生成されない**
  - `qrcode` Pythonパッケージがインストールされているか確認してください
  - 記事のリンクが有効かどうか確認してください

- **PDFの文字化けや表示の問題**
  - フォントが正しく設定されているか確認してください
  - CSSのスタイル定義を見直してください

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は[LICENSE](LICENSE)しファイルを参照してください。

## 貢献

バグレポートや機能リクエストは、GitHubのIssuesページで報告してください。Pull Requestsも歓迎します。

## クレジット

- WordPressエクスポート機能
- BeautifulSoup4 - HTML解析
- PyPDF2 - PDF操作
- md-to-pdf - MarkdownからPDFへの変換
- qrcode - QRコード生成
