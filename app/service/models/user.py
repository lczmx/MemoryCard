"""
定义表结构
"""

import orm
from service import orm_models


class User(orm.Model):
    tablename = "User"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "username": orm.String(max_length=32, allow_null=False, unique=True),
        "email": orm.Email(max_length=128, allow_null=False, unique=True),
        "hashed_pwd": orm.String(max_length=64, allow_null=False, ),  # 哈希后的密文
        "phone_number": orm.String(max_length=11, allow_null=True, unique=True),
        "active": orm.Boolean(default=True)  # 是否允许登录
    }
