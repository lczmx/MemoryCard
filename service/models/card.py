import datetime

import orm
from service import orm_models
from service.models.user import User
from service.models.category import Category


class Card(orm.Model):
    tablename = "Card"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user": orm.ForeignKey(User, on_delete=orm.CASCADE),  # 卡片所属用户
        "category": orm.ForeignKey(Category, on_delete=orm.CASCADE),  # 卡片所属类别
        "title": orm.String(max_length=32, allow_null=False),
        "created_at": orm.DateTime(default=datetime.datetime.now, allow_null=False),  # 创建时间
        "updated_at": orm.DateTime(default=datetime.datetime.now, allow_null=False),  # 更新时间
        "review_at": orm.DateTime(default=datetime.datetime.now, allow_null=False),  # 卡片这次复习时间
        "review_times": orm.Integer(default=0, allow_null=False),  # 卡片这次复习的次数
        "summary": orm.String(max_length=1024, allow_null=False, allow_blank=True, default=""),  # 卡片的概要信息(提示信息)
        "description": orm.Text(allow_null=False),  # 卡片的详细内容
        "is_star": orm.Boolean(default=False),
    }
