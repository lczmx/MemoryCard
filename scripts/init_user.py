from service.models import User
from uuid import uuid4
from settings import pwd_context
import logging

nologin_user = {"username": "nologin", "email": "nologin@email.com", "active": False}


async def create_user():
    # 初始化内置账号
    logging.info("初始化内置用户中...")
    user, created = await User.objects.get_or_create(
        username="nologin", email="nologin@email.com",
        defaults=dict(**nologin_user, hashed_pwd=pwd_context.hash(str(uuid4()))))
    if created:
        logging.info("已初始化内置账号")
    else:
        logging.info("跳过初始化")
