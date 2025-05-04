"""
動画処理のサービス層実装
"""
import random
from typing import List, Dict, Any, Optional

from ..models import Video, VideoCollection
from ..repositories.interfaces import VideoRepository


class VideoService:
    """動画処理のサービスクラス"""
    
    def __init__(self, video_repository: VideoRepository):
        """
        初期化
        
        Args:
            video_repository: 動画リポジトリのインスタンス
        """
        self.video_repository = video_repository

    def _convert_filters(self, filters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        フィルターをYouTube API形式からDB形式に変換する

        Args:
            filters: 元のフィルター条件

        Returns:
            変換後のフィルター条件
        """
        if not filters:
            return {}

        converted_filters = {}

        # YouTube APIのフィルターをDB用に変換
        if 'max_results' in filters:
            converted_filters['limit'] = filters['max_results']
        if 'order' in filters:
            converted_filters['order_by'] = filters['order']
            converted_filters['order_dir'] = 'desc' if filters['order'] == 'date' else 'asc'

        # DB固有のフィルターを追加
        if 'max_duration' in filters:
            converted_filters['max_duration'] = filters['max_duration']
        if 'min_likes' in filters:
            converted_filters['min_likes'] = filters['min_likes']
        if 'min_views' in filters:
            converted_filters['min_views'] = filters['min_views']

        return converted_filters
    
    def get_video_combinations(self, target_duration: int, 
                              attempts: int = 3,
                              filters: Optional[Dict[str, Any]] = None) -> List[VideoCollection]:
        """
        指定された時間に合わせた動画の組み合わせを複数生成する
        
        Args:
            target_duration: 目標時間（秒）
            attempts: 生成する組み合わせの数、デフォルトは3
            filters: 動画のフィルタリング条件（オプション）
            
        Returns:
            動画コレクションのリスト
        """
        # フィルターを変換
        filters = self._convert_filters(filters)

        # リポジトリから動画を取得
        videos = self.video_repository.get_videos(filters)
        print(f"取得した動画の数: {len(videos)}")
        combinations = []
        
        for _ in range(attempts):
            # 動画の組み合わせを選択
            video_collection = self._select_videos(videos, target_duration)
            combinations.append(video_collection)
        
        # 残り時間が少ない順にソート
        combinations.sort(key=lambda collection: collection.remaining_time)
        
        return combinations
    
    def _sort_videos_by_duration(self, videos: List[Video]) -> List[Video]:
        """
        動画を時間順にソートする
        
        Args:
            videos: ソート対象の動画リスト
            
        Returns:
            時間順にソートされた動画リスト
        """
        return sorted(videos, key=lambda video: video.duration)
    
    def _filter_videos_by_max_duration(self, videos: List[Video], max_duration: int) -> List[Video]:
        """
        指定された最大時間以下の動画をフィルタリングする
        
        Args:
            videos: フィルタリング対象の動画リスト
            max_duration: 最大時間（秒）
            
        Returns:
            最大時間以下の動画のリスト
        """
        return [video for video in videos if video.duration <= max_duration]
    
    def _select_videos(self, videos: List[Video], target_duration: int, min_remaining: int = 60) -> VideoCollection:
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
        sorted_videos = self._sort_videos_by_duration(videos)
        
        # 選択された動画を格納するリスト
        selected_videos = []
        total_duration = 0
        remaining_duration = target_duration
        
        # 最初のビデオを候補から選ぶためのビデオコピー
        available_videos = sorted_videos.copy()
        
        # 残り時間が最小残り時間より大きい間、ビデオを選び続ける
        while remaining_duration > min_remaining and available_videos:
            # 残り時間以下の動画をフィルタリング
            filtered_videos = self._filter_videos_by_max_duration(available_videos, remaining_duration)
            
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
