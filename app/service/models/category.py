import orm
from service import orm_models
from service.models.user import User
from service.models.plan import Plan


class Category(orm.Model):
    tablename = "Category"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user": orm.ForeignKey(User, on_delete=orm.CASCADE),
        "plan": orm.ForeignKey(Plan, on_delete=orm.SET_NULL, allow_null=True),
        "name": orm.String(max_length=32, allow_null=False),
        "icon": orm.String(max_length=32, allow_null=False),
        "color": orm.String(max_length=7, allow_null=False),
        "is_star": orm.Boolean(default=False)
    }
