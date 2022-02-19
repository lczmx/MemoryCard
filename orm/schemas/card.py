# 卡片
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from orm.schemas.category import ReadCategoryModel


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


class ReadDescriptionCardModel(ReadSummaryCardModel):
    # 详细的数据
    summary: str
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
