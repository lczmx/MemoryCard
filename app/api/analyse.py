"""
记忆分析页面
"""
import datetime
from typing import List

from fastapi import APIRouter, Depends

import settings
from service.schemas.analyse import ParamsAnalyseModel, ReadAnalyseModel, SummaryAnalyseModel
from service.schemas.generic import GenericResponse
from service.schemas.user import DBUserModel
from service.models import Record, Category
from dependencies.auth import jwt_get_current_user

router = APIRouter(prefix="/analyse", tags=["分析相关"])


@router.get("/", response_model=GenericResponse[SummaryAnalyseModel])
async def get_summary_analyse_data(user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取数据统计的概览数据
    """
    temp = {
        "review": {"today": 0, "incr": 0},
        "create": {"today": 0, "incr": 0},
        "category_count": 0}
    now = datetime.datetime.now()
    today = now.date()
    yesterday = (now - datetime.timedelta(days=1)).date()
    # TODO: 能否使用 count & group_by ?
    # 查询创建卡片的操作记录
    today_recode_review_data = await Record.objects.filter(operation=settings.OPERATION_DATA["review_card"],
                                                           create_at=today, user=user).all()
    yesterday_recode_review_data = await Record.objects.filter(operation=settings.OPERATION_DATA["review_card"],
                                                               create_at=yesterday, user=user).all()
    temp["review"]["today"] = len(today_recode_review_data)
    # ## 同比增加 = 今日 - 昨日
    temp["review"]["incr"] = len(today_recode_review_data) - len(yesterday_recode_review_data)

    today_recode_create_data = await Record.objects.filter(operation=settings.OPERATION_DATA["create_card"],
                                                           create_at=today, user=user).all()
    yesterday_recode_create_data = await Record.objects.filter(operation=settings.OPERATION_DATA["create_card"],
                                                               create_at=yesterday, user=user).all()

    temp["create"]["today"] = len(today_recode_create_data)
    # ## 同比增加 = 今日 - 昨日
    temp["create"]["incr"] = len(today_recode_create_data) - len(yesterday_recode_create_data)

    # TODO: 使用count
    category_data = await Category.objects.filter(user=user).all()

    if category_data:
        temp["category_count"] = len(category_data)

    return {"status": 1, "msg": "获取成功", "data": temp}


@router.post("/review", response_model=GenericResponse[List[ReadAnalyseModel]])
async def analyse_review(data: ParamsAnalyseModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    获取累计复习次数数据
    """

    result = await Record.objects.filter(user=user, create_at__lte=data.end_date, create_at__gte=data.start_date,
                                         operation=settings.OPERATION_DATA["review_card"]).order_by("create_at").all()

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
    # ###### 同上面的函数
    result = await Record.objects.filter(user=user, create_at__lte=data.end_date, create_at__gte=data.start_date,
                                         operation=settings.OPERATION_DATA["create_card"]).order_by("create_at").all()

    date_and_count = {}  # key: date  value: count
    for r in result:
        date_and_count[r.create_at] = date_and_count.setdefault(r.create_at, 0) + 1

    sorted_date = sorted(date_and_count, key=lambda k: k)
    temp = []
    for d in sorted_date:
        temp.append({"date": d, "count": date_and_count[d]})

    return {"status": 1, "msg": "获取成功", "data": temp}
