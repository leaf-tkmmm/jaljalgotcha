"""
YouTube API を使用した動画リポジトリ実装
"""
import re
import logging
from typing import List, Optional, Dict, Any, Tuple

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models import Video
from .interfaces import VideoRepository
from ..config import YOUTUBE_API_KEY

# ロガーの設定
logger = logging.getLogger(__name__)


class YouTubeVideoRepository(VideoRepository):
    """YouTube API を使用した動画リポジトリの実装"""
    
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        if not self.api_key:
            logger.warning("YouTube API キーが設定されていません。")

        self.youtube_channel_id = "UCf-wG6PlxW7rpixx1tmODJw"
        
        # YouTube APIクライアントの初期化
        self.youtube_client = self._initialize_youtube_client() if self.api_key else None
    
    def get_videos(self, filters: Optional[Dict[str, Any]] = None) -> List[Video]:
        """
        YouTube APIから動画のリストを取得する
        
        Args:
            filters: フィルタリング条件（オプション）
                - channel_id: 検索対象のチャンネルID（未指定の場合は設定ファイルの値を使用）
                - max_results: 取得する動画の最大数（デフォルト: 50）
                - order: 並び順（デフォルト: 'date' - 新しい順）
                  'date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'
            
        Returns:
            動画のリスト
        """
        if not self.youtube_client:
            logger.warning("YouTube API クライアントが初期化されていません。ダミーデータを返します。")
            raise ValueError("YouTube API クライアントが初期化されていません。")
        
        try:
            # フィルター設定
            filters = filters or {}
            max_results = min(int(filters.get('max_results', 50)), 50)  # YouTube APIの上限は50
            order = filters.get('order', 'date') # デフォルトを新しい順に変更
            
            if not self.youtube_channel_id:
                logger.error("YouTube チャンネルIDが設定されていません。")
                raise ValueError("YouTube チャンネルIDが設定されていません。")

            # 検索リクエスト (チャンネルIDで検索)
            search_response = self.youtube_client.search().list(
                channelId=self.youtube_channel_id,
                part='id', # snippetは不要なのでidのみ取得
                maxResults=max_results,
                type='video',
                order=order
            ).execute()
            
            # 動画IDのリストを取得
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                logger.warning(f"チャンネルID '{self.youtube_channel_id}' に動画が見つかりませんでした。")
                return []
            
            # 動画の詳細情報を取得
            videos_response = self.youtube_client.videos().list(
                id=','.join(video_ids),
                part='snippet,contentDetails,statistics'
            ).execute()
            
            # 動画情報をVideo オブジェクトに変換
            videos = []
            for item in videos_response['items']:
                video_id = item['id']
                title = item['snippet']['title']
                # ISO 8601形式の動画時間をパース
                duration_str = item['contentDetails']['duration']
                duration = self._parse_iso8601_duration(duration_str)
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                videos.append(Video(
                    id=video_id,
                    title=title,
                    duration=duration,
                    url=url
                ))
            
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API エラー: {e}")
            raise ValueError("データの取得に失敗しました。YouTube APIのエラーが発生しました。")
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            raise ValueError("予期しないエラーが発生しました。")
    
    def _initialize_youtube_client(self):
        """
        YouTube API クライアントを初期化する
        
        Returns:
            YouTube API クライアント
        """
        try:
            return build('youtube', 'v3', developerKey=self.api_key)
        except Exception as e:
            logger.error(f"YouTube API クライアントの初期化エラー: {e}")
            return None
    
    def _parse_iso8601_duration(self, duration_str: str) -> int:
        """
        ISO 8601形式の動画時間（PT1H30M15S）を秒に変換する
        
        Args:
            duration_str: ISO 8601形式の時間文字列
            
        Returns:
            秒数
        """
        # 正規表現でパターンマッチ
        hours_match = re.search(r'(\d+)H', duration_str)
        minutes_match = re.search(r'(\d+)M', duration_str)
        seconds_match = re.search(r'(\d+)S', duration_str)
        
        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0
        
        # 合計時間（秒）を計算
        return hours * 3600 + minutes * 60 + seconds
    
