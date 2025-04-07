-- videos テーブル定義
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

-- よく使うカラムにインデックスを追加 (検索の高速化)
CREATE INDEX idx_like_count ON videos (like_count);
CREATE INDEX idx_comment_count ON videos (comment_count);
CREATE INDEX idx_duration_seconds ON videos (duration_seconds);
