"""
主页
"""
from fastapi import APIRouter

router = APIRouter(prefix="/home")


@router.get("/")
async def index():
    return {"index": "home"}
