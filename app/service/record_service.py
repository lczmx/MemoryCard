import datetime

from models import Record, Operation
from schemas.analyse import ParamsAnalyseModel
from schemas.user import DBUserModel


async def get_operation_id_by_title(title: str) -> int:
    """
    根据 title 获取操作记录的 ID
    如果不存在则创建
    """
    op = await Operation.filter(title=title).first()
    if not op:
        op = await Operation.create(title=title)
    return op.id


async def get_review_card_record_analyse(title: str, user: DBUserModel):
    """
    获取卡片的操作记录
    :param title: 操作类型标题
    :param user: 当前用户
    :return:
    """
    op_id = await get_operation_id_by_title(title)

    now = datetime.datetime.now()
    today = now.date()
    yesterday = (now - datetime.timedelta(days=1)).date()
    # 查询创建卡片的操作记录
    today_data = await Record.filter(operation_id=op_id, create_at=today, user_id=user.id).all()
    yesterday_data = await Record.filter(operation_id=op_id, create_at=yesterday, user_id=user.id).all()
    return today_data, yesterday_data


async def get_record_between_review_date(user: DBUserModel, date_data: ParamsAnalyseModel):
    """
    根据浏览日期获取卡片操作记录
    :param user: 当前用户
    :param date_data: 日期范围
    :return:
    """
    op_id = await get_operation_id_by_title("review_card")
    return Record.filter(user_id=user.id, create_at__lte=date_data.end_date, create_at__gte=date_data.start_date,
                         operation_id=op_id).order_by("create_at").all()

async def get_record_between_create_date(user: DBUserModel, date_data: ParamsAnalyseModel):
    """
    根据创建日期获取卡片操作记录
    :param user: 当前用户
    :param date_data: 日期范围
    :return:
    """
    op_id = await get_operation_id_by_title("create_card")
    return Record.filter(user_id=user.id, create_at__lte=date_data.end_date, create_at__gte=date_data.start_date,
                         operation_id=op_id).order_by("create_at").all()