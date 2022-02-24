"""
获取卡片数据
"""
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from orm.schemas.card import ParamsCardModel, ReadSummaryCardModel, \
    ReadDescriptionCardModel, WriteCardModel, StarModel, BatchCard
from orm.schemas.generic import GenericResponse, QueryLimit

from orm.crud import save_one_to_db, query_all_data_by_user, toggle_star_status, \
    query_one_data_by_user, update_data, delete_data_by_user
from orm.models import Card
from dependencies.orm import get_session
from dependencies.queryParams import get_limit_params

router = APIRouter(prefix="/cards", tags=["卡片相关"])


@router.get("/",
            response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_cards(limit_params: QueryLimit = Depends(get_limit_params), session: Session = Depends(get_session)):
    """
    获取多个卡片
    """
    uid = 1

    card_data = query_all_data_by_user(session, uid=uid, model_class=Card, query_params=limit_params)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": card_data
    }


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=GenericResponse[ReadDescriptionCardModel])
async def create_card(card_data: ParamsCardModel, session: Session = Depends(get_session)):
    """
    创建卡片
    """
    # TODO: 修改uid
    uid = 1
    data = WriteCardModel(uid=uid, **card_data.dict())
    card_obj = save_one_to_db(session=session, model_class=Card, data=data)

    return {
        "status": 1,
        "msg": "创建成功",
        "data": card_obj
    }


@router.post("/batch-star", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_star_card(batch_data: BatchCard, session: Session = Depends(get_session)):
    """
    批量星标卡片
    """
    # TODO: 修改uid
    uid = 1
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


@router.delete("/batch-delete", response_model=GenericResponse, response_model_exclude_unset=True)
async def batch_delete_card(batch_data: BatchCard, session: Session = Depends(get_session)):
    """
    批量删除卡片
    """
    # TODO: 修改uid
    uid = 1
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
        batch_status["success_count"] += 1
    return {
        "status": 1,
        "msg": f"成功删除卡片数: {batch_status.get('success_count')}, 失败删除卡片数: {batch_status.get('fail_count')}",
    }


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, session: Session = Depends(get_session)):
    """
    切换分类星标状态
    """
    uid = 1
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
async def retrieve_card(cid: int, session: Session = Depends(get_session)):
    """
    获取一条卡片的数据
    """
    # TODO
    uid = 1
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
async def retrieve_card(cid: int, data: ParamsCardModel, session: Session = Depends(get_session)):
    """
    修改一条卡片的数据
    """
    # TODO
    uid = 1

    card_data = update_data(session=session, uid=uid, target_id=cid, model_class=Card, data=data)
    if not card_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="不存在的卡片")

    return {
        "status": 1,
        "msg": "更新成功",
        "data": card_data

    }


@router.delete("/{cid}", response_model=GenericResponse, response_model_exclude_unset=True)
async def retrieve_card(cid: int, session: Session = Depends(get_session)):
    """
    删除一条卡片的数据
    """
    # TODO
    uid = 1
    rowcount = delete_data_by_user(session=session, uid=uid, target_id=cid, model_class=Card)
    # rowcount = 0 时
    if not rowcount:
        return {
            "status": 0,
            "msg": "删除失败",
        }

    return {
        "status": 1,
        "msg": "删除成功",

    }
