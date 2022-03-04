"""
一些与数据库相关的工具
"""
import typing
import datetime

from service.models import Plan, Card


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
    return res_date <= datetime.datetime.now()


async def get_card_plan(card: typing.Any) -> typing.Any:
    """
    获取卡片的复习曲线
    :param card:
    :return:
    """
    await card.category.load()
    return await Plan.objects.get(pk=card.category.plan.pk)


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
        await card.update(review_times=0, review_at=datetime.datetime.now())
        review_count += 1
    return review_count
