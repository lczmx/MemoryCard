"""
用于接收query参数的依赖
"""
from datetime import date as datetime_date

from fastapi import Query

from orm.models import Card, Category
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


def convert_card_order(order: str = Query("", description="排序方式")):
    """
    将参数中的字段转换为与数据库中对应的
    :param order:
    :return:
    """
    convert_ref = {
        "createAt": Card.created_at.asc,
        "-createAt": Card.created_at.desc,
        "title": Card.title.asc,
        "-title": Card.title.desc,
        "category": Card.cid.asc,
        "-category": Card.cid.desc,
    }
    return convert_ref.get(order, None)
