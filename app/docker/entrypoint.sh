#!/bin/bash
# ==================== MemoryCard 启动脚本 ====================
# 功能：
#   1. 首次部署时自动初始化数据库
#   2. 版本升级时自动执行数据库迁移
#   3. 支持多数据源（PostgreSQL、MySQL、SQLite）
#   4. 启动失败时自动重试

set -e

# 配置
readonly MAX_RETRIES=5
readonly RETRY_INTERVAL=5
readonly MIGRATION_TIMEOUT=60

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 等待数据库就绪
wait_for_database() {
    local db_type="${DB_TYPE:-pgsql}"
    local retries=0

    log_info "等待数据库就绪..."

    while [ $retries -lt $MAX_RETRIES ]; do
        case "$db_type" in
            "pgsql")
                pg_isready -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "${DB_USER:-user}" > /dev/null 2>&1 && return 0
                ;;
            "mysql")
                mysqladmin ping -h "${DB_HOST:-localhost}" -P "${DB_PORT:-3306}" -u "${DB_USER:-user}" -p"${DB_PASSWORD:-password}" > /dev/null 2>&1 && return 0
                ;;
            "sqlite")
                # SQLite 是嵌入式数据库，无需等待
                return 0
                ;;
        esac

        retries=$((retries + 1))
        log_warn "数据库未就绪，${RETRY_INTERVAL}秒后重试... ($retries/$MAX_RETRIES)"
        sleep $RETRY_INTERVAL
    done

    log_error "数据库连接超时"
    return 1
}

# 初始化数据库
init_database() {
    log_info "正在初始化数据库..."

    if python scripts/init_db.py; then
        log_info "数据库初始化成功"
        return 0
    else
        log_error "数据库初始化失败"
        return 1
    fi
}

# 执行数据库迁移
run_migrations() {
    log_info "正在执行数据库迁移..."

    if python scripts/migrate.py migrate; then
        log_info "数据库迁移成功"
        return 0
    else
        log_error "数据库迁移失败"
        return 1
    fi
}

# 检查是否需要初始化
check_and_init() {
    local db_type="${DB_TYPE:-pgsql}"

    # SQLite: 检查数据库文件是否存在
    if [ "$db_type" = "sqlite" ]; then
        local db_file="${DB_FILE:-memorycard.db}"
        local db_path="/app/$db_file"

        if [ ! -f "$db_path" ]; then
            log_info "SQLite 数据库文件不存在，执行初始化..."
            init_database
            return
        fi
    fi

    # PostgreSQL/MySQL: 检查连接和表是否存在
    # 这里使用 Tortoise ORM 的 generate_schemas 来检查
    # 如果表不存在会报错，我们捕获这个错误来判断是否需要初始化
    if python -c "
import asyncio
from tortoise import Tortoise
from settings import TORTOISE_ORM

async def check():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        # 尝试查询 User 表
        from models import User
        await User.all().count()
        await Tortoise.close_connections()
        return True
    except Exception:
        await Tortoise.close_connections()
        return False

result = asyncio.run(check())
exit(0 if result else 1)
" 2>/dev/null; then
        log_info "数据库已存在，跳过初始化"
    else
        log_info "数据库为空或不存在，执行初始化..."
        init_database
    fi
}

# 启动应用
start_application() {
    log_info "启动应用..."

    exec "$@"
}

# 主流程
main() {
    log_info "========================================"
    log_info "  MemoryCard 启动脚本"
    log_info "========================================"
    log_info "数据库类型: ${DB_TYPE:-pgsql}"
    log_info "数据库主机: ${DB_HOST:-localhost}"
    log_info "========================================"

    # 1. 等待数据库就绪
    wait_for_database || exit 1

    # 2. 检查并初始化数据库
    check_and_init

    # 3. 执行数据库迁移
    run_migrations || {
        log_warn "迁移失败，尝试初始化..."
        init_database
        run_migrations || {
            log_error "数据库迁移失败，请检查日志"
            exit 1
        }
    }

    # 4. 启动应用
    log_info "所有初始化检查完成，启动应用..."
    start_application "$@"
}

# 执行主流程
main "$@"
