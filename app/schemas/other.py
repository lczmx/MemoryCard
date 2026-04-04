from pydantic import BaseModel
from datetime import date
from schemas.user import DBUserModel


class ReadDocModel(BaseModel):
    title: str
    tag: str
    content: str

    class Config:
        from_attributes = True


class DBDocModel(BaseModel):
    id: int
    title: str
    tag: str
    content: str


class DBOperationModel(BaseModel):
    id: int
    title: str


class DBRecordModel(BaseModel):
    id: int
    user: DBUserModel
    operation: DBOperationModel
    create_at: date
