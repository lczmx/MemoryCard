"""
数据库初始化脚本

用于首次创建数据库表结构和内置数据

使用方法:
    python scripts/init_db.py           # 完整初始化
    python scripts/init_db.py --schema # 仅创建表结构
    python scripts/init_db.py --data    # 仅初始化内置数据
"""
import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到 sys.path
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger
from tortoise import Tortoise
import settings
from settings import TORTOISE_ORM, update_operation_data
from models import User, Plan, Operation, Card, Category, Record


async def create_schema():
    """创建数据库表结构"""
    logger.info("正在创建数据库表结构...")

    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        await Tortoise.close_connections()
        logger.success("数据库表结构创建成功!")
        return True
    except Exception as e:
        logger.error(f"创建表结构失败: {e}")
        return False


async def init_builtin_user():
    """初始化内置用户 (nologin)"""
    logger.info("正在初始化内置用户...")

    try:
        from uuid import uuid4
        hashed_pwd = settings.pwd_context.hash(str(uuid4()))

        user, created = await User.get_or_create(
            username="nologin",
            email="nologin@email.com",
            defaults={
                "username": "nologin",
                "email": "nologin@email.com",
                "hashed_pwd": hashed_pwd,
                "active": False
            }
        )

        if created:
            logger.success(f"已创建内置用户: nologin (ID: {user.id})")
        else:
            logger.info("内置用户已存在，跳过创建")

        return user
    except Exception as e:
        logger.error(f"初始化内置用户失败: {e}")
        return None


async def init_builtin_plans(user):
    """初始化内置复习曲线"""
    logger.info("正在初始化内置复习曲线...")

    plans_data = [
        {
            "title": "标准模式",
            "content": "1800-86400-172800-172800-604800-1296000-2592000",
            "description": "适合一般学习，间隔逐渐拉长"
        },
        {
            "title": "单次复习",
            "content": "3600",
            "description": "只复习一次，不再提醒"
        },
        {
            "title": "超级复习",
            "content": "7200-86400-86400-86400-86400-86400-86400-86400-86400-86400-86400",
            "description": "高强度复习，适合重要内容"
        },
        {
            "title": "超级复习(改良版)",
            "content": "1800-86400-172800-172800-604800-1296000-2592000",
            "description": "改良版超级复习，兼顾效果和效率"
        },
        {
            "title": "每日一背",
            "content": "86400",
            "description": "每天复习一次"
        }
    ]

    created_count = 0
    for plan_data in plans_data:
        try:
            plan, created = await Plan.get_or_create(
                user=user,
                title=plan_data["title"],
                defaults={
                    **plan_data,
                    "user": user
                }
            )
            if created:
                created_count += 1
                logger.info(f"已创建复习曲线: {plan.title}")
        except Exception as e:
            logger.warning(f"创建复习曲线 {plan_data['title']} 失败: {e}")

    logger.success(f"复习曲线初始化完成，新增 {created_count} 个")


async def init_builtin_operations():
    """初始化内置操作记录类型"""
    logger.info("正在初始化内置操作类型...")

    operations_data = [
        {"title": "delete_card"},
        {"title": "create_card"},
        {"title": "review_card"},
        {"title": "delete_category"},
        {"title": "create_category"},
        {"title": "delete_plan"},
        {"title": "create_plan"}
    ]

    operation_id_map = {}
    created_count = 0

    for op_data in operations_data:
        try:
            operation, created = await Operation.get_or_create(
                title=op_data["title"],
                defaults=op_data
            )
            operation_id_map[op_data["title"]] = operation.id
            if created:
                created_count += 1
                logger.info(f"已创建操作类型: {operation.title}")
        except Exception as e:
            logger.warning(f"创建操作类型 {op_data['title']} 失败: {e}")

    # 更新全局 OPERATION_DATA
    update_operation_data(operation_id_map)
    logger.success(f"操作类型初始化完成，新增 {created_count} 个")


async def full_init():
    """完整初始化"""
    logger.info("=" * 50)
    logger.info("开始完整数据库初始化")
    logger.info("=" * 50)

    # 1. 创建表结构
    if not await create_schema():
        return False

    # 2. 初始化内置用户
    user = await init_builtin_user()
    if not user:
        logger.error("内置用户初始化失败，终止初始化")
        return False

    # 3. 初始化内置复习曲线
    await init_builtin_plans(user)

    # 4. 初始化内置操作类型
    await init_builtin_operations()

    logger.success("=" * 50)
    logger.success("数据库初始化完成!")
    logger.success("=" * 50)
    return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="数据库初始化工具")
    parser.add_argument("--schema", action="store_true", help="仅创建表结构")
    parser.add_argument("--data", action="store_true", help="仅初始化内置数据")
    args = parser.parse_args()

    if args.schema:
        asyncio.run(create_schema())
    elif args.data:
        asyncio.run(init_builtin_user())
        asyncio.run(init_builtin_plans())
        asyncio.run(init_builtin_operations())
    else:
        asyncio.run(full_init())


if __name__ == "__main__":
    main()
