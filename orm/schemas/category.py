"""
定义分类数据模型
"""
from typing import List
from pydantic import BaseModel, Field
from orm.schemas.plan import ReadPlanModel


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
        orm_mode = True
        allow_population_by_field_name = True


class ReadCategoryModel(BaseCategoryModel, StarModel):
    """
    返回的单个分类
    """
    id: int
    plan: ReadPlanModel
    count: int = Field(None, alias='cardCount')  # 类别的卡片数量

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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
