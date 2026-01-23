"""
复习曲线表
"""
from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import OnDelete


class Plan(Model):
    id = fields.IntField(pk=True, name="复习计划ID")
    user = fields.ForeignKeyField("models.User", related_name="plans", on_delete=OnDelete.SET_NULL, null=True,
                                  name="复习计划所属用户ID")
    title = fields.CharField(max_length=32, null=False, name="复习曲线的名称")
    content = fields.CharField(max_length=1024, null=False, name="复习曲线内容, 以空格隔开, 单位s")

    class Meta:
        table = "Plan"
