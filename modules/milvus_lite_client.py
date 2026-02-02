import os

from pymilvus import MilvusClient


class MilvusClientProxy:
    """
    MilvusClient 的代理类，支持延迟初始化。
    这样可以先 import client 对象，等 main.py 解析完参数后再真正连接数据库。
    """

    def __init__(self):
        self._client = None

    def initialize(self, db_path: str):
        """
        初始化真正的 MilvusClient
        """
        # 确保目录存在
        if db_path:
            try:
                print(f"creating directory: {db_path}")
                os.makedirs(db_path, exist_ok=True)
            except OSError as e:
                print(f"❌ Failed to create directory: {db_path}")
                raise
        db_path = os.path.join(db_path, "data.db")
        print(f"💽 Initializing Milvus Database at: {os.path.abspath(db_path)}")
        self._client = MilvusClient(uri=db_path)

    def __getattr__(self, name):
        """
        将所有调用转发给真正的 _client 实例
        """
        if self._client is None:
            raise RuntimeError("MilvusClient has not been initialized! Call client.initialize(path) first.")
        return getattr(self._client, name)


# 创建一个全局代理对象
# 其他文件 import client 时，拿到的是这个代理
client = MilvusClientProxy()
