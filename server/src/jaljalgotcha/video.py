"""
動画処理のロジック
"""
import random
from typing import List, Tuple

from .models import Video, VideoCollection


def sort_videos_by_duration(videos: List[Video]) -> List[Video]:
    """
    動画を時間順にソートする
    
    Args:
        videos: ソート対象の動画リスト
        
    Returns:
        時間順にソートされた動画リスト
    """
    return sorted(videos, key=lambda video: video.duration)


def filter_videos_by_max_duration(videos: List[Video], max_duration: int) -> List[Video]:
    """
    指定された最大時間以下の動画をフィルタリングする
    
    Args:
        videos: フィルタリング対象の動画リスト
        max_duration: 最大時間（秒）
        
    Returns:
        最大時間以下の動画のリスト
    """
    return [video for video in videos if video.duration <= max_duration]


def select_videos(videos: List[Video], target_duration: int, min_remaining: int = 60) -> VideoCollection:
    """
    指定された時間に最適な動画の組み合わせを選択する
    
    Args:
        videos: 選択対象となる動画のリスト
        target_duration: 目標時間（秒）
        min_remaining: 許容される最小残り時間（秒）、デフォルトは60秒（1分）
        
    Returns:
        選択された動画のコレクション
    """
    # 動画を時間順にソート
    sorted_videos = sort_videos_by_duration(videos)
    
    # 選択された動画を格納するリスト
    selected_videos = []
    total_duration = 0
    remaining_duration = target_duration
    
    # 最初のビデオを候補から選ぶためのビデオコピー
    available_videos = sorted_videos.copy()
    
    # 残り時間が最小残り時間より大きい間、ビデオを選び続ける
    while remaining_duration > min_remaining and available_videos:
        # 残り時間以下の動画をフィルタリング
        filtered_videos = filter_videos_by_max_duration(available_videos, remaining_duration)
        
        # 条件を満たす動画がない場合は終了
        if not filtered_videos:
            break
            
        # ランダムに1つ選択
        selected_video = random.choice(filtered_videos)
        
        # 選択されたビデオを追加
        selected_videos.append(selected_video)
        total_duration += selected_video.duration
        remaining_duration = target_duration - total_duration
        
        # 選択されたビデオを利用可能なビデオから削除
        available_videos.remove(selected_video)
    
    return VideoCollection(
        videos=selected_videos,
        total_time=total_duration,
        remaining_time=remaining_duration
    )


def get_video_combinations(videos: List[Video], target_duration: int, 
                           attempts: int = 3) -> List[VideoCollection]:
    """
    指定された時間に合わせた動画の組み合わせを複数生成する
    
    Args:
        videos: 選択対象となる動画のリスト
        target_duration: 目標時間（秒）
        attempts: 生成する組み合わせの数、デフォルトは3
        
    Returns:
        動画コレクションのリスト
    """
    combinations = []
    
    for _ in range(attempts):
        # 動画の組み合わせを選択
        video_collection = select_videos(videos, target_duration)
        combinations.append(video_collection)
    
    # 残り時間が少ない順にソート
    combinations.sort(key=lambda collection: collection.remaining_time)
    
    return combinations
