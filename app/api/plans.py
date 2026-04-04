from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from dependencies import orm
from dependencies.queryParams import get_limit_params
from dependencies.auth import jwt_get_current_user

from models import Plan, Card, Record, Category
from schemas.generic import QueryLimit, GenericResponse, PaginatedData, PaginationMeta
from schemas.plan import ReadPlanModel, ParamsPlanModel
from schemas.user import DBUserModel
from schemas.other import DBOperationModel
from service import utils

router = APIRouter(prefix="/plans", tags=["复习计划相关"])


@router.get('/', response_model=GenericResponse[PaginatedData[ReadPlanModel]])
async def get_plans(query_limit_params: QueryLimit = Depends(get_limit_params),
                    user: DBUserModel = Depends(jwt_get_current_user),
                    no_login_user: DBUserModel = Depends(orm.get_no_login_user)):
    """获取多个复习曲线"""
    plans = []
    # TODO: 优化offset
    default_plans = await Plan.filter(user=no_login_user).all()
    user_plans = await Plan.filter(user=user).all()
    for p in default_plans:
        temp = ReadPlanModel.from_orm(p)
        temp.editable = False
        plans.append(temp.dict())

    for p in user_plans:
        temp = ReadPlanModel.from_orm(p)
        temp.editable = True
        plans.append(temp)

    # 计算分页
    total = len(plans)
    page = (query_limit_params.offset // query_limit_params.limit) + 1 if query_limit_params.limit > 0 else 1
    total_pages = (total + query_limit_params.limit - 1) // query_limit_params.limit if query_limit_params.limit > 0 else 1
    paginated_plans = plans[query_limit_params.offset: query_limit_params.offset + query_limit_params.limit]
    meta = PaginationMeta(
        total=total,
        limit=query_limit_params.limit,
        offset=query_limit_params.offset,
        page=page,
        page_size=query_limit_params.limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    return {
        "status": 1,
        "msg": "获取成功",
        "data": PaginatedData(items=paginated_plans, meta=meta)
    }


@router.post('/', response_model=GenericResponse[ReadPlanModel])
async def create_plan(plan_data: ParamsPlanModel, user: DBUserModel = Depends(jwt_get_current_user),
                      operation: DBOperationModel = Depends(
                          orm.get_operation("create_plan"))):
    """
    创建复习曲线
    """
    plan = await Plan.create(**plan_data.dict(), user=user)

    if not plan:
        return {"status": 0, "msg": "创建失败", "data": plan}
    await Record.create(user=user, operation=operation)
    return {"status": 1, "msg": "创建成功", "data": plan}


@router.get('/{pid}', response_model=GenericResponse[ReadPlanModel])
async def get_plan(pid: int, user: DBUserModel = Depends(jwt_get_current_user),
                   no_login_user: DBUserModel = Depends(orm.get_no_login_user)):
    """
    获取一条复习曲线数据
    """
    # 使用 prefetch_related 预加载 user 关系
    user_plan = await Plan.filter(pk=pid, user=user).prefetch_related("user").first()
    default_plan = await Plan.filter(pk=pid, user=no_login_user).prefetch_related("user").first()

    if not user_plan and not default_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的复习曲线")
    plan = user_plan if user_plan else default_plan
    editable = True if user_plan else False
    temp = ReadPlanModel.from_orm(plan)
    temp.editable = editable
    return {"status": 1, "msg": "获取成功", "data": temp.dict()}


@router.post('/{pid}', response_model=GenericResponse[ReadPlanModel])
async def update_plan(pid: int, plan_data: ParamsPlanModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    修改一条复习曲线数据
    """
    # 使用 prefetch_related 预加载 user 关系
    plan = await Plan.filter(pk=pid).prefetch_related("user").first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的复习曲线")
    if plan.user.pk != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="禁止访问")

    if plan_data.content != plan.content:
        # 重置
        category = await Category.filter(plan=plan).all()
        # 重置卡片复习次数
        for c in category:
            cards = await Card.filter(category=c).all()
            await utils.reset_card_review(cards)

    await plan.update_from_dict(plan_data.dict())
    await plan.save()
    return {
        "status": 1,
        "msg": "修改成功",
        "data": plan
    }


@router.delete('/{pid}', response_model=GenericResponse, response_model_exclude_unset=True)
async def delete_plan(pid: int, user: DBUserModel = Depends(jwt_get_current_user),
                      no_login_user: DBUserModel = Depends(orm.get_no_login_user)):
    """
    删除一条复习计划
    """
    plan = await Plan.filter(user=user, pk=pid).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的复习曲线")
    # 设置类别的默认复习曲线
    category = await Category.filter(plan=plan).all()
    default_plan = await Plan.filter(user=no_login_user).first()
    if not default_plan:
        return {"status": 0, "msg": "删除失败, 没有默认复习曲线"}

    # 重置卡片复习次数
    for c in category:
        c.plan = default_plan
        await c.save()
        cards = await Card.filter(category=c).all()
        await utils.reset_card_review(cards)

    await plan.delete()

    return {"status": 1, "msg": "删除成功"}
