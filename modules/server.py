from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup event
    print(f"✅ Milvus Lite API started")
    yield


app = FastAPI(title="Milvus REST API Wrapper", lifespan=lifespan)
# 注册路由

from api.milvus_api import router as milvus_router
from api.health_api import router as health_router

app.include_router(milvus_router)
app.include_router(health_router)
