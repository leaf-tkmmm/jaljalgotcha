# JalJalGotcha Client

JalJalGotcha のフロントエンド実装 - React, TypeScript, MUI, Tailwind CSS

## 技術スタック

- React 19
- TypeScript
- Material UI (MUI) - コンポーネントライブラリ
- Tailwind CSS - ユーティリティファースト CSS フレームワーク
- Vite - 高速なビルドツール
- Vitest - テストフレームワーク
- pnpm - パッケージマネージャー

## プロジェクト構造

```
client/
├── public/         # 静的ファイル
├── src/            # ソースコード
│   ├── components/ # Reactコンポーネント
│   │   ├── DurationForm.tsx     # 動画時間入力フォーム
│   │   ├── VideoList.tsx        # 動画一覧コンポーネント
│   │   └── VideoListItem.tsx    # 個別動画表示コンポーネント
│   ├── services/   # APIサービス
│   │   └── api.ts  # バックエンドAPI通信
│   ├── types/      # TypeScript型定義
│   │   └── index.ts
│   ├── App.tsx     # アプリケーションのメインコンポーネント
│   ├── main.tsx    # アプリケーションのエントリーポイント
│   └── index.css   # グローバルスタイル（Tailwind CSS）
├── test/           # テストファイル
├── index.html      # HTMLテンプレート
├── tailwind.config.js # Tailwind CSS設定
├── vite.config.ts  # Vite設定
└── tsconfig.json   # TypeScript設定
```

## 開発環境のセットアップ

```bash
# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm dev
```

## 利用可能なコマンド

- `pnpm dev` - 開発サーバーを起動（デフォルトでポート 5173）
- `pnpm build` - プロダクション用にアプリケーションをビルド
- `pnpm preview` - ビルドされたアプリケーションをプレビュー
- `pnpm test` - テストを実行
- `pnpm test:watch` - ウォッチモードでテストを実行
- `pnpm lint` - lint を実行

## 主要コンポーネント

### DurationForm

ユーザー入力を受け付けるフォームコンポーネント。以下の入力項目があります：

- 希望する時間（分単位または HH:MM:SS 形式）
- 生成する組み合わせの数
- データソース（メモリ内サンプルデータまたは YouTube API）

### VideoList

動画の組み合わせ一覧を表示するコンポーネント。各組み合わせには以下の情報が含まれます：

- 含まれる動画のリスト
- 合計時間
- 残り時間（指定した時間との差）

### VideoListItem

個別の動画情報を表示するコンポーネント。以下の情報が表示されます：

- 動画タイトル
- 動画時間
- 動画 URL（存在する場合）

## API との連携

`src/services/api.ts` に API クライアントが実装されており、バックエンドの Flask API と通信しています。主な機能は以下の通りです：

- `getCombinations()` - 指定された時間に合う動画の組み合わせを取得

## 環境変数

本プロジェクトでは、Vite の環境変数機能を使用しています。`.env`ファイルを作成することで、環境固有の設定を行うことができます。

例：

```
VITE_API_URL=http://localhost:5000
```

## バックエンドとの連携

開発時には、Vite のプロキシ機能を使用して、API リクエストをバックエンドサーバー（デフォルトでポート 5000）に転送しています。この設定は `vite.config.ts` で行われています。
