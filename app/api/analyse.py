"""
记忆分析页面
"""
from typing import List

from fastapi import APIRouter, Depends

from dependencies.auth import jwt_get_current_user
from schemas.analyse import ParamsAnalyseModel, ReadAnalyseModel, SummaryAnalyseModel
from schemas.generic import GenericResponse
from schemas.user import DBUserModel
from service import record_service, category_service

router = APIRouter(prefix="/analyse", tags=["分析相关"])


@router.get("/", response_model=GenericResponse[SummaryAnalyseModel])
async def get_summary_analyse_data(user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取数据统计的概览数据
    """
    data = {
        "review": {"today": 0, "incr": 0},
        "create": {"today": 0, "incr": 0},
        "category_count": 0}

    # 查询创建卡片的操作记录
    today_recode_review_data, yesterday_recode_review_data = await record_service.get_review_card_record_analyse(
        title="review_card", user=user)
    data["review"]["today"] = len(today_recode_review_data)
    # ## 同比增加 = 今日 - 昨日
    data["review"]["incr"] = len(today_recode_review_data) - len(yesterday_recode_review_data)

    today_recode_create_data, yesterday_recode_create_data = await record_service.get_review_card_record_analyse(
        title="create_card", user=user)
    data["create"]["today"] = len(today_recode_create_data)
    # ## 同比增加 = 今日 - 昨日
    data["create"]["incr"] = len(today_recode_create_data) - len(yesterday_recode_create_data)

    # TODO: 使用count
    category_data = await category_service.get_category_by_user(user=user)
    category_count = await category_data.count()
    data["category_count"] = category_count

    return {"status": 1, "msg": "获取成功", "data": data}


@router.post("/review", response_model=GenericResponse[List[ReadAnalyseModel]])
async def analyse_review(data: ParamsAnalyseModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取累计复习次数数据
    """
    result = await record_service.get_record_between_review_date(user=user, date_data=data)
    date_and_count = {}  # key: date  value: count
    for r in result:
        date_and_count[r.create_at] = date_and_count.setdefault(r.create_at, 0) + 1

    sorted_date = sorted(date_and_count, key=lambda k: k)
    temp = []
    for d in sorted_date:
        temp.append({"date": d, "count": date_and_count[d]})

    return {"status": 1, "msg": "获取成功", "data": temp}


@router.post("/create", response_model=GenericResponse[List[ReadAnalyseModel]])
async def analyse_create(data: ParamsAnalyseModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取累计创建卡片次数数据
    """
    result = await record_service.get_record_between_create_date(user=user, date_data=data)

    date_and_count = {}  # key: date  value: count
    for r in result:
        date_and_count[r.create_at] = date_and_count.setdefault(r.create_at, 0) + 1

    sorted_date = sorted(date_and_count, key=lambda k: k)
    temp = []
    for d in sorted_date:
        temp.append({"date": d, "count": date_and_count[d]})

    return {"status": 1, "msg": "获取成功", "data": temp}
