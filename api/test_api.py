from fastapi import APIRouter

from modules.milvus_lite_client import client

router = APIRouter()


@router.get("/test/collections/create")
async def create_collection():
    """
    创建集合
    """
    print(f"GET /test/collections/create")
    return client.create_collection(
        collection_name="test_collection",
        dimension=128,
        description="Created via REST API"
    )


@router.get("/test/collections/drop")
async def drop_collection():
    """
    创建集合
    """
    print(f"GET /test/collections/drop")
    return client.create_collection(
        collection_name="test_collection",
        dimension=128,
        description="Created via REST API"
    )
