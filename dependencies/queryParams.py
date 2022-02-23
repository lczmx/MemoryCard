"""
用于接收query参数的依赖
"""
import datetime
from datetime import date as datetime_date

from fastapi import Query
from orm.schemas.generic import QueryLimit, CardDateQueryLimit


def get_limit_params(limit: int = Query(10, ge=0, le=50, description="查询条数"),
                     offset: int = Query(0, ge=0, description="跳过多少条")) -> QueryLimit:
    data = {"limit": limit, "offset": offset}
    return QueryLimit(**data)


def get_card_by_date_limit_params(
        limit: int = Query(10, ge=0, le=50, description="查询条数"),
        offset: int = Query(0, ge=0, description="跳过多少条"),
        date: datetime_date = Query(..., description="要查询的日期")
) -> CardDateQueryLimit:
    data = {"limit": limit, "offset": offset, "date": date}
    return CardDateQueryLimit(**data)