from tortoise import fields
from tortoise.models import Model


class Doc(Model):
    id = fields.IntField(pk=True, name="文档ID")
    title = fields.CharField(max_length=64, null=False, name="文档标题")
    tag = fields.CharField(max_length=128, null=False, name="文档tag")
    content = fields.TextField(null=False, name="文档内容")

    class Meta:
        table = "Doc"
