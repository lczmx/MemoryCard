"""
定义复习曲线模型
"""
from typing import Optional

from pydantic import BaseModel


class BasePlanModel(BaseModel):
    title: str
    content: str


class PramsPlanModel(BasePlanModel):
    """
    可以作为请求体接收参数
    """
    pass


class ReadPlanModel(BasePlanModel):
    """
    返回的
    """
    id: int

    class Config:
        orm_mode = True


class WritePlanModel(BasePlanModel):
    """
    写入数据库的
    """
    uid: Optional[int] = None
