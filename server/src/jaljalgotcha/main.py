"""
アプリケーションのエントリーポイント
Flaskを使用したWeb APIの提供
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

from .utils import parse_duration, video_collection_to_dict
from .repositories.memory_repository import MemoryVideoRepository
from .repositories.youtube_repository import YouTubeVideoRepository
from .services.video_service import VideoService
from .di.container import container
from .db_integration import get_db_video_service

# サービス設定
def setup_services(use_youtube_api: bool = False, use_database: bool = False):
    """
    アプリケーションサービスの設定
    
    Args:
        use_youtube_api: YouTubeのAPIを使用するかどうか
        use_database: データベースを使用するかどうか
    """
    if use_database:
        # データベースリポジトリを使用
        # 既に登録済みの場合は何もしない
        return get_db_video_service()
    elif use_youtube_api:
        # YouTubeリポジトリを使用
        # API_KEYは環境変数から自動的に取得
        container.register('video_repository', lambda c: YouTubeVideoRepository())
    else:
        # メモリベースのリポジトリを使用
        container.register('video_repository', lambda c: MemoryVideoRepository())
    
    # ビデオサービスを登録
    container.register('video_service', lambda c: VideoService(c.get('video_repository')))

# デフォルトでメモリベースのリポジトリを使用
setup_services(use_youtube_api=False, use_database=False)

# Flaskアプリケーションの初期化
app = Flask(__name__)
CORS(app)  # すべてのルートでCORS対応を有効化


@app.route('/api/combinations')
def get_combinations():
    """
    指定された時間に合う動画の組み合わせを取得するAPI
    
    Query Parameters:
        duration (str): 希望する動画時間（分単位または HH:MM:SS形式）
        attempts (int, optional): 生成する組み合わせの数、デフォルトは3
        use_youtube (bool, optional): YouTubeのAPIを使用するかどうか、デフォルトはFalse
        use_database (bool, optional): データベースを使用するかどうか、デフォルトはFalse
    
    Returns:
        JSON: 動画の組み合わせリスト
    """
    # リクエストパラメータを取得
    duration_str = request.args.get('duration', '')
    attempts = int(request.args.get('attempts', 3))
    use_youtube = request.args.get('use_youtube', 'false').lower() == 'true'
    use_database = request.args.get('use_database', 'false').lower() == 'true'
    
    # パラメータのバリデーション
    if not duration_str:
        return jsonify({"error": "時間を指定してください"}), 400
    
    try:
        # 時間を秒単位に変換
        if ':' in duration_str:
            target_duration = parse_duration(duration_str)
        else:
            # 分単位として扱う
            target_duration = int(duration_str) * 60
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # リポジトリを設定 (YouTube、メモリ、データベースを切り替え)
    video_service = setup_services(use_youtube_api=use_youtube, use_database=use_database)
    
    # ビデオサービスが返されなかった場合はコンテナから取得
    if not video_service:
        video_service = container.get('video_service')
    
    # 動画の組み合わせを取得
    try:
        combinations = video_service.get_video_combinations(target_duration, attempts)
        
        # 結果が空でYouTube APIを使用している場合は、API設定が正しくない可能性がある
        if not combinations and use_youtube:
            from .config import YOUTUBE_API_KEY
            if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
                return jsonify({
                    "error": "YouTube API キーが設定されていません。.envファイルで'YOUTUBE_API_KEY'を設定してください。",
                    "hint": "YouTubeデータAPIキーを取得して.envファイルに設定する必要があります。"
                }), 500
    except Exception as e:
        return jsonify({"error": f"エラーが発生しました：{str(e)}"}), 500
    
    # 結果をJSONに変換
    result = [video_collection_to_dict(combo) for combo in combinations]
    
    return jsonify(result)


if __name__ == '__main__':
    """
    開発サーバーとして実行
    """
    app.run(debug=True)
