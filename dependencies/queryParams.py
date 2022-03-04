"""
用于接收query参数的依赖
"""
import datetime

from fastapi import Query

from service.schemas.generic import QueryLimit, CardDateQueryLimit


def get_limit_params(limit: int = Query(10, ge=0, le=50, description="查询条数"),
                     offset: int = Query(0, ge=0, description="跳过多少条")) -> QueryLimit:
    data = {"limit": limit, "offset": offset}
    return QueryLimit(**data)


def get_card_by_date_limit_params(
        limit: int = Query(10, ge=0, le=50, description="查询条数"),
        offset: int = Query(0, ge=0, description="跳过多少条"),
        date: datetime.date = Query(..., description="要查询的日期")
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
        "createAt": "created_at",
        "-createAt": "-created_at",
        "title": "title",
        "-title": "-title",
        "category": "category",
        "-category": "-category",
    }
    return convert_ref.get(order, None)


def convert_category_order(order: str = Query("", description="排序方式")):
    """
    将参数中的字段转换为与数据库中对应的
    :param order:
    :return:
    """
    convert_ref = {
        # createAt 替换为id
        "createAt": "id",
        "-createAt": "-id",
        "name": "name",
        "-name": "-name",
        "cardCount": "cardCount",
        "-cardCount": "-cardCount",
    }
    return convert_ref.get(order, None)
