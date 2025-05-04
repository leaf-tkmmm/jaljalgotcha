"""
SQLAlchemy を使用したデータベースリポジトリ実装
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy import create_engine

from ..models import Video
from ..db.models_db import VideoModel
from .interfaces import VideoRepository
from ..db.database import engine


class DbVideoRepository(VideoRepository):
    """SQLAlchemy を使用したデータベースリポジトリの実装"""
    
    def __init__(self, db_session: scoped_session[Session]):
        """
        初期化
        
        Args:
            db_session: SQLAlchemy セッション
        """
        self.db_session = db_session
        self.engine = engine
    
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
        # コンテキストマネージャを使用して自動ロールバック
        with Session(self.engine) as session:
            # クエリの作成
            query = session.query(VideoModel)
            
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
                thumbnail_url = getattr(db_video, 'thumbnail_url', None)
                
                videos.append(Video(
                    id=video_id,
                    title=title,
                    duration=duration_seconds,
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    thumbnail_url=thumbnail_url
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
        # コンテキストマネージャを使用して自動コミットまたはロールバック
        with Session(self.engine) as session:
            # 既存の動画を検索
            existing_video = session.query(VideoModel).filter(
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
                result = existing_video
            else:
                # 新しい動画を追加
                session.add(video_model)
                result = video_model
            
            # 変更をコミット（コンテキストマネージャのexitでコミット）
            session.commit()
            
            # 新しいインスタンスを返す（セッションはクローズされるため、detachedな状態で返す）
            return result
    
    def save_videos(self, video_models: List[VideoModel]) -> List[VideoModel]:
        """
        複数の動画をデータベースに保存する
        
        Args:
            video_models: 保存する VideoModel オブジェクトのリスト
            
        Returns:
            保存された VideoModel オブジェクトのリスト
        """
        # コンテキストマネージャを使用してセッションを管理
        with Session(self.engine) as session:
            saved_videos = []
            
            for video_model in video_models:
                # 既存の動画を検索
                existing_video = session.query(VideoModel).filter(
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
                    saved_videos.append(existing_video)
                else:
                    # 新しい動画を追加
                    session.add(video_model)
                    saved_videos.append(video_model)
            
            # 一括でコミット
            session.commit()
            
            return saved_videos
