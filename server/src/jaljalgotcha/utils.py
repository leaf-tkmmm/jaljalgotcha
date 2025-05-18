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
    分単位の文字列を秒数に変換する
    最大1000分（60000秒）まで許容
    
    Args:
        duration_str: 変換する時間文字列（分単位）
    
    Returns:
        秒数
    
    Raises:
        ValueError: 無効な形式または最大値を超える場合
    """
    try:
        minutes = int(duration_str)
        
        # 正の値であることを確認
        if minutes <= 0:
            raise ValueError("時間は正の値である必要があります")
            
        # 最大1000分の制限を追加
        if minutes > 1000:
            raise ValueError("時間は最大1000分までです")
            
        # 秒に変換
        return minutes * 60
        
    except ValueError as e:
        if str(e).startswith("時間は"):
            raise e
        raise ValueError(f"有効な数値を入力してください: {duration_str}")


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
    result = {
        "id": video.id,
        "title": video.title,
        "duration": video.duration,
        "duration_formatted": format_duration(video.duration),
        "url": video.url
    }
    
    # thumbnail_urlがNoneでない場合は追加
    if video.thumbnail_url is not None:
        result["thumbnail_url"] = video.thumbnail_url
        
    return result
