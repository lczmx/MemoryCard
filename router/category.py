"""
分类页面
"""
from typing import List, Dict

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from orm.schemas.category import ParamsCategoryModel, WriteCategoryModel, ReadCategoryModel, StarModel
from orm.schemas.generic import GenericResponse, QueryLimit
from orm.crud import save_one_to_db, query_all_data_by_user
from orm.crud import toggle_star_status
from orm.models import Category
from dependencies.queryParams import get_limit_params
from dependencies.orm import get_session

router = APIRouter(prefix="/category", tags=["分类相关"])


@router.get("/",
            response_model=GenericResponse[List[ReadCategoryModel]])
async def index(query_limit_params: QueryLimit = Depends(get_limit_params),
                session: Session = Depends(get_session)):
    """
    获取全部分类
    """

    uid = 1

    category_data = query_all_data_by_user(session, uid=uid, model_class=Category, query_params=query_limit_params)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": category_data
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadCategoryModel],
             response_model_exclude_unset=True)
async def create_category(category_prams: ParamsCategoryModel,
                          session: Session = Depends(get_session)):
    """
    创建一个分类
    """
    prams = category_prams.dict()
    prams.update({
        "uid": 1
    })
    data = WriteCategoryModel(**prams)

    category_obj = save_one_to_db(session=session, model_class=Category, data=data)
    return {
        "status": 1,
        "msg": "success",
        "data": category_obj
    }


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, session: Session = Depends(get_session)):
    """
    切换分类星标状态
    """
    now_status = toggle_star_status(session, model_class=Category, target_id=cid, star_status=star_status.is_star)
    msg = "切换成功" if star_status.is_star != now_status else "切换失败"
    return {
        "status": 1,
        "msg": msg,
        "data": {
            "is_star": now_status
        }

    }
