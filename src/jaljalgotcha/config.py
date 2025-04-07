"""
アプリケーション設定
環境変数からの設定読み込み
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトのルートディレクトリを取得
# 現在のファイルの場所から2階層上がプロジェクトルート
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# .envファイルの読み込み
load_dotenv(ROOT_DIR / '.env')

# YouTube API 設定
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
# YOUTUBE_SEARCH_QUERY = os.getenv('YOUTUBE_SEARCH_QUERY', 'JalJal') # チャンネル検索に変更したため不要

# アプリケーション設定
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
