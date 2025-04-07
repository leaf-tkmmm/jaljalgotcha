"""
SQLAlchemy データベースモデル
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VideoModel(Base):
    """
    動画テーブルのSQLAlchemyモデル
    
    テーブル定義:
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
    """
    __tablename__ = 'videos'
    
    video_id = Column(String, primary_key=True)
    channel_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    view_count = Column(BigInteger, default=0)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    thumbnail_url = Column(String)
    published_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Video(video_id='{self.video_id}', title='{self.title}', duration_seconds={self.duration_seconds})>"
