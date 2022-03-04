"""
orm相关的依赖
"""
from service.models import User, Operation
from scripts import init_user


async def get_no_login_user() -> User:
    """
    获取内置用户
    :return:
    """
    return await User.objects.filter(**init_user.nologin_user).first()


def get_operation(pk: int):
    """
    获取内置的操作
    :param pk:
    :return:
    """
    async def inner() -> Operation:
        return await Operation.objects.get(pk=pk)

    return inner
