#!/bin/bash
# ==================== MemoryCard Docker 部署脚本 ====================
# 功能：
#   - 构建 Docker 镜像
#   - 启动/停止/重启服务
#   - 查看日志
#   - 清理资源

set -e

# 配置
readonly PROJECT_NAME="memorycard"
readonly DOCKER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")") && pwd"
readonly COMPOSE_FILE="docker-compose.yml"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 帮助信息
show_help() {
    cat << EOF
${GREEN}MemoryCard Docker 部署脚本${NC}

${BLUE}用法:${NC}
    $0 <命令> [选项]

${BLUE}命令:${NC}
    ${GREEN}build${NC}          构建 Docker 镜像
    ${GREEN}up${NC}             启动服务 (默认 PostgreSQL)
    ${GREEN}up-pgsql${NC}      启动服务 (PostgreSQL)
    ${GREEN}up-mysql${NC}      启动服务 (MySQL)
    ${GREEN}up-sqlite${NC}      启动服务 (SQLite)
    ${GREEN}down${NC}           停止服务
    ${GREEN}restart${NC}        重启服务
    ${GREEN}logs${NC}           查看应用日志
    ${GREEN}logs-db${NC}        查看数据库日志
    ${GREEN}status${NC}         查看服务状态
    ${GREEN}clean${NC}          清理 Docker 资源
    ${GREEN}rebuild${NC}        重新构建并启动
    ${GREEN}shell${NC}          进入应用容器
    ${GREEN}db${NC}             进入数据库容器 (PostgreSQL)
    ${GREEN}backup${NC}         备份数据库
    ${GREEN}restore${NC}        恢复数据库
    ${GREEN}help${NC}           显示帮助信息

${BLUE}示例:${NC}
    $0 build                    # 构建镜像
    $0 up-pgsql                # 使用 PostgreSQL 启动
    $0 up-mysql                # 使用 MySQL 启动
    $0 logs -f                  # 实时查看日志
    $0 backup                   # 备份数据库

EOF
}

# 检查依赖
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: docker 未安装${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}错误: docker-compose 未安装${NC}"
        exit 1
    fi
}

# 获取 docker compose 命令
get_compose_cmd() {
    if docker compose version &> /dev/null; then
        echo "docker compose"
    else
        echo "docker-compose"
    fi
}

# 构建镜像
cmd_build() {
    echo -e "${GREEN}构建 Docker 镜像...${NC}"
    docker build -t ${PROJECT_NAME}:latest .
    docker build -t ${PROJECT_NAME}:$(date +%Y%m%d) .
    echo -e "${GREEN}构建完成!${NC}"
}

# 启动服务 (PostgreSQL)
cmd_up_pgsql() {
    echo -e "${GREEN}启动 MemoryCard 服务 (PostgreSQL)...${NC}"
    $(get_compose_cmd) -f ${COMPOSE_FILE} -f docker-compose.yml up -d --build
    echo -e "${GREEN}服务已启动!${NC}"
    echo -e "访问地址: http://localhost:8366"
}

# 启动服务 (MySQL)
cmd_up_mysql() {
    echo -e "${GREEN}启动 MemoryCard 服务 (MySQL)...${NC}"
    $(get_compose_cmd) -f ${COMPOSE_FILE} -f docker-compose.mysql.yml up -d --build
    echo -e "${GREEN}服务已启动!${NC}"
    echo -e "访问地址: http://localhost:8366"
}

# 启动服务 (SQLite)
cmd_up_sqlite() {
    echo -e "${GREEN}启动 MemoryCard 服务 (SQLite)...${NC}"
    $(get_compose_cmd) -f ${COMPOSE_FILE} -f docker-compose.sqlite.yml up -d --build
    echo -e "${GREEN}服务已启动!${NC}"
    echo -e "访问地址: http://localhost:8366"
}

# 停止服务
cmd_down() {
    echo -e "${YELLOW}停止服务...${NC}"
    $(get_compose_cmd) down
    echo -e "${GREEN}服务已停止${NC}"
}

# 重启服务
cmd_restart() {
    cmd_down
    cmd_up_pgsql
}

# 查看日志
cmd_logs() {
    $(get_compose_cmd) logs -f app "$@"
}

# 查看数据库日志
cmd_logs_db() {
    $(get_compose_cmd) logs -f db "$@"
}

# 查看状态
cmd_status() {
    $(get_compose_cmd) ps
}

# 清理资源
cmd_clean() {
    echo -e "${YELLOW}清理 Docker 资源...${NC}"
    $(get_compose_cmd) down -v --remove-orphans
    docker image prune -f
    echo -e "${GREEN}清理完成${NC}"
}

# 重新构建并启动
cmd_rebuild() {
    cmd_clean
    cmd_build
    cmd_up_pgsql
}

# 进入应用容器
cmd_shell() {
    docker exec -it ${PROJECT_NAME}-app sh
}

# 进入数据库容器
cmd_db() {
    docker exec -it ${PROJECT_NAME}-db psql -U memorycard -d memorycard
}

# 备份数据库
cmd_backup() {
    local backup_dir="${DOCKER_DIR}/backups"
    local backup_file="${backup_dir}/backup_$(date +%Y%m%d_%H%M%S).sql"

    mkdir -p "${backup_dir}"

    echo -e "${GREEN}备份数据库...${NC}"
    $(get_compose_cmd) exec -T db pg_dump -U memorycard -d memorycard > "${backup_file}"
    echo -e "${GREEN}备份已保存到: ${backup_file}${NC}"
}

# 恢复数据库
cmd_restore() {
    local backup_dir="${DOCKER_DIR}/backups"

    echo -e "${YELLOW}可用的备份文件:${NC}"
    ls -la "${backup_dir}"/*.sql 2>/dev/null || echo "没有找到备份文件"

    read -p "请输入要恢复的备份文件名: " backup_file

    if [ -f "${backup_dir}/${backup_file}" ]; then
        echo -e "${GREEN}恢复数据库...${NC}"
        cat "${backup_dir}/${backup_file}" | $(get_compose_cmd) exec -T db psql -U memorycard -d memorycard
        echo -e "${GREEN}恢复完成${NC}"
    else
        echo -e "${RED}备份文件不存在${NC}"
    fi
}

# 主函数
main() {
    check_dependencies

    cd "${DOCKER_DIR}"

    case "${1:-help}" in
        build)       cmd_build ;;
        up)           cmd_up_pgsql ;;
        up-pgsql)    cmd_up_pgsql ;;
        up-mysql)    cmd_up_mysql ;;
        up-sqlite)   cmd_up_sqlite ;;
        down)        cmd_down ;;
        restart)     cmd_restart ;;
        logs)        shift; cmd_logs "$@" ;;
        logs-db)     shift; cmd_logs_db "$@" ;;
        status)      cmd_status ;;
        clean)       cmd_clean ;;
        rebuild)     cmd_rebuild ;;
        shell)       cmd_shell ;;
        db)          cmd_db ;;
        backup)      cmd_backup ;;
        restore)     cmd_restore ;;
        help|--help) show_help ;;
        *)
            echo -e "${RED}未知命令: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
