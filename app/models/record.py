"""
操作记录表
"""
import datetime
from tortoise import fields
from tortoise.models import Model


class Record(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="id", on_delete=fields.base.OnDelete.CASCADE)  # 记录所属用户
    operation = fields.ForeignKeyField("models.Operation", related_name="id",
                                       on_delete=fields.base.OnDelete.CASCADE)  # 该记录的操作类型
    create_at = fields.DateField(default=datetime.date.today, null=False)  # 记录时间

    class Meta:
        table = "Category"
