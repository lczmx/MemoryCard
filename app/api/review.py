"""
复习
"""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, Query, status as http_status
from fastapi.exceptions import HTTPException

from service import utils
from models import Card, Record, Category
from schemas.generic import QueryLimit, GenericResponse, CardDateQueryLimit
from schemas.card import ReadSummaryCardModel, BatchCard, ReadDescNoPlanCardModel
from schemas.category import ReadNoLoadPlanCategoryModel
from schemas.user import DBUserModel
from schemas.other import DBOperationModel

from dependencies import orm
from dependencies.queryParams import get_limit_params, get_card_by_date_limit_params
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/review", tags=["复习相关"])


@router.get("/", response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_review(
        limit_params: QueryLimit = Depends(get_limit_params),
        cid: int = Query(None, ge=0, description="类别的id", alias="category"),
        user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取所有需要复习卡片
    """
    # 使用 prefetch_related 预加载 category 和 category__plan
    cards_query = Card.filter(user=user).prefetch_related("category__plan")
    if cid:
        cards_query = cards_query.filter(category__id=cid)
    cards = await cards_query.limit(limit_params.limit).offset(limit_params.offset).all()
    # 判断可以复习
    need_review_cards = await utils.use_need_review_cards(cards)

    return {
        "status": 1,
        "msg": "获取成功",
        "data": need_review_cards
    }


@router.post("/batch-review", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_review_card(review_cards: BatchCard, user: DBUserModel = Depends(jwt_get_current_user),
                            operation: DBOperationModel = Depends(
                                orm.get_operation("review_card"))):
    """
    批量复习卡片
    """
    status = {
        "success_count": 0,
        "fail_count": 0,
    }
    plans = {}  # key: plan ID  value: plan分割后的列表
    for cid in review_cards.cards:
        # 使用 prefetch_related 预加载 category__plan
        card = await Card.filter(pk=cid).prefetch_related("category__plan").first()
        if not card:
            status["fail_count"] += 1
            continue

        # 必须是需要复习的
        if not await utils.card_can_review(card):
            status["fail_count"] += 1
            continue

        # 可以完成复习, 判断是否已经复习完了
        plan_lst = plans.setdefault(card.category.plan.pk, [i for i in card.category.plan.content.split("-") if i])

        old_times = card.review_times
        if old_times >= len(plan_lst):
            # times == len 时, 已经全部复习完了
            status["fail_count"] += 1
            continue
        new_times = old_times + 1
        card.review_at = datetime.now()
        card.review_times = new_times
        await card.save()
        await Record.create(user=user, operation=operation)
        status["success_count"] += 1
    # 返回
    return {
        "status": 1,
        "msg": f"成功复习次数: {status.get('success_count')}, 失败复习次数: {status.get('fail_count')}"
    }


@router.get("/need", response_model=GenericResponse[List[int]])
async def get_need_card_id(limit_params: QueryLimit = Depends(get_limit_params),
                           user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取需要复习的卡片的ID
    """
    # TODO: 优化查询, 可以跳过offset
    cards = await Card.filter(user=user).all()
    cards_id_lst = [card.pk for card in cards if await utils.card_can_review(card)]

    return {
        "status": 1,
        "msg": "获取成功",
        "data": cards_id_lst[limit_params.offset: limit_params.offset + limit_params.limit]
    }


@router.get("/date", response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_card_by_date(query_params: CardDateQueryLimit = Depends(get_card_by_date_limit_params),
                           user: DBUserModel = Depends(jwt_get_current_user)):
    """
    根据日期获取需要复习的卡片
    """
    # 使用 prefetch_related 预加载 category__plan
    cards = await Card.filter(user=user).prefetch_related("category__plan").all()

    can_review_cards = [card for card in cards if
                        await utils.card_can_review_by_date(card, query_date=query_params.date)]

    need_review_cards = can_review_cards[query_params.offset: query_params.offset + query_params.limit]

    return {
        "status": 1,
        "msg": "获取成功",
        "data": need_review_cards
    }


@router.get("/category", response_model=GenericResponse[List[ReadNoLoadPlanCategoryModel]])
async def get_review_card_category(limit_params: QueryLimit = Depends(get_limit_params),
                                   user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取要复习卡片的类别
    """
    # 使用 prefetch_related 预加载 plan 关系
    category_lst = await Category.filter(user=user).prefetch_related("plan").all()
    result = []
    for category in category_lst:
        # 查询需要复习的卡片
        cards = await Card.filter(user=user, category=category).all()
        need_review_cards = await utils.use_need_review_cards(cards)
        if need_review_cards:
            res = ReadNoLoadPlanCategoryModel.from_orm(category)
            res.count = len(need_review_cards)
            result.append(res.dict())

    return {
        "status": 1,
        "msg": "获取成功",
        "data": result[limit_params.offset: limit_params.offset + limit_params.limit]
    }


@router.get("/{cid}", response_model=GenericResponse[ReadDescNoPlanCardModel])
async def get_card(cid: int, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取一条需要复习卡片
    """
    card = await Card.filter(user=user, pk=cid).first()
    if not card:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="不存在的卡片")
    # 必须是需要复习的
    if await utils.card_can_review(card):
        return {"status": 1, "msg": "获取成功", "data": card}
    else:
        return {"status": 0, "msg": "获取失败, 该卡片未到复习时间", "data": None}


@router.post("/{cid}", response_model=GenericResponse, response_model_exclude_none=True)
async def review_done(cid: int, user: DBUserModel = Depends(jwt_get_current_user),
                      operation: DBOperationModel = Depends(
                          orm.get_operation("review_card"))):
    """
    完成卡片复习
    """
    card = await Card.filter(user=user, pk=cid).first()
    if not card:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="不存在的卡片")
    # 必须是需要复习的
    if not await utils.card_can_review(card):
        return {"status": 0, "msg": "该卡片未到复习时间"}

    plan = await utils.get_card_plan(card)

    # 可以完成复习
    plan_count = len([i for i in plan.content.split("-") if i])
    old_times = card.review_times
    if old_times >= plan_count:
        # times == len 时, 已经全部复习完了
        return {"status": 0, "msg": "该卡片已复习完毕"}
    # ## 完成复习, 更新数据
    new_times = old_times + 1
    card.review_at = datetime.now()
    card.review_times = new_times
    await card.save()
    await Record.create(user=user, operation=operation)
    return {"status": 1, "msg": "复习成功"}
