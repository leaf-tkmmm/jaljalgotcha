"""
DbVideoRepositoryのテスト
"""
import pytest
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch

# psycopg2のインポートをモックして、実際のDB接続を回避
with patch.dict(sys.modules, {'psycopg2': MagicMock()}):
    from src.jaljalgotcha.repositories.db_repository import DbVideoRepository
    from src.jaljalgotcha.repositories.interfaces import VideoRepository
    from src.jaljalgotcha.db.models_db import VideoModel


@pytest.fixture
def mock_db_session():
    """モックDBセッションを提供するフィクスチャ"""
    mock_session = MagicMock()
    
    # モッククエリの作成
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # フィルターメソッドがクエリを返すようにする
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    
    # サンプルデータを生成
    mock_videos = [
        VideoModel(
            video_id="001",
            channel_id="channel1",
            title="サンプル動画1",
            duration_seconds=120,
            view_count=1000,
            like_count=100,
            comment_count=10,
            thumbnail_url="https://example.com/thumb1.jpg",
            published_at=datetime(2023, 1, 1),
            updated_at=datetime.now()
        ),
        VideoModel(
            video_id="002",
            channel_id="channel1",
            title="サンプル動画2",
            duration_seconds=180,
            view_count=2000,
            like_count=200,
            comment_count=20,
            thumbnail_url="https://example.com/thumb2.jpg",
            published_at=datetime(2023, 1, 2),
            updated_at=datetime.now()
        )
    ]
    
    # allメソッドがサンプルデータを返すようにする
    mock_query.all.return_value = mock_videos
    
    return mock_session


@pytest.fixture
def db_repository(mock_db_session):
    """DbVideoRepositoryのインスタンスを提供するフィクスチャ"""
    return DbVideoRepository(mock_db_session)


def test_repository_interface(db_repository):
    """VideoRepositoryインターフェースを実装していることを確認"""
    assert isinstance(db_repository, VideoRepository)


def test_get_videos_without_filters(db_repository, mock_db_session):
    """フィルターなしで動画を取得するテスト"""
    # リポジトリメソッドを呼び出す
    videos = db_repository.get_videos()
    
    # 正しいクエリが実行されたことを確認
    mock_db_session.query.assert_called_once()
    mock_query = mock_db_session.query.return_value
    mock_query.order_by.assert_called_once()
    mock_query.all.assert_called_once()
    
    # 返された動画のリストを確認
    assert len(videos) == 2
    assert videos[0].id == "001"
    assert videos[1].id == "002"


def test_get_videos_with_filters(db_repository, mock_db_session):
    """フィルター付きで動画を取得するテスト"""
    # フィルターを指定
    filters = {
        'max_duration': 200,
        'min_likes': 50,
        'min_views': 500,
        'order_by': 'likes',
        'order_dir': 'desc'
    }
    
    # リポジトリメソッドを呼び出す
    videos = db_repository.get_videos(filters)
    
    # 正しいクエリが実行されたことを確認
    mock_query = mock_db_session.query.return_value
    assert mock_query.filter.call_count >= 3  # 3つのフィルター条件
    mock_query.order_by.assert_called_once()  # 並び順が指定されている
    
    # 返された動画のリストを確認
    assert len(videos) == 2


def test_save_video(db_repository, mock_db_session):
    """動画の保存テスト"""
    # 新しい動画モデルを作成
    new_video = VideoModel(
        video_id="003",
        channel_id="channel1",
        title="新しい動画",
        duration_seconds=240,
        view_count=300,
        like_count=30,
        comment_count=3,
        thumbnail_url="https://example.com/thumb3.jpg",
        published_at=datetime(2023, 1, 3),
        updated_at=datetime.now()
    )
    
    # モックのqueryでfirstメソッドがNoneを返すように設定（新規追加のケース）
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value.first.return_value = None
    
    # 保存を実行
    result = db_repository.save_video(new_video)
    
    # addとcommitが呼ばれたことを確認
    mock_db_session.add.assert_called_once_with(new_video)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(new_video)
    
    # 結果を確認
    assert result == new_video