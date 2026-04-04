#!/usr/bin/env python3
"""
数据库迁移管理脚本

支持的功能:
- 初始化数据库 (init)
- 生成迁移 (generate)
- 应用迁移 (migrate)
- 回滚迁移 (rollback)
- 重置数据库 (reset) - 危险操作!
- 查看迁移状态 (status)

使用方法:
    python scripts/migrate.py init           # 初始化数据库
    python scripts/migrate.py generate       # 生成迁移
    python scripts/migrate.py migrate        # 应用迁移
    python scripts/migrate.py rollback        # 回滚上一次迁移
    python scripts/migrate.py status         # 查看迁移状态
    python scripts/migrate.py reset          # 重置数据库 (会丢失数据!)
    python scripts/migrate.py upgrade        # 完整升级 (init + migrate)

多数据源支持:
    DB_TYPE=sqlite python scripts/migrate.py init
    DB_TYPE=mysql python scripts/migrate.py migrate
"""
import sys
import os
import argparse
import asyncio
from pathlib import Path

# 添加项目根目录到 sys.path
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger
from tortoise import Tortoise
from aerich import Command
from tortoise.exceptions import OperationalError


def setup_logging():
    """配置日志"""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )


async def init_db() -> bool:
    """初始化数据库 - 创建所有表"""
    try:
        from settings import TORTOISE_ORM
        logger.info("正在初始化数据库...")

        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        await Tortoise.close_connections()

        logger.success("数据库初始化成功!")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False


async def run_aerich_command(command_name: str, *args) -> bool:
    """运行 Aerich 命令"""
    from settings import TORTOISE_ORM
    from settings import settings

    try:
        app = "models"
        location = str(PROJECT_ROOT / "migrations")

        await Tortoise.init(config=TORTOISE_ORM)
        command = Command(Tortoise.apps[app], location)

        if command_name == "init":
            logger.info("正在初始化 Aerich 迁移环境...")
            await command.init()
            logger.success("Aerich 初始化完成!")

        elif command_name == "migrate":
            logger.info("正在生成迁移文件...")
            await command.migrate(*args)
            logger.success("迁移文件生成成功!")

        elif command_name == "upgrade":
            logger.info("正在应用迁移...")
            await command.upgrade(*args)
            logger.success("迁移应用成功!")

        elif command_name == "downgrade":
            logger.info("正在回滚迁移...")
            await command.downgrade(*args)
            logger.success("回滚成功!")

        elif command_name == "history":
            logger.info("正在获取迁移历史...")
            await command.history()
            logger.success("迁移历史获取成功!")

        await Tortoise.close_connections()
        return True

    except OperationalError as e:
        logger.error(f"数据库连接错误: {e}")
        logger.info("请确保数据库已启动，或使用 'init' 命令初始化数据库")
        return False
    except Exception as e:
        logger.error(f"Aerich 命令执行失败: {e}")
        return False


async def check_db_connection() -> bool:
    """检查数据库连接"""
    from settings import TORTOISE_ORM

    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        await Tortoise.close_connections()
        return True
    except Exception:
        return False


async def full_upgrade() -> bool:
    """完整升级流程: 初始化 + 迁移"""
    logger.info("=" * 50)
    logger.info("开始完整数据库升级")
    logger.info("=" * 50)

    # 步骤1: 初始化数据库
    if not await init_db():
        return False

    # 步骤2: 初始化 Aerich
    if not await run_aerich_command("init"):
        logger.warning("Aerich 可能已经初始化过，跳过...")

    # 步骤3: 生成并应用迁移
    try:
        from settings import TORTOISE_ORM
        from tortoise import Tortoise
        from aerich import Command

        app = "models"
        location = str(PROJECT_ROOT / "migrations")

        await Tortoise.init(config=TORTOISE_ORM)
        command = Command(Tortoise.apps[app], location)

        logger.info("正在生成迁移文件...")
        await command.migrate()

        logger.info("正在应用迁移...")
        await command.upgrade()

        await Tortoise.close_connections()
        logger.success("完整升级完成!")
        return True

    except Exception as e:
        logger.error(f"升级过程中出错: {e}")
        return False


async def reset_database() -> bool:
    """重置数据库 - 危险操作!"""
    from settings import TORTOISE_ORM

    logger.warning("=" * 50)
    logger.warning("警告: 这将删除所有数据!")
    logger.warning("=" * 50)

    confirm = input("确定要继续吗? 输入 'YES' 确认: ")
    if confirm != "YES":
        logger.info("已取消操作")
        return False

    try:
        # 删除迁移目录
        migrations_dir = PROJECT_ROOT / "migrations" / "models"
        for f in migrations_dir.glob("*.py"):
            if f.name != "__init__.py":
                f.unlink()
                logger.info(f"已删除: {f.name}")

        # 删除数据库文件 (如果是 SQLite)
        db_file = PROJECT_ROOT / settings.db_file
        if db_file.exists():
            db_file.unlink()
            logger.info(f"已删除数据库文件: {db_file}")

        # 重新初始化
        return await full_upgrade()

    except Exception as e:
        logger.error(f"重置失败: {e}")
        return False


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="MemoryCard 数据库迁移管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s init                    # 初始化数据库表结构
  %(prog)s generate                # 生成迁移文件
  %(prog)s migrate                 # 应用迁移
  %(prog)s upgrade                 # 完整升级 (init + migrate)
  %(prog)s rollback                # 回滚上一次迁移
  %(prog)s status                  # 查看迁移状态
  %(prog)s reset                   # 重置数据库 (危险!)

环境变量:
  DB_TYPE=pgsql|mysql|sqlite      指定数据库类型
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用的命令")

    # init 命令
    subparsers.add_parser("init", help="初始化数据库表结构")

    # generate 命令
    subparsers.add_parser("generate", help="生成迁移文件")

    # migrate 命令
    migrate_parser = subparsers.add_parser("migrate", help="应用迁移")
    migrate_parser.add_argument("-t", "--target", type=str, default=None,
                                help="指定目标版本")

    # upgrade 命令
    subparsers.add_parser("upgrade", help="完整升级 (init + migrate)")

    # rollback 命令
    rollback_parser = subparsers.add_parser("rollback", help="回滚迁移")
    rollback_parser.add_argument("-t", "--target", type=str, default="-1",
                                 help="回滚步数 (默认: -1)")

    # status 命令
    subparsers.add_parser("status", help="查看迁移状态")

    # reset 命令
    subparsers.add_parser("reset", help="重置数据库 (危险!)")

    return parser.parse_args()


async def main():
    """主函数"""
    setup_logging()

    args = parse_args()

    if not args.command:
        logger.error("请指定命令，使用 --help 查看帮助")
        sys.exit(1)

    logger.info(f"数据库类型: {os.getenv('DB_TYPE', 'pgsql')}")
    logger.info(f"项目路径: {PROJECT_ROOT}")

    success = False

    if args.command == "init":
        success = await init_db()

    elif args.command == "generate":
        success = await run_aerich_command("init")
        if success:
            success = await run_aerich_command("migrate")

    elif args.command == "migrate":
        target = getattr(args, "target", None)
        success = await run_aerich_command("upgrade", [target] if target else None)

    elif args.command == "upgrade":
        success = await full_upgrade()

    elif args.command == "rollback":
        target = getattr(args, "target", "-1")
        success = await run_aerich_command("downgrade", [target])

    elif args.command == "status":
        success = await run_aerich_command("history")

    elif args.command == "reset":
        success = await reset_database()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

