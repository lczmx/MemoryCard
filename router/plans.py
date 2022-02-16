from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.orm import get_session
from dependencies.queryPrams import get_limit_prams
from orm.schemas.generic import QueryLimit, GenericResponse
from orm.schemas.plan import WritePlanModel, ReadPlanModel, PramsPlanModel
from orm.crud import query_plan_by_user

router = APIRouter(prefix="/plans")


@router.get('/', response_model=GenericResponse[List[ReadPlanModel]])
def get_plans(query_limit_prams: Dict[str, int] = Depends(get_limit_prams),
              session: Session = Depends(get_session)):
    # TODO: 用真实uid

    uid = 1
    query_prams = QueryLimit(**query_limit_prams)

    plans = query_plan_by_user(session=session, uid=uid, query_prams=query_prams)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": plans
    }
