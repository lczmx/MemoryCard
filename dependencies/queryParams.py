"""
用于接收query参数的依赖
"""
from fastapi import Query
from orm.schemas.generic import QueryLimit


def get_limit_params(limit: int = Query(10, ge=0, le=50, description="查询条数"),
                     offset: int = Query(0, ge=0, description="跳过多少条")) -> QueryLimit:
    data = {"limit": limit, "offset": offset}
    return QueryLimit(**data)
