"""
复习曲线表
"""
from tortoise import fields
from tortoise.models import Model


class Plan(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="id", on_delete=fields.base.OnDelete.SET_NULL, null=True)
    title = fields.CharField(max_length=32, null=False)  # 复习曲线的名称
    content = fields.CharField(max_length=1024, null=False)  # 复习曲线内容, 以空格隔开, 单位s

    class Meta:
        table = "Plan"
