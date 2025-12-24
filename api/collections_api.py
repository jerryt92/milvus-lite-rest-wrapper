import json

from fastapi import APIRouter

from modules.milvus_lite_client import client

router = APIRouter()

@router.get("/v1/rest/milvuls/collections")
async def list_collections():
    client.list_collections()
    return json.dumps(client.list_collections())
