"""
记忆分析页面
"""

from fastapi import APIRouter

router = APIRouter(prefix="/analyse")


@router.get("/")
async def index():
    return {"index": "analyse"}
