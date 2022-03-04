"""
初始化复习曲线数据

"""
import logging

from service.models import Operation


async def crate_operation():
    logging.info("初始化操作数据中...")
    # 没有uid
    data = [
        {"id": 1, "title": "delete_card"}, {"id": 2, "title": "create_card"}, {"id": 3, "title": "review_card"},
        {"id": 4, "title": "delete_category"}, {"id": 5, "title": "create_category"}, {"id": 6, "title": "delete_plan"},
        {"id": 7, "title": "create_plan"}]
    for d in data:
        _, created = await Operation.objects.get_or_create(**d, defaults=d)
        if created:
            logging.info(f"已初始化{d.get('title')}")
        else:
            logging.info("跳过初始化")
