from modules.milvus_lite_client import client
from modules.server import app

@app.get("/v1/rest/test/collections/create")
async def create_collection():
    """
    创建集合
    """
    print(f"GET /v1/rest/test/collections/create")
    return client.create_collection(
        collection_name="test_collection",
        dimension=128,
        description="Created via REST API"
    )


@app.get("/v1/rest/test/collections/drop")
async def drop_collection():
    """
    创建集合
    """
    print(f"GET /v1/rest/test/collections/drop")
    return client.create_collection(
        collection_name="test_collection",
        dimension=128,
        description="Created via REST API"
    )
