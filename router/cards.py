"""
获取卡片数据
"""
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter, status, Depends
from orm.schemas.card import ParamsCardModel, ReadSummaryCardModel, ReadDescriptionCardModel, WriteCardModel, StarModel
from orm.schemas.generic import GenericResponse, QueryLimit

from orm.crud import save_one_to_db, query_all_data_by_user, toggle_star_status
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


@router.post("/{cid}/star", response_model=GenericResponse[StarModel])
async def toggle_star(cid: int, star_status: StarModel, session: Session = Depends(get_session)):
    """
    切换分类星标状态
    """
    now_status = toggle_star_status(session, model_class=Card, target_id=cid, star_status=star_status.is_star)
    msg = "切换成功" if star_status.is_star != now_status else "切换失败"
    return {
        "status": 1,
        "msg": msg,
        "data": {
            "is_star": now_status
        }

    }
