"""
分类页面
"""
from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from service.schemas.category import ParamsCategoryModel, ReadCategoryModel, StarModel, BatchCategory, \
    ResetCardByCategory, ReadNoLoadPlanCategoryModel
from service.schemas.generic import GenericResponse, QueryLimit
from dependencies.queryParams import get_limit_params, convert_category_order
from dependencies.auth import jwt_get_current_user
import settings

from service.schemas.user import DBUserModel
from service.schemas.other import DBOperationModel
from service import utils
from service.models import Category, Plan, Card, Record
from orm.exceptions import NoMatch, MultipleMatches
from dependencies import orm, tasks

router = APIRouter(prefix="/category", tags=["分类相关"], dependencies=[Depends(tasks.rollback_all_category)])


@router.get("/", response_model=GenericResponse[List[ReadNoLoadPlanCategoryModel]])
async def get_category(query_limit_params: QueryLimit = Depends(get_limit_params),
                       order=Depends(convert_category_order), user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取全部分类
    """
    # uid = user.id
    if order and order not in ["cardCount", "-cardCount"]:
        category_data = await Category.objects.filter(user=user).limit(query_limit_params.limit).offset(
            query_limit_params.offset).order_by(order).all()
    elif order in ["cardCount", "-cardCount"]:
        # TODO: 优化
        category_lst = await Category.objects.filter(user=user).all()
        result = []
        for category in category_lst:
            # 对比数据
            # 查询需要复习的卡片
            cards = await Card.objects.filter(user=user, category=category).all()
            res = ReadNoLoadPlanCategoryModel.from_orm(category)
            res.count = len(cards)
            result.append(res.dict())
        if order == "cardCount":
            category_data = sorted(result, key=lambda x: x.get('count'))[
                            query_limit_params.offset:query_limit_params.offset + query_limit_params.limit]
        else:
            category_data = sorted(result, key=lambda x: x.get('count'), reverse=True)[
                            query_limit_params.offset:query_limit_params.offset + query_limit_params.limit]



    else:
        category_data = await Category.objects.filter(user=user).limit(query_limit_params.limit).offset(
            query_limit_params.offset).all()

    return {
        "status": 1,
        "msg": "获取成功",
        "data": category_data
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadNoLoadPlanCategoryModel],
             response_model_exclude_unset=True)
async def create_category(category_params: ParamsCategoryModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    创建一个分类
    """
    # 判断有无复习曲线
    try:
        plan = await Plan.objects.get(pk=category_params.pid)
    except (NoMatch, MultipleMatches):
        return {"status": 0, "msg": "创建类别失败"}
    params = category_params.dict(exclude={"pid"})
    params.update({"user": user, "plan": plan})
    category = await Category.objects.create(**params)
    return {
        "status": 1,
        "msg": "创建类别成功",
        "data": category
    }


@router.post("/reset", response_model=GenericResponse, response_model_exclude_unset=True)
async def reset_card_category(category_data: ResetCardByCategory, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    分类的所有卡片的复习
    """
    category = await Category.objects.filter(user=user, pk=category_data.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的分类")
    cards = await Card.objects.filter(category=category).all()
    await utils.reset_card_review(cards)
    return {
        "status": 1,
        "msg": "重置成功",
    }


@router.post("/batch-star", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_category(batch_data: BatchCategory, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    批量星标类别
    """
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.category:
        category = await Category.objects.filter(pk=cid, user=user).first()
        if not category:
            batch_status["fail_count"] += 1
            continue
        await category.update(is_star=True)
        batch_status["success_count"] += 1
    return {
        "status": 1,
        "msg": f"成功星标卡片数: {batch_status.get('success_count')}, 失败星标卡片数: {batch_status.get('fail_count')}",
    }


@router.delete("/batch-delete", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_delete_category(batch_data: BatchCategory, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    批量删除类别
    """
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.category:
        category = await Category.objects.filter(pk=cid, user=user).first()
        if not category:
            batch_status["fail_count"] += 1
            continue
        # await category.delete()
        batch_status["success_count"] += 1
    return {
        "status": 1,
        "msg": f"成功删除卡片数: {batch_status.get('success_count')}, 失败删除卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    切换分类星标状态
    """
    category = await Category.objects.filter(pk=cid, user=user).first()
    if not category:
        return {"status": 0, "msg": "切换失败", "data": {"is_star": star_status.is_star}}
    await category.update(is_star=not star_status.is_star)
    return {"status": 1, "msg": "切换成功", "data": {"is_star": not star_status.is_star}}


@router.get("/{cid}", response_model=GenericResponse[ReadCategoryModel])
async def retrieve_category(cid: int, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    检索一条分类
    """
    category = await Category.objects.filter(user=user, pk=cid).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的分类")

    await category.plan.load()
    return {
        "status": 1,
        "msg": "获取成功",
        "data": category
    }


@router.post("/{cid}", response_model=GenericResponse[ReadNoLoadPlanCategoryModel])
async def update_category(cid: int, category_prams: ParamsCategoryModel,
                          user: DBUserModel = Depends(jwt_get_current_user),
                          no_login_user: DBUserModel = Depends(orm.get_no_login_user)):
    """
    更新一条分类
    """
    category = await Category.objects.filter(user=user, pk=cid).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的分类")

    plan = await Plan.objects.filter(pk=category_prams.pid).first()
    # 确保复习曲线是用户的
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的复习曲线")
    if plan.user.pk != user.id and plan.user.pk != no_login_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="禁止访问")
    # 假如修改复习曲线, 需要重置该类别的所有卡片复习
    if category.plan.pk != plan.pk:
        cards = await Card.objects.filter(category=category).all()
        await utils.reset_card_review(cards)

    data = category_prams.dict(exclude={"pid"})
    await category.update(**data, plan=plan)
    return {
        "status": 1,
        "msg": "更新成功",
        "data": category
    }


@router.delete("/{cid}", response_model=GenericResponse, response_model_exclude_unset=True)
async def delete_category(cid: int, user: DBUserModel = Depends(jwt_get_current_user),
                          operation: DBOperationModel = Depends(
                              orm.get_operation(settings.OPERATION_DATA["delete_category"]))):
    """
    删除一条分类
    """
    category = await Category.objects.filter(pk=cid, user=user).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的分类")

    # await category.delete()
    await Record.objects.create(user=user, operation=operation)
    return {
        "status": 1,
        "msg": "删除成功",
    }
