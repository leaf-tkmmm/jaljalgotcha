# YouTube データベース連携

このプロジェクトでは、YouTube API を使用して動画情報を取得し、PostgreSQL データベースに保存します。
保存したデータを元に、指定した時間内に収まる動画の組み合わせを提供します。

このプロジェクトは以下の機能を提供します：

1. YouTube API からデータを取得してデータベースに保存
2. データベースから動画情報を取得して表示
3. 指定した時間内に収まる動画の組み合わせを選択
4. Web API を通じてデータベースの動画情報を提供

## 前提条件

- Python 3.8 以上
- PostgreSQL データベース（Docker で実行）
- YouTube API キー

## セットアップ

1. 必要なパッケージをインストールします：

```bash
pip install -r requirements_minimal.txt
```

2. Docker で PostgreSQL を起動します：

```bash
cd server
docker-compose up -d
```

3. YouTube API から動画データを取得してデータベースに保存します：

```bash
cd server
python -m src.jaljalgotcha.scripts.fetch_youtube_data
```

## 使用方法

### データベースの内容を確認する

```bash
cd server
python -m src.jaljalgotcha.scripts.check_db
```

### 指定した時間内に収まる動画を選択する

```bash
cd server
python -m src.jaljalgotcha.scripts.select_videos <目標時間（分）> [最小いいね数] [最小再生数]
```

例：

- 10 分以内の動画を選択する：

  ```bash
  python -m src.jaljalgotcha.scripts.select_videos 10
  ```

- 15 分以内で、いいね数が 1500 以上の動画を選択する：

  ```bash
  python -m src.jaljalgotcha.scripts.select_videos 15 1500
  ```

- 20 分以内で、いいね数が 1000 以上、再生数が 50000 以上の動画を選択する：
  ```bash
  python -m src.jaljalgotcha.scripts.select_videos 20 1000 50000
  ```

### Web API を使用する

1. Flask サーバーを起動する：

```bash
cd server
python -m src.jaljalgotcha.main
```

2. API をテストする：

```bash
cd server
python -m src.jaljalgotcha.scripts.test_api_with_db <目標時間（分）> [組み合わせ数]
```

例：

- 10 分以内の動画を 3 つの組み合わせで取得する：
  ```bash
  python -m src.jaljalgotcha.scripts.test_api_with_db 10 3
  ```

### API エンドポイント

- `GET /api/combinations` - 指定された時間に合う動画の組み合わせを取得する
  - クエリパラメータ：
    - `duration` (必須): 希望する動画時間（分単位または HH:MM:SS 形式）
    - `attempts` (オプション): 生成する組み合わせの数、デフォルトは 3
    - `use_youtube` (オプション): YouTube の API を使用するかどうか、デフォルトは false
    - `use_database` (オプション): データベースを使用するかどうか、デフォルトは false

## ファイル構成

- `src/jaljalgotcha/db/models.py`: SQLAlchemy データベースモデル
- `src/jaljalgotcha/db/database.py`: データベース接続ユーティリティ
- `src/jaljalgotcha/repositories/video_repository.py`: データベースリポジトリ実装
- `src/jaljalgotcha/scripts/fetch_youtube_data.py`: YouTube API からデータを取得するスクリプト
- `src/jaljalgotcha/scripts/check_db.py`: データベースの内容を確認するスクリプト
- `src/jaljalgotcha/scripts/select_videos.py`: 指定した時間内に収まる動画を選択するスクリプト
- `src/jaljalgotcha/scripts/test_api_with_db.py`: データベースリポジトリを使用した API のテスト
- `src/jaljalgotcha/db_integration.py`: データベースリポジトリと API の統合
- `src/jaljalgotcha/main.py`: Flask Web API のエントリーポイント

## 実装の詳細

### データベースモデル

`VideoModel` クラスは、`videos` テーブルのスキーマを表現しています：

```python
class VideoModel(Base):
    __tablename__ = 'videos'

    video_id = Column(String, primary_key=True)
    channel_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    view_count = Column(BigInteger, default=0)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    thumbnail_url = Column(String)
    published_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.now)
```

### 動画選択アルゴリズム

1. 指定された時間内に収まる動画をデータベースから取得します
2. フィルタリング条件（いいね数、再生数など）を適用します
3. 残り時間が 1 分以上ある間、以下を繰り返します：
   - 残り時間以下の動画をフィルタリングします
   - ランダムに 1 つの動画を選択します
   - 選択した動画を結果リストに追加します
   - 残り時間を更新します

## 注意事項

- YouTube API には 1 日あたりのクォータ制限があります。大量のデータを取得する場合は注意してください。
- データベースの初期化は `init.sql` スクリプトによって行われます。
