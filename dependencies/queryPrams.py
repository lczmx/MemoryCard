"""
用于接收query参数的依赖
"""
from fastapi import Query


def get_limit_prams(limit: int = Query(10, ge=0, le=50, description="查询条数"),
                    offset: int = Query(0, ge=0, description="跳过多少条")):
    return {"limit": limit, "offset": offset}
