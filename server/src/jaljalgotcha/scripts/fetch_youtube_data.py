#!/usr/bin/env python
"""
YouTube APIからデータを取得してデータベースに保存するスクリプト
"""
import os
import sys
import logging
import re
import isodate
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.jaljalgotcha.db.database import init_db, db_session
from src.jaljalgotcha.db.models_db import VideoModel
from src.jaljalgotcha.repositories.db_repository import DbVideoRepository
from src.jaljalgotcha.config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_iso8601_duration(duration_str: str) -> int:
    """
    ISO 8601形式の動画時間（PT1H30M15S）を秒に変換する
    
    Args:
        duration_str: ISO 8601形式の時間文字列
        
    Returns:
        秒数
    """
    return int(isodate.parse_duration(duration_str).total_seconds())


def fetch_videos_from_youtube(api_key: str, channel_id: str) -> list:
    """
    YouTube APIから動画情報を取得する
    
    Args:
        api_key: YouTube API キー
        channel_id: YouTube チャンネルID
        
    Returns:
        動画情報のリスト
    """
    if not api_key:
        raise ValueError("YouTube API キーが設定されていません。")
    
    if not channel_id:
        raise ValueError("YouTube チャンネルIDが設定されていません。")
    
    try:
        # YouTube APIクライアントの初期化
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # まずチャンネル情報を取得して、アップロードプレイリストIDを取得
        channel_response = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()
        
        if not channel_response.get('items'):
            logger.warning(f"チャンネルID '{channel_id}' が見つかりませんでした。")
            return []
        
        # アップロードプレイリストIDを取得（すべての動画を含む特別なプレイリスト）
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        logger.info(f"チャンネルのアップロードプレイリストID: {uploads_playlist_id}")
        
        # プレイリストから全ての動画を取得
        all_video_ids = []
        next_page_token = None
        page_count = 0
        
        while True:
            # プレイリストアイテムを取得（ページングあり）
            playlist_response = youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='snippet',
                maxResults=50,  # APIの最大値
                pageToken=next_page_token
            ).execute()
            
            # 動画IDをリストに追加
            video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response.get('items', [])]
            all_video_ids.extend(video_ids)
            
            # ページ数をカウント
            page_count += 1
            logger.info(f"プレイリストページ {page_count}: {len(video_ids)}件の動画IDを取得しました（合計: {len(all_video_ids)}件）")
            
            # 次のページがあるか確認
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                logger.info(f"全ての動画IDを取得しました（合計: {len(all_video_ids)}件）")
                break
        
        # 動画IDのリストを取得
        video_ids = all_video_ids
        
        if not video_ids:
            logger.warning(f"チャンネルID '{channel_id}' に動画が見つかりませんでした。")
            return []
        
        # 動画の詳細情報を取得（50件ずつに分割して取得）
        all_videos = []
        # YouTubeのAPIは一度に最大50件のIDしか処理できないため、50件ずつに分割
        chunk_size = 50
        for i in range(0, len(video_ids), chunk_size):
            chunk = video_ids[i:i + chunk_size]
            videos_response = youtube.videos().list(
                id=','.join(chunk),
                part='snippet,contentDetails,statistics'
            ).execute()
            all_videos.extend(videos_response.get('items', []))
        
        return all_videos
        
    except HttpError as e:
        logger.error(f"YouTube API エラー: {e}")
        raise
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        raise


def convert_to_video_model(youtube_video: dict) -> VideoModel:
    """
    YouTube APIのレスポンスからVideoModelオブジェクトを作成する
    
    Args:
        youtube_video: YouTube APIのレスポンス
        
    Returns:
        VideoModelオブジェクト
    """
    video_id = youtube_video['id']
    channel_id = youtube_video['snippet']['channelId']
    title = youtube_video['snippet']['title']
    
    # 動画時間の変換
    duration_str = youtube_video['contentDetails']['duration']
    duration_seconds = parse_iso8601_duration(duration_str)
    
    # 統計情報の取得
    statistics = youtube_video.get('statistics', {})
    view_count = int(statistics.get('viewCount', 0))
    like_count = int(statistics.get('likeCount', 0))
    comment_count = int(statistics.get('commentCount', 0))
    
    # サムネイル画像URL
    thumbnail_url = youtube_video['snippet']['thumbnails']['default']['url']
    
    # 公開日時
    published_at_str = youtube_video['snippet']['publishedAt']
    published_at = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
    
    # VideoModelオブジェクトの作成
    return VideoModel(
        video_id=video_id,
        channel_id=channel_id,
        title=title,
        duration_seconds=duration_seconds,
        view_count=view_count,
        like_count=like_count,
        comment_count=comment_count,
        thumbnail_url=thumbnail_url,
        published_at=published_at,
        updated_at=datetime.now()
    )


def main():
    """メイン処理"""
    try:
        # データベースの初期化
        init_db()
        logger.info("データベースの初期化が完了しました。")
        
        # YouTube APIからデータを取得
        api_key = YOUTUBE_API_KEY
        channel_id = YOUTUBE_CHANNEL_ID
        if api_key is None or channel_id is None:
            raise Exception("APIキーが空です。")
        
        logger.info(f"YouTube APIからチャンネル '{channel_id}' の動画データを取得します...")
        youtube_videos = fetch_videos_from_youtube(api_key, channel_id)
        logger.info(f"{len(youtube_videos)}件の動画データを取得しました。")
        
        # VideoModelオブジェクトに変換
        video_models = [convert_to_video_model(video) for video in youtube_videos]
        
        # データベースに保存
        repo = DbVideoRepository(db_session)
        saved_videos = repo.save_videos(video_models)
        
        logger.info(f"{len(saved_videos)}件の動画データをデータベースに保存しました。")
        
        # 保存した動画の情報を表示
        for i, video in enumerate(saved_videos[:5], 1):  # 最初の5件のみ表示
            logger.info(f"{i}. {video.title} ({video.duration_seconds}秒)")
        
        if len(saved_videos) > 5:
            logger.info(f"...他 {len(saved_videos) - 5} 件")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        sys.exit(1)
    finally:
        # セッションをクローズ
        db_session.remove()


if __name__ == "__main__":
    main()
