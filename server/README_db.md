# DB設計
## テーブル定義
init.sql　に記載

## テスト用docker構成
docker-compose.yml　に記載

## videosテーブルの中身とyoutube apiで取得する情報の対応
|videos|youtube api|
|----|----|
|video_id|item["id"]|
|channel_id|channel_id|
|title|item["snippet"]["title"]|
|duration_seconds|duration|
|view_count|view_count|
|like_count|like_count|
|comment_count|comment_count|
|thumbnail_url|item["snippet"]["thumbnails"]["default"]["url"]|
|published_at|published_at|
|updated_at TIMESTAMP DEFAULT now()||


