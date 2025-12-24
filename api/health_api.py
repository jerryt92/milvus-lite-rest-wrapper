from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def check_health():
    # TODO: 实现业务逻辑
    return {"status": "ok"}
