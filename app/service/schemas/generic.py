from datetime import date as datetime_date
from typing import Optional, Generic, TypeVar, Type
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

# ##### orm

DataT = TypeVar("DataT")


class GenericResponse(GenericModel, Generic[DataT]):
    """
    通用返回数据
    单个数据时:
    GenericResponse[WriteCategoryModel]
    多个数据时:
    GenericResponse[List[WriteCategoryModel]]
    """
    status: int
    msg: str
    data: Optional[DataT] = None


class QueryLimit(BaseModel):
    limit: int = Field(10, ge=0, le=50, description="查询条数")  # 最多可以查询50条
    offset: int = Field(0, ge=0, description="跳过多少条")


class CardDateQueryLimit(QueryLimit):
    date: datetime_date
