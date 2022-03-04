"""
其他的路由
"""
from typing import List

from fastapi import APIRouter, Depends

from service.models import Doc
from service.schemas.other import ReadDocModel
from service.schemas.generic import GenericResponse
from service.schemas.user import DBUserModel
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/help", tags=["帮助相关"])


@router.get("/docs", response_model=GenericResponse[List[ReadDocModel]])
async def get_docs(_: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取帮助文档
    """
    docs = await Doc.objects.all()
    return {
        "status": 1,
        "msg": "获取成功",
        "data": docs
    }
