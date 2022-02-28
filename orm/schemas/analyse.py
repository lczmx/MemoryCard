# 分析数据
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta, date


class DiffAnalyse(BaseModel):
    # 比较
    today: int
    incr: int  # 新增


class SummaryAnalyseModel(BaseModel):
    # 概览信息
    review: DiffAnalyse
    create: DiffAnalyse
    category_count: int = Field(..., alias="categoryCount")

    class Config:
        allow_population_by_field_name = True


class ReadAnalyseModel(BaseModel):
    # 给曲线的数据
    count: int
    create_at: date = Field(..., alias="date")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ParamsAnalyseModel(BaseModel):
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")

    @validator("start_date")
    def vali_min_date(cls, v, **kwargs):
        min_date = datetime.now() - timedelta(days=366)
        if min_date.date() > v:
            # 最小值为一年
            return min_date.strftime("%Y/%m/%d")
        return v

    @validator("end_date")
    def vali_max_date(cls, v, **kwargs):
        max_date = datetime.now()
        if max_date.date() < v:
            # 不能超过今天
            return max_date.strftime("%Y/%m/%d")
        return v


class WriteOperationModel(BaseModel):
    # 与记录相关
    id: int
    title: str


class WriteRecodeModel(BaseModel):
    # 与记录相关
    uid: int
    oid: int
    create_at: date
