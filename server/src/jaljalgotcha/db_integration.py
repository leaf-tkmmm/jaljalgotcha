"""
データベースリポジトリとAPIの統合
"""
from .repositories.db_repository import DbVideoRepository
from .db.database import db_session, init_db
from .di.container import container
from .services.video_service import VideoService


def setup_db_repository():
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
    # データベースリポジトリが登録されていない場合は登録
    if 'db_video_repository' not in container._factory_methods:
        setup_db_repository()
    
    return container.get('db_video_service')
