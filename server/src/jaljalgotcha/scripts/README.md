# YouTube データ取得スクリプト

このスクリプトは、YouTube API を使用して指定したチャンネルの動画情報を取得し、PostgreSQL データベースに保存するためのものです。

## 前提条件

- Python 3.8 以上
- PostgreSQL データベース（Docker で実行）
- YouTube API キー

## 必要なパッケージ

以下のパッケージが必要です：

```
sqlalchemy
psycopg2-binary
google-api-python-client
python-dotenv
isodate
```

これらは `requirements.txt` に含まれています。

## 使い方

1. Docker で PostgreSQL を起動します：

```bash
cd server
docker-compose up -d
```

2. スクリプトを実行します：

```bash
cd server
python -m src.jaljalgotcha.scripts.fetch_youtube_data
```

## 設定

スクリプトは以下の環境変数を使用します：

- `YOUTUBE_API_KEY`: YouTube API キー
- `YOUTUBE_CHANNEL_ID`: 取得対象の YouTube チャンネル ID

これらの値は `.env` ファイルに設定されています。

## データベース

取得したデータは `videos` テーブルに保存されます。テーブル構造は以下の通りです：

```sql
CREATE TABLE videos (
    video_id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL,
    title TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    thumbnail_url TEXT,
    published_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT now()
);
```

## 注意事項

- YouTube API には 1 日あたりのクォータ制限があります。大量のデータを取得する場合は注意してください。
- スクリプトは既存のデータを更新するため、同じ動画 ID のデータが既に存在する場合は上書きされます。
