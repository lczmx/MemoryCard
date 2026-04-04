from datetime import date as datetime_date
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class GenericResponse(BaseModel, Generic[DataT]):
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


class PaginationMeta(BaseModel):
    """
    分页元数据
    """
    total: int = Field(description="总记录数")
    limit: int = Field(description="每页记录数")
    offset: int = Field(description="跳过记录数")
    page: int = Field(description="当前页码 (从1开始)")
    page_size: int = Field(description="每页记录数 (与limit一致)")
    total_pages: int = Field(description="总页数")
    has_next: bool = Field(description="是否有下一页")
    has_prev: bool = Field(description="是否有上一页")


class PaginatedData(BaseModel, Generic[DataT]):
    """
    带分页信息的数据列表
    """
    items: List[DataT] = Field(description="数据列表")
    meta: PaginationMeta = Field(description="分页元数据")


class PaginatedResponse(GenericResponse[PaginatedData[DataT]]):
    """
    分页响应
    """
    pass


class QueryLimit(BaseModel):
    limit: int = Field(10, ge=0, le=50, description="查询条数")  # 最多可以查询50条
    offset: int = Field(0, ge=0, description="跳过多少条")


class CardDateQueryLimit(QueryLimit):
    date: datetime_date
