"""
获取卡片数据
"""
from fastapi import APIRouter

router = APIRouter(prefix="/cards")


@router.get("/")
async def index():
    return {"index": "cards"}
