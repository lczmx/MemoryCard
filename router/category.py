"""
分类页面
"""
from typing import List, Dict

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from orm.schemas.category import ParamsCategoryModel, WriteCategoryModel, ReadCategoryModel, StarModel, BatchCategory
from orm.schemas.generic import GenericResponse, QueryLimit
from orm.crud import save_one_to_db, query_all_data_by_user, query_one_data_by_user, \
    update_data, delete_category_data, toggle_star_status, query_category_by_user_order_card_count
from orm.models import Category, User
from dependencies.queryParams import get_limit_params, convert_category_order
from dependencies.orm import get_session
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/category", tags=["分类相关"])


@router.get("/",
            response_model=GenericResponse[List[ReadCategoryModel]])
async def get_category(query_limit_params: QueryLimit = Depends(get_limit_params),
                       order=Depends(convert_category_order), session: Session = Depends(get_session),
                       user: User = Depends(jwt_get_current_user)):
    """
    获取全部分类
    """

    uid = user.id
    if order in ["cardCount", "-cardCount"]:
        # 根据卡片数量排序, 不能使用通用的方法
        category_data = query_category_by_user_order_card_count(session, uid=uid,
                                                                query_params=query_limit_params, order=order)
    else:
        category_data = query_all_data_by_user(session, uid=uid, model_class=Category, query_params=query_limit_params,
                                               order=order)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": category_data
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadCategoryModel],
             response_model_exclude_unset=True)
async def create_category(category_prams: ParamsCategoryModel, session: Session = Depends(get_session),
                          user: User = Depends(jwt_get_current_user)):
    """
    创建一个分类
    """
    prams = category_prams.dict()
    prams.update({
        "uid": user.id
    })
    data = WriteCategoryModel(**prams)

    category_obj = save_one_to_db(session=session, model_class=Category, data=data)
    return {
        "status": 1,
        "msg": "success",
        "data": category_obj
    }


@router.post("/batch-star", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_category(batch_data: BatchCategory, session: Session = Depends(get_session),
                              user: User = Depends(jwt_get_current_user)):
    """
    批量星标类别
    """
    uid = user.id
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.category:
        rowcount = toggle_star_status(session, model_class=Category, target_id=cid, uid=uid, star_status=False)
        if not rowcount:  # 0时, 星标失败
            batch_status["fail_count"] += 1
            continue
        batch_status["success_count"] += 1

    return {
        "status": 1,
        "msg": f"成功星标卡片数: {batch_status.get('success_count')}, 失败星标卡片数: {batch_status.get('fail_count')}",
    }


@router.delete("/batch-delete", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_delete_category(batch_data: BatchCategory, session: Session = Depends(get_session),
                                user: User = Depends(jwt_get_current_user)):
    """
    批量删除类别
    """
    uid = user.id
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.category:
        rowcount = delete_category_data(session=session, uid=uid, cid=cid)
        # rowcount = 0 时
        if not rowcount:
            batch_status["fail_count"] += 1
            continue
        batch_status["success_count"] += 1
    return {
        "status": 1,
        "msg": f"成功删除卡片数: {batch_status.get('success_count')}, 失败删除卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, session: Session = Depends(get_session),
                      user: User = Depends(jwt_get_current_user)):
    """
    切换分类星标状态
    """
    uid = user.id

    rowcount = toggle_star_status(session, model_class=Category, target_id=cid, uid=uid,
                                  star_status=star_status.is_star)
    msg = "切换成功" if rowcount else "切换失败"
    now_status = not star_status.is_star if rowcount else star_status.is_star
    return {
        "status": 1,
        "msg": msg,
        "data": {
            "is_star": now_status
        }

    }


@router.get("/{cid}", response_model=GenericResponse[ReadCategoryModel])
async def retrieve_category(cid: int, session: Session = Depends(get_session),
                            user: User = Depends(jwt_get_current_user)):
    """
    检索一条分类
    """
    uid = user.id
    category_data = query_one_data_by_user(session=session, uid=uid, target_id=cid, model_class=Category)
    if not category_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的分类")
    return {
        "status": 1,
        "msg": "获取成功",
        "data": category_data
    }


@router.post("/{cid}", response_model=GenericResponse[ReadCategoryModel])
async def update_category(cid: int, category_prams: ParamsCategoryModel, session: Session = Depends(get_session),
                          user: User = Depends(jwt_get_current_user)):
    """
    更新一条分类
    """
    uid = user.id
    # TODO: 修改plan时 重置 review_at和review_times
    category_data = update_data(session=session, uid=uid, target_id=cid, model_class=Category, data=category_prams)

    return {
        "status": 1,
        "msg": "更新成功",
        "data": category_data
    }


@router.delete("/{cid}", response_model=GenericResponse, response_model_exclude_unset=True)
async def delete_category(cid: int, session: Session = Depends(get_session),
                          user: User = Depends(jwt_get_current_user)):
    """
    删除一条分类
    """
    uid = user.id
    rowcount = delete_category_data(session=session, uid=uid, cid=cid)
    if not rowcount:
        return {
            "status": 0,
            "msg": "删除失败",
        }
    return {
        "status": 1,
        "msg": "删除成功",
    }
