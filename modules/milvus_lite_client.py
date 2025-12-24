import os
from pymilvus import MilvusClient

# 确保数据库目录存在
db_dir = "./db"
os.makedirs(db_dir, exist_ok=True)

# 初始化 Milvus 客户端
client = MilvusClient(os.path.join(db_dir, "milvus_lite.db"))
