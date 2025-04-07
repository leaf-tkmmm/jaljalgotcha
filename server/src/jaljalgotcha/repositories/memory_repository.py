"""
メモリベースの動画リポジトリ実装
"""
from typing import List, Optional, Dict, Any

from ..models import Video
from .interfaces import VideoRepository


class MemoryVideoRepository(VideoRepository):
    """メモリ内データを使用した動画リポジトリの実装"""
    
    def __init__(self):
        """サンプル動画データを初期化"""
        self._videos = self._create_sample_videos()
    
    def get_videos(self, filters: Optional[Dict[str, Any]] = None) -> List[Video]:
        """
        動画のリストを取得する
        
        Args:
            filters: フィルタリング条件（オプション）
            
        Returns:
            動画のリスト
        """
        videos = self._videos
        
        # フィルタリング条件がある場合は適用
        if filters:
            # ここでフィルタリングロジックを実装
            # 例: フィルター条件に応じてビデオをフィルタリング
            pass
            
        return videos
    
    def _create_sample_videos(self) -> List[Video]:
        """
        テスト用のサンプル動画データを生成する
        
        Returns:
            サンプル動画のリスト
        """
        return [
            Video(id="001", title="サンプル動画1", duration=120),  # 2分
            Video(id="002", title="サンプル動画2", duration=180),  # 3分
            Video(id="003", title="サンプル動画3", duration=300),  # 5分
            Video(id="004", title="サンプル動画4", duration=240),  # 4分
            Video(id="005", title="サンプル動画5", duration=150),  # 2分30秒
            Video(id="006", title="サンプル動画6", duration=360),  # 6分
            Video(id="007", title="サンプル動画7", duration=420),  # 7分
            Video(id="008", title="サンプル動画8", duration=90),   # 1分30秒
            Video(id="009", title="サンプル動画9", duration=540),  # 9分
            Video(id="010", title="サンプル動画10", duration=600)  # 10分
        ]
