"""
ユーティリティ関数
"""
from datetime import timedelta
from typing import Dict, Any

from .models import Video, VideoCollection


def format_duration(seconds: int) -> str:
    """
    秒数をHH:MM:SS形式にフォーマットする
    
    Args:
        seconds: フォーマットする秒数
        
    Returns:
        フォーマットされた時間文字列
    """
    return str(timedelta(seconds=seconds))


def parse_duration(duration_str: str) -> int:
    """
    'HH:MM:SS'または'MM:SS'形式の文字列を秒数に変換する
    
    Args:
        duration_str: 変換する時間文字列
    
    Returns:
        秒数
    """
    parts = duration_str.split(':')
    
    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    else:
        try:
            # 単位が秒の場合
            return int(duration_str)
        except ValueError:
            raise ValueError(f"Invalid duration format: {duration_str}")


def video_collection_to_dict(collection: VideoCollection) -> Dict[str, Any]:
    """
    VideoCollectionオブジェクトを辞書形式に変換する
    
    Args:
        collection: 変換するVideoCollectionオブジェクト
        
    Returns:
        辞書形式のデータ
    """
    return {
        "videos": [video_to_dict(video) for video in collection.videos],
        "total_time": collection.total_time,
        "total_time_formatted": format_duration(collection.total_time),
        "remaining_time": collection.remaining_time,
        "remaining_time_formatted": format_duration(collection.remaining_time)
    }


def video_to_dict(video: Video) -> Dict[str, Any]:
    """
    Videoオブジェクトを辞書形式に変換する
    
    Args:
        video: 変換するVideoオブジェクト
        
    Returns:
        辞書形式のデータ
    """
    return {
        "id": video.id,
        "title": video.title,
        "duration": video.duration,
        "duration_formatted": format_duration(video.duration),
        "url": video.url
    }
