"""
初始化复习曲线数据

"""
import logging

from orm import SessionLocal
from orm.models import Operation
from orm.crud import save_all_to_db, query_operation_title
from orm.schemas.analyse import WriteOperationModel


def crate_operation():
    logging.info("初始化 操作数据 中...")
    # 没有uid
    data = [
        {"id": 1, "title": "delete_card"}, {"id": 2, "title": "create_card"}, {"id": 3, "title": "review_card"},
        {"id": 4, "title": "delete_category"}, {"id": 5, "title": "create_category"}, {"id": 6, "title": "delete_plan"},
        {"id": 7, "title": "create_plan"}]

    with SessionLocal() as session:
        # 跳过已经有的
        exists_plans = query_operation_title(session=session)
        operation = [WriteOperationModel(**d) for d in data if d.get("title") not in exists_plans]
        if operation:
            # 正式初始化
            save_all_to_db(session=session, model_class=Operation, data_list=operation)
            logging.info("初始化完毕")
        else:
            # 已经初始化过了
            logging.info("已经初始化了")
