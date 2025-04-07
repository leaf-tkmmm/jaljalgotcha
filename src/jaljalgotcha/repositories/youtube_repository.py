"""
YouTube API を使用した動画リポジトリ実装
"""
import re
import logging
from typing import List, Optional, Dict, Any, Tuple
import random

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models import Video
from .interfaces import VideoRepository
from ..config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID

# ロガーの設定
logger = logging.getLogger(__name__)


class YouTubeVideoRepository(VideoRepository):
    """YouTube API を使用した動画リポジトリの実装"""
    
    def __init__(self, api_key: str = None):
        """
        初期化
        
        Args:
            api_key: YouTube Data API のキー（未指定の場合は環境変数から取得）
        """
        self.api_key = api_key or YOUTUBE_API_KEY
        if not self.api_key:
            logger.warning("YouTube API キーが設定されていません。")
        
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
            return self._get_dummy_videos()
        
        try:
            # フィルター設定
            filters = filters or {}
            channel_id = filters.get('channel_id', YOUTUBE_CHANNEL_ID)
            max_results = min(int(filters.get('max_results', 50)), 50)  # YouTube APIの上限は50
            order = filters.get('order', 'date') # デフォルトを新しい順に変更
            
            if not channel_id:
                logger.error("YouTube チャンネルIDが設定されていません。")
                return self._get_dummy_videos()

            # 検索リクエスト (チャンネルIDで検索)
            search_response = self.youtube_client.search().list(
                channelId=channel_id,
                part='id', # snippetは不要なのでidのみ取得
                maxResults=max_results,
                type='video',
                order=order
            ).execute()
            
            # 動画IDのリストを取得
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                logger.warning(f"チャンネルID '{channel_id}' に動画が見つかりませんでした。")
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
            return self._get_dummy_videos()
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return self._get_dummy_videos()
    
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
    
    def _get_dummy_videos(self) -> List[Video]:
        """
        テスト用のダミー動画データを生成する（API接続に失敗した場合のフォールバック）
        
        Returns:
            ダミー動画のリスト
        """
        video_titles = [
            "JalJal公式: 面白い瞬間集",
            "JalJal: ベストプレイ集2024",
            "JalJal: ゲーム実況Part1",
            "JalJal: ゲーム実況Part2",
            "JalJalメンバー: 爆笑トーク",
            "JalJal: 実況プレイ特集",
            "JalJal公式: 人気シーン集",
            "JalJal: 最新ゲームレビュー",
            "JalJalチャレンジ集",
            "JalJal: 視聴者質問コーナー"
        ]
        
        videos = []
        for i, title in enumerate(video_titles, 1):
            # ランダムな時間（1分～10分）
            duration = random.randint(60, 600)
            video_id = f"yt{i:03d}"
            videos.append(Video(
                id=video_id,
                title=title,
                duration=duration,
                url=f"https://www.youtube.com/watch?v={video_id}"
            ))
        
        return videos
