"""
初始化复习曲线数据
"""
import logging

from service.models import Plan
from service.models import User
from scripts import init_user


async def crate_plans():
    logging.info("初始化复习曲线数据中...")
    # 没有uid
    data = [
        {
            "title": "标准模式",
            "content": "1800-86400-172800-172800-604800-1296000-2592000"
        },
        {
            "title": "单次复习",
            "content": "3600"
        },
        {
            "title": "超级复习",
            "content": "7200-86400-86400-86400-86400-86400-86400-86400-86400-86400-86400"
        },
        {
            "title": "超级复习(改良版)",
            "content": "1800-86400-172800-172800-604800-1296000-2592000"
        }
    ]
    # 跳过已经有的
    nologin_user = await User.objects.filter(**init_user.nologin_user).first()
    for d in data:
        _, created = await Plan.objects.get_or_create(user=nologin_user, **d, defaults=dict(**d, user=nologin_user))
        if created:
            logging.info(f"已初始化{d.get('title')}")
        else:
            logging.info("跳过初始化")
