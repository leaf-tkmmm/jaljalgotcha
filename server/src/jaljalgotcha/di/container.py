"""
依存性注入コンテナの実装
"""
from typing import Dict, Any, Optional, Type, TypeVar
from src.jaljalgotcha.repositories.video_repository import DbVideoRepository
from src.jaljalgotcha.db.database import db_session

T = TypeVar('T')


class Container:
    """
    シンプルな依存性注入コンテナ
    
    このコンテナはシングルトンとして機能し、アプリケーション全体で
    依存関係を一元管理します。
    """
    
    def __init__(self):
        """コンテナの初期化"""
        self._instances: Dict[str, Any] = {}
        self._factory_methods: Dict[str, Any] = {}
    
    def register(self, name: str, factory_method):
        """
        ファクトリメソッドを登録する
        
        Args:
            name: インスタンスの名前
            factory_method: インスタンスを生成するためのファクトリメソッド
        """
        self._factory_methods[name] = factory_method
    
    def get(self, name: str) -> Any:
        """
        登録されたインスタンスを取得する
        
        Args:
            name: インスタンスの名前
            
        Returns:
            登録されたインスタンス
            
        Raises:
            KeyError: 指定された名前のインスタンスが登録されていない場合
        """
        if name not in self._instances:
            if name not in self._factory_methods:
                raise KeyError(f"Unknown service: {name}")
            
            # ファクトリメソッドを使用してインスタンスを生成
            self._instances[name] = self._factory_methods[name](self)
        
        return self._instances[name]
    
    def get_instance_of(self, cls: Type[T]) -> Optional[T]:
        """
        指定されたクラスのインスタンスを探して返す
        
        Args:
            cls: インスタンスのクラス
            
        Returns:
            指定されたクラスのインスタンス（見つからない場合はNone）
        """
        for instance in self._instances.values():
            if isinstance(instance, cls):
                return instance
        return None


# グローバルインスタンス
container = Container()

# Register DbVideoRepository as the default VideoRepository
container.register('video_repository', lambda c: DbVideoRepository(db_session))
