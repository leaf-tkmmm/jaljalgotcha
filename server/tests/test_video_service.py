"""
VideoServiceのテスト
"""
import pytest
from unittest.mock import MagicMock
from src.jaljalgotcha.services.video_service import VideoService
from src.jaljalgotcha.repositories.interfaces import VideoRepository
from src.jaljalgotcha.models import Video, VideoCollection


@pytest.fixture
def mock_video_repository():
    """モックビデオリポジトリを提供するフィクスチャ"""
    mock_repo = MagicMock(spec=VideoRepository)
    
    # 仮の動画データ
    mock_videos = [
        Video(id="001", title="サンプル動画1", duration=120),  # 2分
        Video(id="002", title="サンプル動画2", duration=180),  # 3分
        Video(id="003", title="サンプル動画3", duration=300),  # 5分
    ]
    
    # get_videosメソッドがモックデータを返すように設定
    mock_repo.get_videos.return_value = mock_videos
    
    return mock_repo


@pytest.fixture
def video_service(mock_video_repository):
    """VideoServiceのインスタンスを提供するフィクスチャ"""
    return VideoService(mock_video_repository)


def test_filter_conversion(video_service, mock_video_repository):
    """フィルター変換機能のテスト"""
    # YouTube API形式のフィルター
    youtube_filters = {
        'max_results': 10,
        'order': 'date'
    }
    
    # サービスを呼び出す
    video_service.get_video_combinations(target_duration=600, filters=youtube_filters)
    
    # モックのget_videosが変換されたフィルターで呼ばれたことを確認
    mock_video_repository.get_videos.assert_called_once()
    args = mock_video_repository.get_videos.call_args[0]
    
    # 引数が辞書であることを確認
    assert isinstance(args[0], dict)
    
    # フィルターが正しく変換されていることを確認
    converted_filters = args[0]
    assert converted_filters['limit'] == 10
    assert converted_filters['order_by'] == 'date'
    assert converted_filters['order_dir'] == 'desc'


def test_db_specific_filters(video_service, mock_video_repository):
    """DB固有のフィルターが保持されることのテスト"""
    # DB固有のフィルターを含むリクエスト
    db_filters = {
        'max_duration': 300,
        'min_likes': 100,
        'min_views': 1000
    }
    
    # サービスを呼び出す
    video_service.get_video_combinations(target_duration=600, filters=db_filters)
    
    # モックのget_videosが同じフィルターで呼ばれたことを確認
    mock_video_repository.get_videos.assert_called_once()
    args = mock_video_repository.get_videos.call_args[0]
    
    # フィルターが正しく渡されていることを確認
    converted_filters = args[0]
    assert converted_filters['max_duration'] == 300
    assert converted_filters['min_likes'] == 100
    assert converted_filters['min_views'] == 1000