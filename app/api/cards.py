"""
获取卡片数据
"""
from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from schemas.card import ParamsCardModel, ReadSummaryCardModel, ReadNoCategoryCardModel, StarModel, BatchCard, \
    ResetModel, ReadResetModel
from schemas.generic import GenericResponse, QueryLimit

from models import Card, Category, Record
from schemas.user import DBUserModel
from schemas.other import DBOperationModel
from schemas.card import ReadDescNoPlanCardModel
from dependencies.queryParams import get_limit_params, convert_card_order
from dependencies.auth import jwt_get_current_user
from dependencies import orm

from service import utils

router = APIRouter(prefix="/cards", tags=["卡片相关"])


@router.get("/", response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_cards(limit_params: QueryLimit = Depends(get_limit_params), order=Depends(convert_card_order),
                    user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取多个卡片
    """
    # 先预加载 category 和 category__plan 关系
    cards = Card.filter(user=user).prefetch_related("category__plan")
    if order:
        cards = cards.order_by(order)
    cards = await cards.limit(limit_params.limit).offset(limit_params.offset).all()
    return {
        "status": 1,
        "msg": "获取成功",
        "data": cards
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadNoCategoryCardModel])
async def create_card(card_data: ParamsCardModel, user: DBUserModel = Depends(jwt_get_current_user),
                      operation: DBOperationModel = Depends(orm.get_operation("create_card"))):
    """
    创建卡片
    """

    category = await Category.filter(pk=card_data.cid, user=user).first()
    if not category:
        return {"status": 0, "msg": "不存在的类别", "data": None}
    card = await Card.create(**card_data.dict(exclude={"cid"}), user=user, category=category)
    if not card:
        return {"status": 0, "msg": "创建失败", "data": None}
    await Record.create(user=user, operation=operation)

    return {"status": 1, "msg": "创建成功", "data": card}


@router.post("/reset", response_model=GenericResponse[ReadResetModel], response_model_exclude_unset=True)
async def reset_card(reset_data: ResetModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    重置卡片的复习
    """
    card = await Card.filter(user=user, pk=reset_data.cid).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")
    await utils.reset_card_review([card, ])
    return {
        "status": 1,
        "msg": "重置成功",
        "data": card
    }


@router.post("/batch-star", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_card(batch_data: BatchCard, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    批量星标卡片
    """

    batch_status = {"success_count": 0, "fail_count": 0, }
    cards = await Card.filter(id__in=batch_data.cards, user=user).all()
    for card in cards:
        card.is_star = True
        await card.save()
        batch_status["success_count"] += 1

    batch_status["fail_count"] = len(batch_data.cards) - batch_status["success_count"]

    return {
        "status": 1,
        "msg": f"成功星标卡片数: {batch_status.get('success_count')}, 失败星标卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/batch-reset", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_card(batch_data: BatchCard, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    批量重置卡片
    """

    batch_status = {"success_count": 0, "fail_count": 0}
    cards = await Card.filter(id__in=batch_data.cards, user=user).all()

    batch_status["success_count"] = await utils.reset_card_review(cards)
    batch_status["fail_count"] = len(batch_data.cards) - batch_status["success_count"]

    return {
        "status": 1,
        "msg": f"成功重置卡片数: {batch_status.get('success_count')}, 失败重置卡片数: {batch_status.get('fail_count')}",
    }


@router.delete("/batch-delete", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_delete_card(batch_data: BatchCard, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    批量删除卡片
    """
    batch_status = {"success_count": 0, "fail_count": 0}
    cards = await Card.filter(id__in=batch_data.cards, user=user).all()
    for card in cards:
        await card.delete()
        batch_status["success_count"] += 1
    batch_status["fail_count"] = len(batch_data.cards) - batch_status["success_count"]
    return {
        "status": 1,
        "msg": f"成功删除卡片数: {batch_status.get('success_count')}, 失败删除卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    切换分类星标状态
    """
    card = await Card.filter(pk=cid, user=user).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    now_status = not card.is_star
    card.is_star = now_status
    await card.save()
    msg = "切换成功" if now_status != star_status.is_star else "切换失败"
    return {
        "status": 1,
        "msg": msg,
        "data": {"is_star": now_status}}


@router.get("/{cid}", response_model=GenericResponse[ReadDescNoPlanCardModel])
async def retrieve_card(cid: int, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取一条卡片的数据
    """
    card = await Card.filter(pk=cid, user=user).prefetch_related("category__plan").first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    return {"status": 1, "msg": "获取成功", "data": card}


@router.post("/{cid}", response_model=GenericResponse[ReadNoCategoryCardModel])
async def update_card(cid: int, data: ParamsCardModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    修改一条卡片的数据
    """
    category = await Category.filter(pk=data.cid, user=user).first()
    if not category:
        return {"status": 0, "msg": "不存在的类别", "data": None}
    card = await Card.filter(pk=cid, user=user).prefetch_related("category").first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    # 查看是否修改了类别, 重置卡片复习
    if card.category.pk != category.pk:
        await utils.reset_card_review([card, ])
    await card.update_from_dict(data.dict(exclude={"cid"}))
    card.user = user
    card.category = category
    await card.save()
    return {"status": 1, "msg": "更新成功", "data": card}


@router.delete("/{cid}", response_model=GenericResponse, response_model_exclude_unset=True)
async def delete_card(cid: int, user: DBUserModel = Depends(jwt_get_current_user),
                      operation: DBOperationModel = Depends(orm.get_operation("delete_card"))):
    """
    删除一条卡片的数据
    """
    card = await Card.filter(pk=cid, user=user).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    await card.delete()
    await Record.create(operation=operation, user=user)
    return {"status": 1, "msg": "删除成功"}
