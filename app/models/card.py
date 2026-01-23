from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import OnDelete


class Card(Model):
    id = fields.IntField(pk=True, description="卡片ID")
    user = fields.ForeignKeyField("models.User", related_name="cards", on_delete=OnDelete.CASCADE,
                                  description="卡片所属用户ID")
    category = fields.ForeignKeyField("models.Category", related_name="cards", on_delete=OnDelete.CASCADE,
                                      description="卡片所属类别ID")
    title = fields.CharField(max_length=32, null=False, description="卡片标题")
    created_at = fields.DatetimeField(auto_now_add=True, null=False, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, null=False, description="更新时间")
    review_at = fields.DatetimeField(auto_now=True, null=False, description="卡片这次复习时间")
    review_times = fields.IntField(default=0, null=False, description="卡片这次复习的次数")
    summary = fields.CharField(max_length=1024, null=False, allow_blank=True, default="",
                               description="卡片的概要信息(提示信息)")
    description = fields.TextField(null=False, description="卡片的详细内容")
    is_star = fields.BooleanField(default=False, description="卡片是否收藏")

    class Meta:
        table = "Card"
