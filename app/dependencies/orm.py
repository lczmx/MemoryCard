"""
orm相关的依赖
"""
from models import User, Operation
from scripts import init_user


async def get_no_login_user() -> User:
    """
    获取内置用户
    """
    return await User.filter(**init_user.nologin_user).first()


async def get_or_create_operation(title: str) -> Operation:
    """
    获取或创建操作记录
    如果记录不存在，自动创建
    """
    operation = await Operation.filter(title=title).first()
    if not operation:
        operation = await Operation.create(title=title)
    return operation


def get_operation(title: str):
    """
    获取内置的操作记录（通过 title 查找）
    如果记录不存在，自动创建
    """
    async def inner() -> Operation:
        return await get_or_create_operation(title)

    return inner
