"""
初始化复习曲线数据

"""
import logging

from orm import SessionLocal
from orm.models import Plan
from orm.crud import save_all_to_db, query_plan_title_by_user
from orm.schemas.plan import WritePlanModel
from orm.schemas.generic import QueryLimit


def crate_plans():
    logging.info("初始化复习曲线数据中...")
    # 没有uid
    data = [
        {
            "title": "标准模式",
            "content": "1800-86400-172800-172800-604800-1296000-2592000"
        }, {
            "title": "单次复习",
            "content": "3600"
        }, {
            "title": "超级复习",
            "content": "7200-86400-86400-86400-86400-86400-86400-86400-86400-86400-86400"
        }, {
            "title": "超级复习(改良版)",
            "content": "1800-86400-172800-172800-604800-1296000-2592000"
        },
    ]

    with SessionLocal() as session:
        # 跳过已经有的
        exists_plans = query_plan_title_by_user(session=session, uid=None, query_prams=QueryLimit())
        plans = [WritePlanModel(**d) for d in data if d.get("title") not in exists_plans]
        if plans:
            # 正式初始化
            save_all_to_db(session=session, model_class=Plan, data_list=plans)
            logging.info("初始化完毕")
        else:
            # 已经初始化过了
            logging.info("已经初始化了")
