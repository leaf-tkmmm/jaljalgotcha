"""
アプリケーションのエントリーポイント
Flaskを使用したWeb APIの提供
"""
from flask import Flask, request, jsonify, render_template_string

from .models import Video
from .utils import parse_duration, video_collection_to_dict
from .repositories.memory_repository import MemoryVideoRepository
from .repositories.youtube_repository import YouTubeVideoRepository
from .services.video_service import VideoService
from .di.container import container

# サービス設定
def setup_services(use_youtube_api: bool = False):
    """
    アプリケーションサービスの設定
    
    Args:
        use_youtube_api: YouTubeのAPIを使用するかどうか
    """
    if use_youtube_api:
        # YouTubeリポジトリを使用
        # API_KEYは環境変数から自動的に取得
        container.register('video_repository', lambda c: YouTubeVideoRepository())
    else:
        # メモリベースのリポジトリを使用
        container.register('video_repository', lambda c: MemoryVideoRepository())
    
    # ビデオサービスを登録
    container.register('video_service', lambda c: VideoService(c.get('video_repository')))

# デフォルトでメモリベースのリポジトリを使用
setup_services(use_youtube_api=False)

# Flaskアプリケーションの初期化
app = Flask(__name__)


@app.route('/')
def index():
    """
    インデックスページを表示
    """
    # シンプルなHTMLページをテンプレート文字列として提供
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>JalJalGotcha</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input[type="text"] {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                border-top: 1px solid #ddd;
                padding-top: 20px;
            }
            .video-list {
                list-style-type: none;
                padding: 0;
            }
            .video-item {
                background-color: #f9f9f9;
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 4px;
            }
            .summary {
                margin-top: 15px;
                padding: 10px;
                background-color: #e9e9e9;
            }
        </style>
    </head>
    <body>
        <h1>JalJalGotcha - 動画の時間組み合わせシステム</h1>
        
        <div class="form-group">
            <label for="duration">希望する時間（分単位または HH:MM:SS形式）:</label>
            <input type="text" id="duration" name="duration" placeholder="例: 30 または 00:30:00">
        </div>
        
        <div class="form-group">
            <label for="combinations">生成する組み合わせの数:</label>
            <input type="text" id="combinations" name="combinations" value="3">
        </div>
        
        <div class="form-group">
            <label>データソース:</label>
            <div>
                <input type="radio" id="use_memory" name="data_source" value="memory" checked>
                <label for="use_memory">メモリ内サンプルデータ</label>
            </div>
            <div>
                <input type="radio" id="use_youtube" name="data_source" value="youtube">
                <label for="use_youtube">YouTube API</label>
            </div>
        </div>
        
        <button onclick="getVideoCombinations()">動画組み合わせを取得</button>
        
        <div id="result"></div>
        
        <script>
            function getVideoCombinations() {
                const duration = document.getElementById('duration').value;
                const combinations = document.getElementById('combinations').value;
                
                if (!duration) {
                    alert('時間を入力してください');
                    return;
                }
                
                // データソースの選択を取得
                const dataSource = document.querySelector('input[name="data_source"]:checked').value;
                const useYoutube = dataSource === 'youtube';
                
                // APIリクエスト
                fetch(`/api/combinations?duration=${duration}&attempts=${combinations}&use_youtube=${useYoutube}`)
                    .then(response => response.json())
                    .then(data => {
                        const resultDiv = document.getElementById('result');
                        resultDiv.innerHTML = '';
                        
                        if (data.length === 0) {
                            resultDiv.innerHTML = '<p>条件に合う組み合わせが見つかりませんでした。</p>';
                            return;
                        }
                        
                        // 各組み合わせを表示
                        data.forEach((combo, index) => {
                            const comboDiv = document.createElement('div');
                            comboDiv.innerHTML = `<h3>組み合わせ ${index + 1}</h3>`;
                            
                            const videoList = document.createElement('ul');
                            videoList.className = 'video-list';
                            
                            combo.videos.forEach(video => {
                                const videoItem = document.createElement('li');
                                videoItem.className = 'video-item';
                                videoItem.innerHTML = `
                                    <strong>${video.title}</strong>
                                    <div>時間: ${video.duration_formatted}</div>
                                `;
                                videoList.appendChild(videoItem);
                            });
                            
                            comboDiv.appendChild(videoList);
                            
                            const summary = document.createElement('div');
                            summary.className = 'summary';
                            summary.innerHTML = `
                                <div>合計時間: ${combo.total_time_formatted}</div>
                                <div>残り時間: ${combo.remaining_time_formatted}</div>
                            `;
                            
                            comboDiv.appendChild(summary);
                            resultDiv.appendChild(comboDiv);
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('result').innerHTML = 
                            `<p>エラーが発生しました: ${error.message}</p>`;
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/api/combinations')
def get_combinations():
    """
    指定された時間に合う動画の組み合わせを取得するAPI
    
    Query Parameters:
        duration (str): 希望する動画時間（分単位または HH:MM:SS形式）
        attempts (int, optional): 生成する組み合わせの数、デフォルトは3
        use_youtube (bool, optional): YouTubeのAPIを使用するかどうか、デフォルトはFalse
    
    Returns:
        JSON: 動画の組み合わせリスト
    """
    # リクエストパラメータを取得
    duration_str = request.args.get('duration', '')
    attempts = int(request.args.get('attempts', 3))
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
    
    # リポジトリを設定 (YouTubeかメモリかを切り替え)
    setup_services(use_youtube_api=use_youtube)
    
    # ビデオサービスを取得
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
