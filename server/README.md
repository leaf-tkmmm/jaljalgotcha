# JalJalGotcha

動画時間を入力すると、その時間内に収まる動画の組み合わせを提供するシステム

## 機能

- 指定した時間内に収まる動画の組み合わせを提供
- 使い切れなかった時間を最小化するアルゴリズム

## 開発環境のセットアップ

```bash
# 仮想環境のアクティベート
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 開発用（テスト実行時）
pytest
```

## 使用方法

```bash
# Flaskサーバーの起動
python -m src.jaljalgotcha.main
```

## プロジェクト構造

```
jaljalgotcha/
├── .gitignore               # Git管理から除外するファイル
├── README.md                # プロジェクト説明
├── requirements.txt         # 依存パッケージ
├── src/                     # ソースコード
│   └── jaljalgotcha/
│       ├── __init__.py      # パッケージ化
│       ├── main.py          # アプリケーションのエントリーポイント
│       ├── models.py        # データモデル
│       ├── video.py         # 動画処理のロジック
│       └── utils.py         # ユーティリティ関数
└── tests/                   # テストコード
    ├── __init__.py
    └── test_video.py        # ビデオ処理のテスト
```
