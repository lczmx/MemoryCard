"""
定义表结构
"""
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, null=False, unique=True)
    email = fields.CharField(max_length=128, null=False, unique=True)
    hashed_pwd = fields.CharField(max_length=128, null=False, )  # 哈希后的密文
    phone_number = fields.CharField(max_length=11, null=True, unique=True)
    active = fields.BooleanField(default=True)  # 是否允许登录

    class Meta:
        table = "User"
