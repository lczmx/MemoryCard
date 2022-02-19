"""
获取卡片数据
"""
from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter, status, Depends
from orm.schemas.card import ParamsCardModel, ReadSummaryCardModel, ReadDescriptionCardModel, WriteCardModel
from orm.schemas.generic import GenericResponse

from orm.crud import save_one_to_db
from orm.models import Card
from dependencies.orm import get_session

router = APIRouter(prefix="/cards", tags=["卡片相关"])


@router.get("/")
async def get_cards():
    """
    获取多个卡片
    """
    return {"index": "cards"}


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
