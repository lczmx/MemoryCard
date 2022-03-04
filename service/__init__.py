"""
初始化orm配置
"""
import databases
import orm
from settings import ASYNC_SQLALCHEMY_DATABASE_URL

orm_database = databases.Database(ASYNC_SQLALCHEMY_DATABASE_URL)
orm_models = orm.ModelRegistry(database=orm_database)
metadata = orm_models.metadata


async def create_all():
    # 创建数据库
    await orm_models.create_all()


async def drop_all():
    await orm_models.drop_all()
