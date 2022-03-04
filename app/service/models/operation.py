"""
默认的操作

1. delete_card
2. create_card
3. review_card

4. delete_category
5. create_category

6. delete_plan
7. create_plan
"""
import orm
from service import orm_models


class Operation(orm.Model):
    tablename = "Operation"
    registry = orm_models
    fields = {
        "id": orm.Integer(primary_key=True),
        "title": orm.String(max_length=32, allow_null=False),  # 操作记录
    }
