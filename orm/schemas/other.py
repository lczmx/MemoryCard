from pydantic import BaseModel


class ReadDocModel(BaseModel):
    title: str
    tag: str
    content: str

    class Config:
        orm_mode = True
