"""
SQLAlchemy を使用したデータベースリポジトリ実装
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, scoped_session

from ..models import Video
from ..db.models_db import VideoModel
from .interfaces import VideoRepository


class DbVideoRepository(VideoRepository):
    """SQLAlchemy を使用したデータベースリポジトリの実装"""
    
    def __init__(self, db_session: scoped_session[Session]):
        """
        初期化
        
        Args:
            db_session: SQLAlchemy セッション
        """
        self.db = db_session
    
    def get_videos(self, filters: Optional[Dict[str, Any]] = None) -> List[Video]:
        """
        データベースから動画のリストを取得する
        
        Args:
            filters: フィルタリング条件（オプション）
                - max_duration: 最大動画時間（秒）
                - min_likes: 最小いいね数
                - min_views: 最小再生数
                - order_by: 並び順 ('duration', 'likes', 'views', 'published_at')
                - order_dir: 並び順の方向 ('asc', 'desc')
            
        Returns:
            動画のリスト
        """
        # クエリの作成
        query = self.db.query(VideoModel)
        
        # フィルタリング条件の適用
        if filters:
            if 'max_duration' in filters:
                query = query.filter(VideoModel.duration_seconds <= filters['max_duration'])
            
            if 'min_likes' in filters:
                query = query.filter(VideoModel.like_count >= filters['min_likes'])
            
            if 'min_views' in filters:
                query = query.filter(VideoModel.view_count >= filters['min_views'])
            
            # 並び順の適用
            order_by = filters.get('order_by', 'duration_seconds')
            order_dir = filters.get('order_dir', 'asc')
            
            # 並び順のカラムを取得
            if order_by == 'duration':
                order_column = VideoModel.duration_seconds
            elif order_by == 'likes':
                order_column = VideoModel.like_count
            elif order_by == 'views':
                order_column = VideoModel.view_count
            elif order_by == 'published_at':
                order_column = VideoModel.published_at
            else:
                order_column = VideoModel.duration_seconds
            
            # 並び順の方向を適用
            if order_dir == 'desc':
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column)
        else:
            # デフォルトは時間順
            query = query.order_by(VideoModel.duration_seconds)
        
        # クエリの実行
        db_videos = query.all()
        
        # VideoModel から Video モデルへの変換
        videos = []
        for db_video in db_videos:
            # VideoModel から Video モデルへの変換（型エラー回避のため getattr を使用）
            video_id = getattr(db_video, 'video_id')
            title = getattr(db_video, 'title')
            duration_seconds = getattr(db_video, 'duration_seconds')
            
            videos.append(Video(
                id=video_id,
                title=title,
                duration=duration_seconds,
                url=f"https://www.youtube.com/watch?v={video_id}"
            ))
        
        return videos
    
    def save_video(self, video_model: VideoModel) -> VideoModel:
        """
        動画をデータベースに保存する
        
        Args:
            video_model: 保存する VideoModel オブジェクト
            
        Returns:
            保存された VideoModel オブジェクト
        """
        # 既存の動画を検索
        existing_video = self.db.query(VideoModel).filter(
            VideoModel.video_id == video_model.video_id
        ).first()
        
        if existing_video:
            # 既存の動画を更新
            existing_video.channel_id = video_model.channel_id
            existing_video.title = video_model.title
            existing_video.duration_seconds = video_model.duration_seconds
            existing_video.view_count = video_model.view_count
            existing_video.like_count = video_model.like_count
            existing_video.comment_count = video_model.comment_count
            existing_video.thumbnail_url = video_model.thumbnail_url
            existing_video.published_at = video_model.published_at
            existing_video.updated_at = video_model.updated_at
        else:
            # 新しい動画を追加
            self.db.add(video_model)
        
        # 変更をコミット
        self.db.commit()
        
        # 新しく追加された場合のみリフレッシュ
        if existing_video:
            return existing_video
        else:
            self.db.refresh(video_model)
            return video_model
    
    def save_videos(self, video_models: List[VideoModel]) -> List[VideoModel]:
        """
        複数の動画をデータベースに保存する
        
        Args:
            video_models: 保存する VideoModel オブジェクトのリスト
            
        Returns:
            保存された VideoModel オブジェクトのリスト
        """
        saved_videos = []
        for video_model in video_models:
            saved_videos.append(self.save_video(video_model))
        
        return saved_videos
