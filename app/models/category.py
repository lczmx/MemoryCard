from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import OnDelete


class Category(Model):
    id = fields.IntField(pk=True, name="分类ID")
    user = fields.ForeignKeyField("models.User", related_name="categories", on_delete=OnDelete.CASCADE,
                                  description="分类所属用户ID")
    plan = fields.ForeignKeyField("models.Plan", related_name="categories", on_delete=OnDelete.SET_NULL, null=True,
                                  description="计划所属用户ID")
    name = fields.CharField(max_length=32, null=False, name="分类名称")
    icon = fields.CharField(max_length=32, null=False, name="分类图标")
    color = fields.CharField(max_length=7, null=False, name="分类颜色")
    is_star = fields.BooleanField(default=False, name="是否收藏分类")

    class Meta:
        table = "Category"
