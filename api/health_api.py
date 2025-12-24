from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/v1/rest/check-health")
async def check_health():
    """Handle GET request for /v1/rest/check-health"""
    # TODO: 实现业务逻辑
    return {"status": "ok"}
