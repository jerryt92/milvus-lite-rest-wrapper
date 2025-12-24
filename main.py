import argparse
import os
import sys

import uvicorn

from modules.server import app

if __name__ == "__main__":
    # 1. 定义命令行参数解析
    parser = argparse.ArgumentParser(description="Milvus Lite Service")
    parser.add_argument("--port", type=int, default=29530, help="Service port")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Service host")

    args = parser.parse_args()

    # 检测调试模式
    is_debug = "pydevd" in sys.modules or "PYCHARM_HOSTED" in os.environ

    print(f"🚀 Starting Milvus Service on {args.host}:{args.port}")

    if is_debug:
        print("🔧 Debug mode detected")
        # debug 模式下可以通过字符串引用来支持 reload，但在打包模式下必须传对象
        config = uvicorn.Config(app, host="127.0.0.1", port=args.port, reload=False)
        server = uvicorn.Server(config)
        import asyncio

        asyncio.run(server.serve())
    else:
        # 生产模式 (打包后走这里)
        uvicorn.run(app, host=args.host, port=args.port, reload=False)
