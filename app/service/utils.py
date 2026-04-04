"""
一些与数据库相关的工具
"""
import typing
import datetime
from zoneinfo import ZoneInfo

from models import Card

# 项目配置的时区
PROJECT_TIMEZONE = ZoneInfo("Asia/Shanghai")


def get_now_with_timezone() -> datetime.datetime:
    """
    获取当前时间（带时区信息）
    :return:
    """
    return datetime.datetime.now(PROJECT_TIMEZONE)


async def use_need_review_cards(cards: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """
    筛选可以复习的卡片
    :param cards:
    :return:
    """
    temp = []
    for card in cards:
        if await card_can_review(card):
            temp.append(card)
    return temp


async def card_can_review(card: typing.Any):
    """
    卡片是否可以复习
    :return:
    """
    plan = await get_card_plan(card)
    plan_sec = plan.content.split('-')
    if card.review_times >= len(plan_sec):
        return False
    sec = int(plan_sec[card.review_times])
    res_date = card.review_at + datetime.timedelta(seconds=sec)
    return res_date <= get_now_with_timezone()


async def get_card_plan(card: typing.Any) -> typing.Any:
    """
    获取卡片的复习曲线
    :param card:
    :return:
    """
    # 使用 fetch_related 预加载嵌套关系 category__plan
    await card.fetch_related("category__plan")
    return card.category.plan


async def card_can_review_by_date(card: typing.Any, query_date: datetime.date) -> bool:
    """
    判断卡片在指定日期内是否可以复习
    :param card:
    :param query_date:
    :return:
    """
    plan = await get_card_plan(card)
    plan_sec = plan.content.split('-')
    if card.review_times >= len(plan_sec):
        return False
    sec = int(plan_sec[card.review_times])
    res_date = card.review_at + datetime.timedelta(seconds=sec)
    return query_date == res_date.date()


async def reset_card_review(cards: typing.List[Card]) -> int:
    """
    处置卡片复习
    :return:
    """
    review_count = 0
    for card in cards:
        card.review_times = 0
        card.review_at = get_now_with_timezone()
        await card.save()
        review_count += 1
    return review_count
