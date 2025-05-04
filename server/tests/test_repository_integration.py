"""
DbVideoRepositoryとVideoServiceの統合テスト
"""
import pytest
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime

# psycopg2のインポートをモックして、実際のDB接続を回避
with patch.dict(sys.modules, {'psycopg2': MagicMock()}):
    from server.src.jaljalgotcha.repositories.video_repository import DbVideoRepository
    from src.jaljalgotcha.services.video_service import VideoService
    from src.jaljalgotcha.db.models_db import VideoModel
    from src.jaljalgotcha.models import Video


@pytest.fixture
def mock_db_videos():
    """モックデータベース動画のリストを提供するフィクスチャ"""
    return [
        VideoModel(
            video_id="001",
            channel_id="channel1",
            title="サンプル動画1",
            duration_seconds=120,  # 2分
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
            duration_seconds=180,  # 3分
            view_count=2000,
            like_count=200,
            comment_count=20,
            thumbnail_url="https://example.com/thumb2.jpg",
            published_at=datetime(2023, 1, 2),
            updated_at=datetime.now()
        ),
        VideoModel(
            video_id="003",
            channel_id="channel1",
            title="サンプル動画3",
            duration_seconds=240,  # 4分
            view_count=3000,
            like_count=300,
            comment_count=30,
            thumbnail_url="https://example.com/thumb3.jpg",
            published_at=datetime(2023, 1, 3),
            updated_at=datetime.now()
        ),
    ]


@pytest.fixture
def mock_db_session(mock_db_videos):
    """モックDBセッションを提供するフィクスチャ"""
    mock_session = MagicMock()
    
    # モッククエリの設定
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # フィルタメソッドの振る舞いを設定
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    
    # allメソッドがサンプルデータを返すように設定
    mock_query.all.return_value = mock_db_videos
    
    return mock_session


@pytest.fixture
def video_repository(mock_db_session):
    """DbVideoRepositoryのインスタンスを提供するフィクスチャ"""
    return DbVideoRepository(mock_db_session)


@pytest.fixture
def video_service(video_repository):
    """VideoServiceのインスタンスを提供するフィクスチャ"""
    return VideoService(video_repository)


def test_video_service_with_youtube_filters(video_service, mock_db_session):
    """YouTube APIフィルター形式を使用した統合テスト"""
    # YouTube API形式のフィルター
    youtube_filters = {
        'max_results': 10,
        'order': 'date'
    }
    
    # 動画の組み合わせを取得
    combinations = video_service.get_video_combinations(
        target_duration=600,
        filters=youtube_filters
    )
    
    # 結果を検証
    assert len(combinations) > 0
    
    # DBクエリが正しく呼び出されたことを確認
    mock_query = mock_db_session.query.return_value
    mock_query.order_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_video_service_with_db_filters(video_service, mock_db_session):
    """DB固有のフィルター形式を使用した統合テスト"""
    # DB固有のフィルター
    db_filters = {
        'max_duration': 300,
        'min_likes': 100,
        'min_views': 1000
    }
    
    # 動画の組み合わせを取得
    combinations = video_service.get_video_combinations(
        target_duration=600,
        filters=db_filters
    )
    
    # 結果を検証
    assert len(combinations) > 0
    
    # 各組み合わせが目標時間以内であることを確認
    for combo in combinations:
        assert combo.total_time <= 600
        
    # 結果がソートされていることを確認（残り時間が少ない順）
    for i in range(1, len(combinations)):
        assert combinations[i-1].remaining_time <= combinations[i].remaining_time