"""
分类页面
"""
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from orm.schemas.category import PramsCategoryModel, WriteCategoryModel, ReadCategoryModel
from orm.schemas.generic import GenericResponse, QueryLimit
from orm.crud import create_category as create_category_to_db
from dependencies.orm import get_session

router = APIRouter(prefix="/category", tags=["分类相关"])


@router.get("/")
async def index():
    return {"index": "category"}


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadCategoryModel],
             response_model_exclude_unset=True)
async def create_category(category_prams: PramsCategoryModel,
                          session: Session = Depends(get_session)):
    prams = category_prams.dict()
    prams.update({
        "uid": 1
    })
    data = WriteCategoryModel(**prams)

    category_obj = create_category_to_db(session, data)
    print(category_obj)
    return {
        "status": 1,
        "msg": "success",
        "data": category_obj
    }
