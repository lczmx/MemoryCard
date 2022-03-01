"""
获取卡片数据
"""
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from orm.schemas.card import ParamsCardModel, ReadSummaryCardModel, \
    ReadDescriptionCardModel, WriteCardModel, StarModel, BatchCard, ResetModel, ReadResetModel
from orm.schemas.generic import GenericResponse, QueryLimit

from orm.crud import save_one_to_db, query_all_data_by_user, toggle_star_status, \
    query_one_data_by_user, update_card_data, delete_data_by_user, recode_operation, reset_cards_review, \
    batch_reset_cards
from orm.models import Card, User
from dependencies.orm import get_session
from dependencies.queryParams import get_limit_params, convert_card_order
from dependencies.auth import jwt_get_current_user
import settings

router = APIRouter(prefix="/cards", tags=["卡片相关"])


@router.get("/",
            response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_cards(limit_params: QueryLimit = Depends(get_limit_params), order=Depends(convert_card_order),
                    session: Session = Depends(get_session), user: User = Depends(jwt_get_current_user)):
    """
    获取多个卡片
    """
    uid = user.id

    card_data = query_all_data_by_user(session, uid=uid, model_class=Card, query_params=limit_params, order=order)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": card_data
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadDescriptionCardModel])
async def create_card(card_data: ParamsCardModel, session: Session = Depends(get_session),
                      user: User = Depends(jwt_get_current_user)):
    """
    创建卡片
    """
    uid = user.id
    data = WriteCardModel(uid=uid, **card_data.dict())
    card_obj = save_one_to_db(session=session, model_class=Card, data=data)
    if not card_obj:
        return {
            "status": 0,
            "msg": "创建失败",
            "data": None
        }
    recode_operation(session=session, uid=uid, oid=settings.OPERATION_DATA["create_card"])
    return {
        "status": 1,
        "msg": "创建成功",
        "data": card_obj
    }


@router.post("/reset", response_model=GenericResponse[ReadResetModel], response_model_exclude_unset=True)
async def reset_card(reset_data: ResetModel, session: Session = Depends(get_session),
                     user: User = Depends(jwt_get_current_user)):
    """
    重置卡片的复习
    """
    uid = user.id
    card = query_one_data_by_user(session=session, uid=uid, target_id=reset_data.cid, model_class=Card)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    return {
        "status": 1,
        "msg": "重置成功",
        "data": reset_cards_review(session=session, uid=uid, cards=[card])[0]
    }


@router.post("/batch-star", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_card(batch_data: BatchCard, session: Session = Depends(get_session),
                          user: User = Depends(jwt_get_current_user)):
    """
    批量星标卡片
    """
    uid = user.id
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.cards:
        rowcount = toggle_star_status(session, model_class=Card, target_id=cid, uid=uid, star_status=False)
        if not rowcount:  # 0时, 星标失败
            batch_status["fail_count"] += 1
            continue
        batch_status["success_count"] += 1

    return {
        "status": 1,
        "msg": f"成功星标卡片数: {batch_status.get('success_count')}, 失败星标卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/batch-reset", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_card(batch_data: BatchCard, session: Session = Depends(get_session),
                          user: User = Depends(jwt_get_current_user)):
    """
    批量重置卡片
    """
    uid = user.id
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    cards = batch_reset_cards(session=session, uid=uid, cid_lst=batch_data.cards)
    for card in cards:
        if card.review_times:  # 0时, 成功
            batch_status["fail_count"] += 1
            continue
        batch_status["success_count"] += 1

    return {
        "status": 1,
        "msg": f"成功重置卡片数: {batch_status.get('success_count')}, 失败重置卡片数: {batch_status.get('fail_count')}",
    }


@router.delete("/batch-delete", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_delete_card(batch_data: BatchCard, session: Session = Depends(get_session),
                            user: User = Depends(jwt_get_current_user)):
    """
    批量删除卡片
    """
    uid = user.id
    batch_status = {
        "success_count": 0,
        "fail_count": 0,
    }
    for cid in batch_data.cards:
        rowcount = delete_data_by_user(session=session, uid=uid, target_id=cid, model_class=Card)
        # rowcount = 0 时
        if not rowcount:
            batch_status["fail_count"] += 1
            continue
        recode_operation(session=session, uid=uid, oid=settings.OPERATION_DATA["delete_card"])
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
    rowcount = toggle_star_status(session, model_class=Card, target_id=cid, uid=uid, star_status=star_status.is_star)
    msg = "切换成功" if rowcount else "切换失败"
    now_status = not star_status.is_star if rowcount else star_status.is_star

    return {
        "status": 1,
        "msg": msg,
        "data": {
            "is_star": now_status
        }

    }


@router.get("/{cid}", response_model=GenericResponse[ReadDescriptionCardModel])
async def retrieve_card(cid: int, session: Session = Depends(get_session), user: User = Depends(jwt_get_current_user)):
    """
    获取一条卡片的数据
    """

    uid = user.id
    card_data = query_one_data_by_user(session=session,
                                       uid=uid, target_id=cid, model_class=Card)
    if not card_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    return {
        "status": 1,
        "msg": "获取成功",
        "data": card_data

    }


@router.post("/{cid}", response_model=GenericResponse[ReadDescriptionCardModel])
async def update_card(cid: int, data: ParamsCardModel, session: Session = Depends(get_session),
                      user: User = Depends(jwt_get_current_user)):
    """
    修改一条卡片的数据
    """

    uid = user.id
    card_data = update_card_data(session=session, uid=uid, cid=cid, data=data)
    if not card_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    return {
        "status": 1,
        "msg": "更新成功",
        "data": card_data

    }


@router.delete("/{cid}", response_model=GenericResponse, response_model_exclude_unset=True)
async def delete_card(cid: int, session: Session = Depends(get_session), user: User = Depends(jwt_get_current_user)):
    """
    删除一条卡片的数据
    """

    uid = user.id
    rowcount = delete_data_by_user(session=session, uid=uid, target_id=cid, model_class=Card)
    # rowcount = 0 时
    if not rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")
    recode_operation(session=session, uid=uid, oid=settings.OPERATION_DATA["delete_card"])
    return {
        "status": 1,
        "msg": "删除成功",

    }
