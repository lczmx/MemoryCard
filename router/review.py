"""
主页
"""
from fastapi import APIRouter

router = APIRouter(prefix="/review")


@router.get("/")
async def index():
    return {"index": "复习数据"}
