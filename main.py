import asyncio  # 记得导入 asyncio
import uvicorn
from modules.server import app
import sys
import os

if __name__ == "__main__":
    # 检测是否在调试模式下运行
    is_debug = "pydevd" in sys.modules or "PYCHARM_HOSTED" in os.environ
    if is_debug:
        print("🔧 Debug mode detected: Starting manually to bypass PyCharm/Python3.12 conflict...")
        # 1. 创建 Config 对象
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=29530,
            reload=False
        )
        # 2. 创建 Server 对象
        server = uvicorn.Server(config)
        # 3. 手动运行 Server，不传 loop_factory 参数
        asyncio.run(server.serve())
    else:
        # 生产/非调试模式继续使用标准启动方式
        uvicorn.run(app, reload=False)