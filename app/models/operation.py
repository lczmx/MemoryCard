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
from tortoise import fields
from tortoise.models import Model


class Operation(Model):
    id = fields.IntField(pk=True, name="操作ID")
    title = fields.CharField(max_length=32, name="操作说明")

    class Meta:
        table = "Operation"
