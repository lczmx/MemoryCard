# MemoryCard 记忆卡片后端服务

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-purple.svg)](https://fastapi.tiangolo.com/)
[![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-0.25.3-orange.svg)](https://tortoise.github.io/)

基于 FastAPI 的记忆卡片后端服务，支持间隔重复学习算法（艾宾浩斯遗忘曲线），帮助用户高效记忆各类知识。

## 📖 项目介绍

MemoryCard 是一个轻量级、可扩展的记忆卡片学习系统后端，提供以下核心功能：

- **记忆卡片管理** - 创建、编辑、删除、批量导入卡片
- **智能复习引擎** - 基于艾宾浩斯遗忘曲线的间隔重复算法
- **学习计划** - 自定义复习曲线，灵活调整复习节奏
- **分类体系** - 多层级知识分类管理
- **学习分析** - 复习统计、记忆曲线分析、薄弱点诊断
- **多数据库支持** - PostgreSQL、MySQL、SQLite

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 用户认证 | JWT Token 认证，支持用户名/邮箱登录 |
| 卡片管理 | CRUD 操作、批量处理、星标收藏 |
| 分类管理 | 多层级分类、图标颜色自定义 |
| 智能复习 | 艾宾浩斯算法自动调度复习时间 |
| 学习计划 | 多种预设曲线 + 自定义复习间隔 |
| 数据分析 | 学习时长、复习次数、掌握度统计 |
| 多数据源 | PostgreSQL / MySQL / SQLite |
| Docker 部署 | 一键部署，自动数据库迁移 |

## 🛠️ 技术栈

| 分类 | 技术 |
|------|------|
| Web 框架 | FastAPI 0.128.0+ |
| ORM | Tortoise ORM 0.25.3+ |
| 数据库迁移 | Aerich 0.9.2+ |
| 数据校验 | Pydantic v2 |
| 认证 | python-jose, passlib |
| 日志 | Loguru |
| 异步驱动 | asyncpg, aiomysql, aiosqlite |
| 服务器 | Uvicorn |

## 📁 项目结构

```
MemoryCard/
├── api/                    # API 路由层
│   ├── analyse.py          # 学习分析接口
│   ├── cards.py            # 卡片管理接口
│   ├── category.py         # 分类管理接口
│   ├── help.py             # 帮助文档接口
│   ├── plans.py            # 学习计划接口
│   ├── review.py           # 复习接口
│   └── user.py             # 用户接口
├── models/                 # 数据模型层
│   ├── card.py             # 卡片模型
│   ├── category.py         # 分类模型
│   ├── doc.py              # 文档模型
│   ├── operation.py        # 操作记录模型
│   ├── plan.py             # 复习曲线模型
│   ├── record.py           # 学习记录模型
│   └── user.py             # 用户模型
├── schemas/                # Pydantic 数据模型
├── service/                # 业务逻辑层
│   ├── category_service.py
│   ├── record_service.py
│   └── utils.py            # 复习调度工具
├── dependencies/            # 依赖注入
│   ├── auth.py             # JWT 认证
│   ├── orm.py              # ORM 依赖
│   └── queryParams.py      # 查询参数处理
├── scripts/                 # 脚本
│   ├── migrate.py          # 数据库迁移管理
│   └── init_db.py          # 数据库初始化
├── docker/                  # Docker 相关
│   ├── entrypoint.sh       # 容器启动脚本
│   └── deploy.sh           # 部署脚本
├── main.py                 # 应用入口
├── settings.py              # 配置管理
└── pyproject.toml          # 项目配置
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- PostgreSQL 14+ / MySQL 8+ / SQLite 3
- Docker & Docker Compose (可选)

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/lczmx/MemoryCard.git
cd MemoryCard/app

# 2. 创建虚拟环境
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. 安装依赖
uv sync

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 SECRET_KEY 等配置

# 5. 初始化数据库
python scripts/migrate.py upgrade

# 6. 启动开发服务器
uvicorn main:app --host 0.0.0.0 --port 8366 --reload
# 或
fastapi dev main.py --host 0.0.0.0 --port 8366
```

访问 http://localhost:8366/docs 查看 API 文档。

### Docker 部署

```bash
# 1. 复制环境变量配置
cp .env.docker.example .env.docker
# 编辑 .env.docker 设置密码等

# 2. 启动服务 (PostgreSQL)
docker-compose -f docker-compose.yml up -d

# 3. 查看日志
docker logs -f memorycard-app

# 4. 访问
# API 文档: http://localhost:8366/docs
# 应用端口: 8366
```

**使用其他数据库：**

```bash
# MySQL
docker-compose -f docker-compose.yml -f docker-compose.mysql.yml up -d

# SQLite (开发环境)
docker-compose -f docker-compose.yml -f docker-compose.sqlite.yml up -d
```

**使用部署脚本：**

```bash
cd docker
./deploy.sh build          # 构建镜像
./deploy.sh up-pgsql       # 启动 (PostgreSQL)
./deploy.sh logs -f        # 查看日志
./deploy.sh backup         # 备份数据库
```

## ⚙️ 环境变量配置

创建 `.env` 文件：

```bash
# ==================== 数据库配置 ====================
DB_TYPE="pgsql"              # 支持: pgsql, mysql, sqlite

# PostgreSQL
DB_HOST="localhost"
DB_PORT=5432
DB_NAME="memorycard"
DB_USER="user"
DB_PASSWORD="password"

# SQLite (开发环境)
DB_FILE="memorycard.db"

# ==================== JWT配置 ====================
SECRET_KEY="your-secret-key"  # 必须设置，使用随机字符串
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=360

# ==================== 日志配置 ====================
LOG_LEVEL="info"
LOG_ROTATION="10 MB"
LOG_RETENTION="30 days"
```

## 📚 数据库迁移

### 使用迁移脚本

```bash
# 完整升级 (初始化 + 迁移)
python scripts/migrate.py upgrade

# 仅初始化表结构
python scripts/migrate.py init

# 生成迁移文件
python scripts/migrate.py generate

# 应用迁移
python scripts/migrate.py migrate

# 回滚迁移
python scripts/migrate.py rollback

# 查看迁移状态
python scripts/migrate.py status

# 重置数据库 (危险!)
python scripts/migrate.py reset
```

### 多数据源迁移

```bash
# PostgreSQL
DB_TYPE=pgsql python scripts/migrate.py upgrade

# MySQL
DB_TYPE=mysql python scripts/migrate.py upgrade

# SQLite
DB_TYPE=sqlite python scripts/migrate.py upgrade
```

### 模型变更流程

```bash
# 1. 修改 models/ 中的模型
# 2. 生成迁移
python scripts/migrate.py generate

# 3. 应用迁移
python scripts/migrate.py migrate

# 4. 提交代码
git add migrations/ && git commit
```

## 📖 API 接口

启动服务后访问交互式文档：

- **Swagger UI**: http://localhost:8366/docs
- **ReDoc**: http://localhost:8366/redoc

### 主要接口

| 模块 | 前缀 | 功能 |
|------|------|------|
| 用户 | `/user` | 注册、登录、个人信息 |
| 卡片 | `/cards` | 卡片 CRUD、批量操作 |
| 分类 | `/category` | 分类管理、星标收藏 |
| 复习 | `/review` | 获取复习卡片、完成复习 |
| 计划 | `/plans` | 学习计划管理 |
| 分析 | `/analyse` | 学习统计数据 |
| 帮助 | `/help` | 使用文档 |

## 🔧 开发规范

### 代码风格

- 遵循 PEP 8
- 使用类型注解
- 异步函数使用 `async/await`

### API 设计规范

- RESTful 风格
- 使用 Pydantic 进行数据校验
- 返回统一格式：

```json
{
  "status": 1,
  "msg": "操作成功",
  "data": {}
}
```

### ORM 使用规范

```python
# ✅ 正确：预加载外键
card = await Card.filter(pk=cid).first()
await card.fetch_related("category", "category__plan")

# ❌ 错误：直接访问未预加载的外键
plan = card.category.plan  # 可能返回 QuerySet 而非对象

# ✅ 正确：模型实例更新
card.field = value
await card.save()

# ❌ 错误：模型实例不能使用 .update()
await card.update(field=value)  # 不存在此方法
```

### 分支管理

```bash
main      # 主分支，稳定版本
develop   # 开发分支
feature/* # 功能分支
fix/*     # 修复分支
```

## 🐛 常见问题

### Q: 启动报错 "SECRET_KEY" is required?

**A:** 在 `.env` 文件中设置 `SECRET_KEY`：
```bash
SECRET_KEY="your-random-secret-key-here"
```

### Q: 数据库连接失败?

**A:** 检查以下几点：
1. 数据库服务是否运行
2. `.env` 配置是否正确
3. 数据库用户权限是否足够
4. 防火墙是否允许连接

### Q: 迁移失败如何回滚?

**A:** 
```bash
# 查看迁移历史
python scripts/migrate.py status

# 回滚到上一个版本
python scripts/migrate.py rollback
```

### Q: 如何完全重置数据库?

**A:** 
```bash
# 删除迁移文件
rm -rf migrations/models/*.py

# 重建数据库
python scripts/migrate.py reset
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 📄 许可证

本项目基于 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 开源。

## 📬 联系方式

- GitHub: https://github.com/lczmx/MemoryCard
- Email: lczmx@foxmail.com

---

<p align="center">
 Made with ❤️ by lczmx
</p>
