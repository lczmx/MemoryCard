"""
定义分类数据模型
"""

from pydantic import BaseModel, Field
from orm.schemas.plan import ReadPlanModel


class BaseCategoryModel(BaseModel):
    name: str
    icon: str
    color: str = Field(..., max_length=7)


class PramsCategoryModel(BaseCategoryModel):
    """
    添加分类请求体
    """
    pid: int = Field(..., alias="plan")


class ReadCategoryModel(BaseCategoryModel):
    """
    返回的单个分类
    """
    id: int
    plan: ReadPlanModel

    class Config:
        orm_mode = True


class WriteCategoryModel(BaseCategoryModel):
    """
    要保存到数据库的分类
    """
    uid: int
    pid: int
    is_star: bool = Field(False, alias="isStar")
