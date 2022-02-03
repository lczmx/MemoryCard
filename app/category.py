"""
分类页面
"""
from fastapi import APIRouter

router = APIRouter(prefix="/category")


@router.get("/")
async def index():
    return {"index": "category"}
