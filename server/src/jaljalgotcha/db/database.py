"""
データベース接続ユーティリティ (SQLite バージョン)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# SQLite用のファイルパス
SQLITE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "sqlite.db")

# SQLAlchemy エンジン作成 (SQLite使用)
DATABASE_URL = f"sqlite:///{SQLITE_FILE_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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
