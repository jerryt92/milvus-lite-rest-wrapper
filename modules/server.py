from contextlib import asynccontextmanager
from typing import List, Optional, AsyncGenerator

from fastapi import FastAPI
from pydantic import BaseModel

from modules.milvus_lite_client import client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup event
    print(f"✅ Milvus Lite API started")
    # 在应用启动时导入 API 模块，避免循环导入
    import api  # noqa: F401 - 导入用于注册路由
    yield


app = FastAPI(title="Milvus REST API Wrapper", lifespan=lifespan)

@app.get("/collections")
async def show_collections():
    """
    获取所有集合
    """
    print(f"GET /collections")
    return client.list_collections()
