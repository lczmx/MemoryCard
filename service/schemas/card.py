# 卡片
from typing import List
from datetime import datetime

from pydantic import BaseModel, Field

from service.schemas.user import DBUserModel
from service.schemas.category import DBCategoryModel, ReadCategoryModel, ReadNoLoadPlanCategoryModel


class StarModel(BaseModel):
    is_star: bool = Field(..., alias="isStar")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BaseCardModel(BaseModel):
    title: str


class ParamsCardModel(BaseCardModel):
    # 接收卡片参数
    cid: int = Field(..., alias="category")
    summary: str
    description: str


class WriteCardModel(ParamsCardModel):
    uid: int

    class Config:
        allow_population_by_field_name = True


class ReadSummaryCardModel(BaseCardModel, StarModel):
    # 预览的数据
    id: int
    review_at: datetime = Field(None, alias="reviewAt")
    review_times: int = Field(None, alias="reviewTimes")
    category: ReadCategoryModel

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ReadNoLoadPlanCardModel(ReadSummaryCardModel):
    """
    只取复习曲线id的情况
    """
    category: ReadNoLoadPlanCategoryModel

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ReadDescriptionCardModel(ReadSummaryCardModel):
    # 详细的数据
    summary: str
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ReadDescNoPlanCardModel(ReadDescriptionCardModel):
    # 详细的数据, 没有复习曲线
    summary: str
    description: str
    category: ReadNoLoadPlanCategoryModel

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OnlyCategoryID(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ReadNoCategoryCardModel(ReadDescriptionCardModel):
    category: OnlyCategoryID

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BatchCard(BaseModel):
    # 批量处理卡片
    cards: List[int]


class ResetModel(BaseModel):
    cid: int


class ReadResetModel(BaseModel):
    id: int
    review_at: datetime = Field(None, alias="reviewAt")
    review_times: int = Field(None, alias="reviewTimes")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DBCardModel(BaseModel):
    """
    数据库模型
    """
    id: int
    user: DBUserModel
    category: DBCategoryModel
    title: str
    created_at: datetime
    updated_at: datetime
    review_at: datetime
    review_times: int
    summary: str
    description: str
    is_star: bool
