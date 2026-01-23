"""
定义表结构
"""
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True, name="用户ID")
    username = fields.CharField(max_length=32, null=False, unique=True, name="用户名称")
    email = fields.CharField(max_length=128, null=False, unique=True, name="用户邮箱")
    hashed_pwd = fields.CharField(max_length=128, null=False, name="用户密码哈希后的密文")
    phone_number = fields.CharField(max_length=11, null=True, unique=True, name="用户手机号码")
    active = fields.BooleanField(default=True, name="账号是否有效")

    class Meta:
        table = "User"
