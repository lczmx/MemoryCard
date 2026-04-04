"""
定义分类数据模型
"""
from typing import List
from pydantic import BaseModel, Field

from schemas.user import DBUserModel
from schemas.plan import DBPlanModel, ReadPlanModel, ReadNoLoadPlanID


class BaseCategoryModel(BaseModel):
    name: str
    icon: str
    color: str = Field(..., max_length=7)


class ParamsCategoryModel(BaseCategoryModel):
    """
    添加分类请求体
    """
    pid: int = Field(..., alias="plan")


class StarModel(BaseModel):
    is_star: bool = Field(..., alias="isStar")

    class Config:
        from_attributes = True
        validate_by_name = True


class ReadCategoryModel(BaseCategoryModel, StarModel):
    """
    返回的单个分类
    """
    id: int
    plan: ReadPlanModel  # 用的时候才确定返回类型
    count: int = Field(None, alias='cardCount')  # 类别的卡片数量

    class Config:
        from_attributes = True
        validate_by_name = True


class ReadNoLoadPlanCategoryModel(ReadCategoryModel):
    """
    只返回复习的id
    """
    plan: ReadNoLoadPlanID

    class Config:
        from_attributes = True
        validate_by_name = True


class WriteCategoryModel(BaseCategoryModel):
    """
    要保存到数据库的分类
    """
    uid: int
    pid: int
    is_star: bool = Field(False, alias="isStar")


class BatchCategory(BaseModel):
    # 批量处理类别
    category: List[int]


class ResetCardByCategory(BaseModel):
    id: int


class DBCategoryModel(BaseModel):
    id: int
    user: DBUserModel
    plan: DBPlanModel
    name: str
    icon: str
    color: str
    is_star: bool
    phone_number: str
