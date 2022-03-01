"""
其他的路由
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from orm.schemas.other import ReadDocModel
from orm.crud import query_all_docs
from orm.schemas.generic import GenericResponse
from orm.models import User
from dependencies.orm import get_session
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/help", tags=["帮助相关"])


@router.get("/docs", response_model=GenericResponse[List[ReadDocModel]])
async def get_docs(session: Session = Depends(get_session), _: User = Depends(jwt_get_current_user)):
    """
    获取帮助文档
    """
    docs = query_all_docs(session=session)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": docs
    }
