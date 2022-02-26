from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.orm import get_session
from dependencies.queryParams import get_limit_params
from orm.schemas.generic import QueryLimit, GenericResponse
from orm.schemas.plan import WritePlanModel, ReadPlanModel, ParamsPlanModel
from orm.crud import query_all_data_by_user, save_one_to_db, query_one_data_by_user, update_data, delete_data_by_user
from orm.models import Plan

router = APIRouter(prefix="/plans", tags=["复习计划相关"])


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


@router.post('/', response_model=GenericResponse[ReadPlanModel])
def create_plan(plan_data: ParamsPlanModel, session: Session = Depends(get_session)):
    """
    创建复习曲线
    """
    # TODO: 用真实uid
    uid = 1
    data = WritePlanModel(**plan_data.dict(), uid=uid)
    plan = save_one_to_db(session=session, model_class=Plan, data=data)
    return {
        "status": 1,
        "msg": "创建成功",
        "data": plan
    }


@router.get('/{pid}', response_model=GenericResponse[ReadPlanModel])
def get_plan(pid: int, session: Session = Depends(get_session)):
    """
    获取一条复习曲线数据
    """
    # TODO: 用真实uid
    uid = 1
    plan = query_one_data_by_user(session=session, uid=uid, target_id=pid, model_class=Plan)
    if not plan:
        return {
            "status": 0,
            "msg": "没有找到对应资源",
            "data": plan
        }

    return {
        "status": 1,
        "msg": "获取成功",
        "data": plan
    }


@router.post('/{pid}', response_model=GenericResponse[ReadPlanModel])
def update_plan(pid: int, plan_data: ParamsPlanModel, session: Session = Depends(get_session)):
    """
    获取一条复习曲线数据
    """
    # TODO: 用真实uid
    uid = 1
    plan = update_data(session=session, uid=uid, target_id=pid, model_class=Plan, data=plan_data)
    if not plan:
        return {
            "status": 0,
            "msg": "修改失败",
            "data": plan
        }
    return {
        "status": 1,
        "msg": "修改成功",
        "data": plan
    }


@router.delete('/{pid}', response_model=GenericResponse, response_model_exclude_unset=True)
def delete_plan(pid: int, session: Session = Depends(get_session)):
    """
    删除一天复习计划
    """
    # TODO: 用真实uid
    uid = 1
    plan = delete_data_by_user(session=session, uid=uid, target_id=pid, model_class=Plan)
    if not plan:
        return {
            "status": 0,
            "msg": "删除失败",
        }
    return {
        "status": 1,
        "msg": "删除成功",
    }
