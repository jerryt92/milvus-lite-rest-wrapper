from contextlib import asynccontextmanager
from typing import List, Optional, AsyncGenerator

from fastapi import FastAPI
from pydantic import BaseModel

from modules.milvus_lite_client import client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup event
    print(f"✅ Milvus Lite API started")
    yield


app = FastAPI(title="Milvus REST API Wrapper", lifespan=lifespan)


# --- Pydantic 模型 (用于请求体验证) ---
class CreateCollectionRequest(BaseModel):
    collection_name: str
    dimension: int
    description: Optional[str] = "Created via REST API"


class InsertDataRequest(BaseModel):
    collection_name: str
    vectors: List[List[float]]  # 二维数组: [ [0.1, 0.2...], [0.3, 0.4...] ]


class SearchRequest(BaseModel):
    collection_name: str
    query_vectors: List[List[float]]
    top_k: int = 5
    nprobe: int = 10


@app.get("/collections")
async def show_collections():
    """
    获取所有集合
    """
    print(f"GET /collections")
    return client.list_collections()
