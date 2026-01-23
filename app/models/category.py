from tortoise import fields
from tortoise.models import Model


class Category(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="id", on_delete=fields.base.OnDelete.CASCADE)
    plan = fields.ForeignKeyField("models.Plan", related_name="id", on_delete=fields.base.OnDelete.SET_NULL, null=True)
    name = fields.CharField(max_length=32, null=False)
    icon = fields.CharField(max_length=32, null=False)
    color = fields.CharField(max_length=7, null=False)
    is_star = fields.BooleanField(default=False)

    class Meta:
        table = "Category"
