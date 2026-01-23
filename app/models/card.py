from tortoise import fields
from tortoise.models import Model


class Card(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="id", on_delete=fields.base.OnDelete.CASCADE)  # 卡片所属用户
    category = fields.ForeignKeyField("models.Category", related_name="id",
                                      on_delete=fields.base.OnDelete.CASCADE)  # 卡片所属类别
    title = fields.CharField(max_length=32, null=False)
    created_at = fields.DatetimeField(auto_now_add=True, null=False)  # 创建时间
    updated_at = fields.DatetimeField(auto_now=True, null=False)  # 更新时间
    review_at = fields.DatetimeField(auto_now=True, null=False)  # 卡片这次复习时间
    review_times = fields.IntField(default=0, null=False)  # 卡片这次复习的次数
    summary = fields.CharField(max_length=1024, null=False, allow_blank=True, default="")  # 卡片的概要信息(提示信息)
    description = fields.TextField(null=False)  # 卡片的详细内容
    is_star = fields.BooleanField(default=False)

    class Meta:
        table = "Card"
