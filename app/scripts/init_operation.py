"""
初始化操作数据

"""
import logging

from models import Operation
from settings import update_operation_data


async def crate_operation():
    logging.info("初始化操作数据中...")
    data = [
        {"title": "delete_card"},
        {"title": "create_card"},
        {"title": "review_card"},
        {"title": "delete_category"},
        {"title": "create_category"},
        {"title": "delete_plan"},
        {"title": "create_plan"}
    ]
    operation_id_map = {}
    for d in data:
        op, created = await Operation.get_or_create(**d, defaults=d)
        operation_id_map[d["title"]] = op.id
        if created:
            logging.info(f"已初始化{d.get('title')}")
        else:
            logging.info("跳过初始化")
    # 更新全局 OPERATION_DATA
    update_operation_data(operation_id_map)
    logging.info("操作数据初始化完成")
