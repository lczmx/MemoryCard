"""
项目启动时, 执行脚本
"""

from .init_plans import crate_plans
from .init_operation import crate_operation
from .init_docs import crate_docs

crate_plans()
crate_operation()
crate_docs()
