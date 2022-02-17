from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.orm import get_session
from dependencies.queryParams import get_limit_params
from orm.schemas.generic import QueryLimit, GenericResponse
from orm.schemas.plan import WritePlanModel, ReadPlanModel, ParamsPlanModel
from orm.crud import query_all_data_by_user
from orm.models import Plan

router = APIRouter(prefix="/plans")


@router.get('/', response_model=GenericResponse[List[ReadPlanModel]])
def get_plans(query_limit_params: QueryLimit = Depends(get_limit_params),
              session: Session = Depends(get_session)):
    # TODO: 用真实uid

    uid = 1
    plans = query_all_data_by_user(session=session, model_class=Plan, uid=uid, query_params=query_limit_params,
                                   allow_none=True)
    return {
        "status": 1,
        "msg": "获取成功",
        "data": plans
    }
