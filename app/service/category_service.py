from tortoise.queryset import QuerySet

from models import Category

from schemas.user import DBUserModel


async def get_category_by_user(user: DBUserModel) -> QuerySet[Category]:
    """
    获取用户分类数据
    :param user:
    :return:
    """
    return Category.filter(user=user).all()
