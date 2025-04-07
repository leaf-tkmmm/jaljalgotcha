"""
データベース接続ユーティリティ
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# データベース接続情報
DB_USER = os.getenv('POSTGRES_USER', 'testuser')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'testpass')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'testdb')

# SQLAlchemy エンジン作成
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# セッションファクトリ作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# モデルのベースクラス
Base = declarative_base()
Base.query = db_session.query_property()


def get_db():
    """
    データベースセッションを取得する
    
    Yields:
        SQLAlchemy セッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    データベースの初期化
    テーブルが存在しない場合は作成する
    """
    # モデルをインポートしてテーブルを作成
    from .models_db import VideoModel  # noqa
    Base.metadata.create_all(bind=engine)
