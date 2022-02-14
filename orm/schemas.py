"""
定义数据模型
Read开头用于返回数据的模型
"""
from pydantic import BaseModel, EmailStr, Field


class TagModel(BaseModel):
    uid: int
    icon: str
    color: str


class ReadTagModel(TagModel):
    id: int

    class Config:
        orm_mode = True


class TagClassNameModel(BaseModel):
    class_name: str


class TagColorModel(BaseModel):
    color: str
