"""
其他的路由
"""
from typing import List

from fastapi import APIRouter, Depends

from models import Doc
from schemas.other import ReadDocModel
from schemas.generic import GenericResponse, PaginatedData, PaginationMeta
from schemas.user import DBUserModel
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/help", tags=["帮助相关"])


def build_pagination_meta(total: int, limit: int, offset: int) -> PaginationMeta:
    """
    构建分页元数据
    """
    page = (offset // limit) + 1 if limit > 0 else 1
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    return PaginationMeta(
        total=total,
        limit=limit,
        offset=offset,
        page=page,
        page_size=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/docs", response_model=GenericResponse[PaginatedData[ReadDocModel]])
async def get_docs(limit: int = 10, offset: int = 0, _: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取帮助文档
    """
    docs_query = Doc.all()
    total = await docs_query.count()
    docs = await docs_query.limit(limit).offset(offset).all()
    meta = build_pagination_meta(total, limit, offset)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": PaginatedData(items=docs, meta=meta)
    }
