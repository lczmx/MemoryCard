"""
项目启动时, 执行脚本
"""

from .init_plans import crate_plans
from .init_operation import crate_operation
from .init_docs import crate_docs
from .init_user import create_user


async def start_init():
    await crate_plans()
    await crate_operation()
    await crate_docs()
    await create_user()
