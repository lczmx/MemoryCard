"""
记忆分析页面
"""

from fastapi import APIRouter

router = APIRouter(prefix="/analyse", tags=["分析相关"])


@router.get("/")
async def index():
    return {"index": "analyse"}
