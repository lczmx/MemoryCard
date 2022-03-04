import orm
from service import orm_models


class Doc(orm.Model):
    tablename = "Doc"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "title": orm.String(max_length=64, allow_null=False),  # 文档标题
        "tag": orm.String(max_length=128, allow_null=False),  # 文档tag
        "content": orm.Text(allow_null=False),  # 文档内容
    }
