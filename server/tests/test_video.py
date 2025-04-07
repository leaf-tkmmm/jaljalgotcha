"""
動画処理モジュールのテスト
"""
import pytest
from src.jaljalgotcha.models import Video
from src.jaljalgotcha.video import (
    sort_videos_by_duration,
    filter_videos_by_max_duration,
    select_videos,
    get_video_combinations
)


@pytest.fixture
def sample_videos():
    """サンプル動画データを提供するフィクスチャ"""
    return [
        Video(id="001", title="サンプル動画1", duration=120),  # 2分
        Video(id="002", title="サンプル動画2", duration=180),  # 3分
        Video(id="003", title="サンプル動画3", duration=300),  # 5分
        Video(id="004", title="サンプル動画4", duration=240),  # 4分
        Video(id="005", title="サンプル動画5", duration=150),  # 2分30秒
    ]


def test_sort_videos_by_duration(sample_videos):
    """動画時間によるソートのテスト"""
    sorted_videos = sort_videos_by_duration(sample_videos)
    
    # 時間順に並んでいることを確認
    durations = [v.duration for v in sorted_videos]
    assert durations == sorted(durations)
    
    # 最初が最短、最後が最長であることを確認
    assert sorted_videos[0].duration == 120
    assert sorted_videos[-1].duration == 300


def test_filter_videos_by_max_duration(sample_videos):
    """最大時間によるフィルタリングのテスト"""
    # 3分以下の動画をフィルタリング
    filtered = filter_videos_by_max_duration(sample_videos, 180)
    
    # 3つの動画が該当する（120秒、150秒、180秒）
    assert len(filtered) == 3
    
    # すべての動画が180秒以下であることを確認
    for video in filtered:
        assert video.duration <= 180


def test_select_videos(sample_videos):
    """動画選択機能のテスト"""
    # 10分（600秒）の時間枠で選択
    result = select_videos(sample_videos, 600)
    
    # 結果がVideoCollectionオブジェクトであることを確認
    assert hasattr(result, 'videos')
    assert hasattr(result, 'total_time')
    assert hasattr(result, 'remaining_time')
    
    # 少なくとも1つの動画が選択されていることを確認
    assert len(result.videos) > 0
    
    # 合計時間が目標時間以下であることを確認
    assert result.total_time <= 600
    
    # 残り時間が正しく計算されていることを確認
    assert result.remaining_time == 600 - result.total_time


def test_get_video_combinations(sample_videos):
    """複数の動画組み合わせ生成のテスト"""
    # 5分（300秒）の時間枠で3つの組み合わせを生成
    combinations = get_video_combinations(sample_videos, 300, 3)
    
    # 3つの組み合わせが生成されていることを確認
    assert len(combinations) == 3
    
    # すべての組み合わせの合計時間が目標時間以下であることを確認
    for combo in combinations:
        assert combo.total_time <= 300
        
    # 残り時間が少ない順にソートされていることを確認
    remaining_times = [combo.remaining_time for combo in combinations]
    assert remaining_times == sorted(remaining_times)
