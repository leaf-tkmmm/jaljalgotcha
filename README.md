# JalJalGotcha

動画の時間組み合わせシステム - 指定した時間に合う複数の動画を組み合わせて提供するプロジェクト

## プロジェクト概要

このプロジェクトは JalJal の動画を指定した時間以内の組み合わせで提供するシステムです。例えば、入力が 10 分であれば、10 分以内の動画を複数組み合わせて提供します。

## プロジェクト構成

このプロジェクトは以下の構成になっています：

```
jaljalgotcha/
├── client/        # Reactフロントエンド（TypeScript, MUI, Tailwind CSS）
├── server/        # Flaskバックエンド（Python）
└── README.md      # このファイル
```

### フロントエンド（client/）

- **技術スタック**:

  - React 19
  - TypeScript
  - Material UI (MUI)
  - Tailwind CSS
  - Vite（ビルドツール）
  - Vitest（テストフレームワーク）
  - pnpm（パッケージマネージャー）

- **主要機能**:
  - 希望する時間の入力
  - 組み合わせ数の指定
  - データソースの選択（メモリ内サンプルデータまたは YouTube API）
  - 結果の表示

### バックエンド（server/）

- **技術スタック**:

  - Python
  - Flask
  - 依存性注入パターン
  - リポジトリパターン
  - YouTube API 連携（オプション）

- **主要機能**:
  - 動画データの管理
  - 指定時間に合う動画の組み合わせの計算
  - RESTful API

## セットアップ方法

### 前提条件

- Node.js 18 以上
- pnpm 9 以上
- Python 3.9 以上
- pip

### クライアント（フロントエンド）のセットアップ

```bash
# client ディレクトリに移動
cd client

# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm dev
```

### サーバー（バックエンド）のセットアップ

```bash
# server ディレクトリに移動
cd server

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定（必要に応じて）
cp .env.example .env
# .envファイルを編集してYOUTUBE_API_KEYを設定（YouTubeデータソースを使用する場合）

# サーバーの起動
python -m src.jaljalgotcha.main
```

## 使用方法

1. バックエンドサーバーを起動します（ポート 5000）
2. フロントエンド開発サーバーを起動します（ポート 5173）
3. ブラウザで http://localhost:5173 にアクセスします
4. フォームに希望する時間を入力し、必要に応じて設定を調整します
5. 「動画組み合わせを取得」ボタンをクリックして結果を取得します

## YouTube API の設定（オプション）

YouTube のデータソースを使用する場合は、Google Cloud Platform で YouTube Data API v3 の認証情報を取得し、`.env`ファイルに設定する必要があります：

```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## 開発者向け情報

詳細な開発者向け情報は、各ディレクトリ内の README.md ファイルを参照してください：

- [クライアント開発情報](client/README.md)
- [サーバー開発情報](server/README.md)
