from flask import Flask, request, jsonify
from flask_cors import CORS
from requests import get
from sqlalchemy.orm import Session

from .utils import parse_duration, video_collection_to_dict
from .services.video_service import VideoService
from .di.container import container
from .db_integration import get_db_video_service, setup_video_repository
from .db.database import engine

# サービスの初期化と設定
video_service = get_db_video_service()
# Flaskアプリケーションの初期化
app = Flask(__name__)


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
    # コンテキストマネージャを使用して自動ロールバック
    with Session(engine) as session:
        # リクエストパラメータを取得
        duration_str = request.args.get('duration', '')
        
        # attempsパラメータを安全に取得・変換
        attempts_str = request.args.get('attempts', '3')
        try:
            # 数値部分のみを抽出して変換
            attempts = int(attempts_str.split('&')[0])
        except (ValueError, AttributeError):
            attempts = 3
            
        use_youtube = request.args.get('use_youtube', 'false').lower() == 'true'
        
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
        
        # ビデオサービスが返されなかった場合はコンテナから取得
        if not video_service:
            raise ValueError("ビデオサービスが取得できませんでした。DIコンテナの設定を確認してください。")
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
            # エラー発生時にセッションはロールバックされる（コンテキストマネージャのexit処理）
            return jsonify({"error": f"エラーが発生しました：{str(e)}"}), 500
        
        # 結果をJSONに変換
        result = [video_collection_to_dict(combo) for combo in combinations]
        
        # コンテキストマネージャを抜ける際に自動的にロールバックされる（明示的なcommitがないため）
        return jsonify(result)

CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run()
