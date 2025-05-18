"""
データベースリポジトリとAPIの統合
"""
from .repositories.video_repository import DbVideoRepository
from .db.database import db_session, init_db
from .di.container import container
from .services.video_service import VideoService


def setup_video_repository():
    """
    データベースリポジトリをDIコンテナに登録する
    """
    # データベースの初期化
    init_db()
    
    # データベースリポジトリを登録
    container.register('db_video_repository', lambda c: DbVideoRepository(db_session))
    
    # ビデオサービスを登録
    container.register('db_video_service', lambda c: VideoService(c.get('db_video_repository')))


def get_db_video_service() -> VideoService:
    """
    データベースを使用するビデオサービスを取得する
    
    Returns:
        VideoService: データベースリポジトリを使用するビデオサービス
    """
    setup_video_repository()
    return container.get('db_video_service')
