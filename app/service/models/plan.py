"""
复习曲线表
"""
import orm
from service import orm_models
from service.models.user import User


class Plan(orm.Model):
    tablename = "Plan"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user": orm.ForeignKey(User, on_delete=orm.SET_NULL, allow_null=True),  # 复习曲线所属用户
        "title": orm.String(max_length=32, allow_null=False),  # 复习曲线的名称
        "content": orm.String(max_length=1024, allow_null=False),  # 复习曲线内容, 以空格隔开, 单位s
    }
