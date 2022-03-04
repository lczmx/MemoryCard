"""
定义复习曲线模型
"""
from typing import Optional

from pydantic import BaseModel
from service.schemas.user import DBUserModel


class BasePlanModel(BaseModel):
    title: str
    content: str


class ParamsPlanModel(BasePlanModel):
    """
    可以作为请求体接收参数
    """
    pass


class ReadPlanModel(BasePlanModel):
    """
    返回的
    """
    id: int
    editable: Optional[bool] = None

    class Config:
        orm_mode = True


class WritePlanModel(BasePlanModel):
    """
    写入数据库的
    """
    uid: Optional[int] = None


class ReadNoLoadPlanID(BaseModel):
    # 复习曲线ID
    id: int

    class Config:
        orm_mode = True


class DBPlanModel(BaseModel):
    id: int
    user: DBUserModel
    title: str
    content: str
