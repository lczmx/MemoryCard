import datetime

from models import Record
from schemas.analyse import ParamsAnalyseModel
from schemas.user import DBUserModel
from settings import OPERATION_DATA


async def get_review_card_record_analyse(operation: str, user: DBUserModel):
    """
    获取卡片的操作记录
    :param operation: OPERATION_DATA
    :param user: 当前用户
    :return:
    """

    now = datetime.datetime.now()
    today = now.date()
    yesterday = (now - datetime.timedelta(days=1)).date()
    # TODO: 能否使用 count & group_by ?
    # 查询创建卡片的操作记录
    today_data = await Record.filter(operation=operation, create_at=today, user=user).all()
    yesterday_data = await Record.filter(operation=operation, create_at=yesterday, user=user).all()
    return today_data, yesterday_data


async def get_record_between_review_date(user: DBUserModel, date_data: ParamsAnalyseModel):
    """
    根据浏览日期获取卡片操作记录
    :param user: 当前用户
    :param date_data: 日期范围
    :return:
    """
    return  Record.filter(user=user, create_at__lte=date_data.end_date, create_at__gte=date_data.start_date,
                                         operation=OPERATION_DATA["review_card"]).order_by("create_at").all()

async def get_record_between_create_date(user: DBUserModel, date_data: ParamsAnalyseModel):
    """
    根据创建日期获取卡片操作记录
    :param user: 当前用户
    :param date_data: 日期范围
    :return:
    """

    return  Record.filter(user=user, create_at__lte=date_data.end_date, create_at__gte=date_data.start_date,
                                         operation=OPERATION_DATA["create_card"]).order_by("create_at").all()