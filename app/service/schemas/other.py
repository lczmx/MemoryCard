from pydantic import BaseModel
from datetime import date
from service.schemas.user import DBUserModel


class ReadDocModel(BaseModel):
    title: str
    tag: str
    content: str

    class Config:
        orm_mode = True


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
