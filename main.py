import argparse
import os
import sys

import uvicorn

# 引入我们在上面定义的代理对象
from modules.milvus_lite_client import client
from modules.server import app


def get_default_db_path():
    """
    获取默认数据库路径：
    1. 打包环境 (Frozen): 在二进制文件同级目录下
    2. 开发环境: 在当前脚本同级目录下
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的可执行文件路径
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境下的 main.py 所在路径
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # 默认放在同级目录的 milvus_data 文件夹下
    return os.path.join(base_dir, "milvus_data")


if __name__ == "__main__":
    # 1. 计算默认路径
    default_db_path = get_default_db_path()

    # 2. 定义命令行参数解析
    parser = argparse.ArgumentParser(description="Milvus Lite Service")
    parser.add_argument("--port", type=int, default=29530, help="Service port")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Service host")
    parser.add_argument(
        "--data-path",
        type=str,
        default=default_db_path,
        help=f"Path to Milvus Lite database file. Default: {default_db_path}"
    )

    args = parser.parse_args()

    # 3. 【核心步骤】初始化数据库
    # 这会激活 modules.milvus_lite_client 中的 client 对象
    try:
        client.initialize(args.data_path)
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

    # 检测调试模式
    is_debug = "pydevd" in sys.modules or "PYCHARM_HOSTED" in os.environ

    print(f"🚀 Starting Milvus Service on {args.host}:{args.port}")

    if is_debug:
        print("🔧 Debug mode detected")
        config = uvicorn.Config(app, host="127.0.0.1", port=args.port, reload=False)
        server = uvicorn.Server(config)
        import asyncio

        asyncio.run(server.serve())
    else:
        uvicorn.run(app, host=args.host, port=args.port, reload=False)
