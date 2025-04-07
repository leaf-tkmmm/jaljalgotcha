"""
リポジトリのインターフェース定義
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..models import Video


class VideoRepository(ABC):
    """動画リポジトリのインターフェース"""
    
    @abstractmethod
    def get_videos(self, filters: Optional[Dict[str, Any]] = None) -> List[Video]:
        """
        動画のリストを取得する
        
        Args:
            filters: フィルタリング条件（オプション）
            
        Returns:
            動画のリスト
        """
        pass
