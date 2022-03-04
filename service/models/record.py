"""
操作记录表
"""
import datetime
import orm
from service import orm_models
from service.models.user import User
from service.models.operation import Operation


class Record(orm.Model):
    tablename = "Record"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user": orm.ForeignKey(User, on_delete=orm.CASCADE),  # 记录所属用户
        "operation": orm.ForeignKey(Operation, on_delete=orm.CASCADE),  # 该记录的操作类型
        "create_at": orm.Date(default=datetime.date.today, allow_null=False)  # 记录时间
    }
