"""
复习
"""
from typing import List

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from orm.schemas.generic import QueryLimit, GenericResponse
from orm.schemas.card import ReadSummaryCardModel
from orm.crud import query_need_review_card
from dependencies.queryParams import get_limit_params
from dependencies.orm import get_session

router = APIRouter(prefix="/review", tags=["复习相关"])


@router.get("/",response_model=GenericResponse[List[ReadSummaryCardModel]])
async def get_review(
    session: Session= Depends(get_session),
    limit_params:QueryLimit=Depends(get_limit_params)
):
    """
    获取所有需要复习卡片
    """
    # TODO: 替换uid

    uid = 1
    review_data = query_need_review_card(session, uid=uid,  query_params=limit_params)
    print(review_data)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": review_data
    }
