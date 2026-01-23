"""
操作记录表
"""
import datetime
from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import OnDelete


class Record(Model):
    id = fields.IntField(pk=True, name="操作记录ID")
    user = fields.ForeignKeyField("models.User", related_name="records", on_delete=OnDelete.CASCADE,
                                  name="记录所属用户ID")
    operation = fields.ForeignKeyField("models.Operation", related_name="records", on_delete=OnDelete.CASCADE,
                                       name="记录的操作类型ID")
    create_at = fields.DateField(default=datetime.date.today, null=False, name="创建时间")

    class Meta:
        table = "Record"
