from tortoise import fields
from tortoise.models import Model


class Doc(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64, null=False)  # 文档标题
    tag = fields.CharField(max_length=128, null=False)  # 文档tag
    content = fields.TextField(null=False)  # 文档内容

    class Meta:
        table = "Doc"
