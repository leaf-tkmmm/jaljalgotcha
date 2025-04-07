"""
データモデルの定義
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Video:
    """動画データのモデル"""
    id: str  # 動画ID
    title: str  # タイトル
    duration: int  # 動画時間（秒）
    url: Optional[str] = None  # 動画URL（オプション）
    
    def duration_minutes(self) -> float:
        """動画時間を分単位で返す"""
        return self.duration / 60


@dataclass
class VideoCollection:
    """選択された動画のコレクション"""
    videos: List[Video]
    total_time: int  # 合計時間（秒）
    remaining_time: int  # 残り時間（秒）
    
    def total_duration_minutes(self) -> float:
        """合計動画時間を分単位で返す"""
        return self.total_time / 60
    
    def remaining_duration_minutes(self) -> float:
        """残り時間を分単位で返す"""
        return self.remaining_time / 60
