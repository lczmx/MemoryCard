"""
复习
"""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from orm.schemas.generic import QueryLimit, GenericResponse
from orm.schemas.card import ReadSummaryCardModel, ReadDescriptionCardModel
from orm.crud import query_need_review_card, query_one_data_by_user, update_review_times
from orm.models import Card
from dependencies.queryParams import get_limit_params
from dependencies.orm import get_session

router = APIRouter(prefix="/review", tags=["复习相关"])


@router.get("/", response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_review(
        session: Session = Depends(get_session),
        limit_params: QueryLimit = Depends(get_limit_params)
):
    """
    获取所有需要复习卡片
    """
    # TODO: 替换uid

    uid = 1
    review_data = query_need_review_card(session, uid=uid, query_params=limit_params)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": review_data
    }


@router.get("/need", response_model=GenericResponse[List[int]])
async def get_need_card_id(session: Session = Depends(get_session),
                           limit_params: QueryLimit = Depends(get_limit_params)):
    """
    获取需要复习的卡片的ID
    """
    # TODO: 替换uid

    uid = 1
    card_id_lst = query_need_review_card(session=session, uid=uid, query_params=limit_params)
    data = []
    for card in card_id_lst:
        data.append(card.id)

    return {
        "status": 1,
        "msg": "获取成功",
        "data": data
    }


@router.get("/{cid}", response_model=GenericResponse[ReadDescriptionCardModel])
async def get_card(
        cid: int,
        session: Session = Depends(get_session),
):
    """
    获取一条需要复习卡片
    """
    # TODO: 替换uid

    uid = 1
    card_data = query_one_data_by_user(session=session, uid=uid, target_id=cid, model_class=Card)
    if not card_data:
        return {
            "status": 0,
            "msg": "获取失败, 该卡片不存在",
            "data": None
        }
    # 必须是需要复习的
    if card_data.is_review_date:
        return {
            "status": 1,
            "msg": "获取成功",
            "data": card_data
        }
    else:
        return {
            "status": 0,
            "msg": "获取失败, 该卡片未到复习时间",
            "data": None
        }


@router.post("/{cid}", response_model=GenericResponse, response_model_exclude_none=True)
async def review_done(
        cid: int,
        session: Session = Depends(get_session),
):
    """
    完成卡片复习
    """
    # TODO: 替换uid

    uid = 1
    card_data = query_one_data_by_user(session=session, uid=uid, target_id=cid, model_class=Card)
    if not card_data:
        return {
            "status": 0,
            "msg": "该卡片不存在",
        }
    # 必须是需要复习的
    if card_data.is_review_date:
        # 可以完成复习

        plan_count = len([i for i in card_data.category.plan.content.split("-") if i])

        old_times = card_data.review_times
        if old_times >= plan_count:
            # times == len 时, 已经全部复习完了
            return {
                "status": 0,
                "msg": "该卡片已复习完毕",
            }
        new_times = old_times + 1
        update_review_times(session=session, cid=cid, review_at=datetime.now(), review_times=new_times)
        return {
            "status": 1,
            "msg": "复习成功",

        }

    else:
        return {
            "status": 0,
            "msg": "该卡片未到复习时间",
        }
