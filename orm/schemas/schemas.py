"""
定义数据模型
Read开头用于返回数据的模型
"""
from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class QueryLimit(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class PlanModel(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class BaseCategoryModel(BaseModel):
    name: str
    icon: str
    color: str = Field(..., max_length=7)


class PramsCategoryModel(BaseCategoryModel):
    """
    添加分类请求体
    """
    name: str
    icon: str
    color: str = Field(..., max_length=7)


class ReadCategoryModel(BaseCategoryModel):
    """
    返回的单个分类
    """
    id: int
    plan: PlanModel

    class Config:
        orm_mode = True


class WriteCategoryModel(CategoryModel):
    """
    要保存到数据库的分类
    """
    uid: int
    pid: int
    is_star: bool = Field(False, alias="isStar")


