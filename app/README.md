# 记忆卡片后端服务

## 开发
1. 创建虚拟环境
    ```shell
    uv venv memory-card-venv --python 3.14
    ```
    请自行安装uv
2. 安装依赖
   ```shell
   uv sync
   ```
3. 启动服务
    ```shell
    uvicorn main:app --reload
    # 或
    python -m fastapi dev main.py
    ```
4. 更改数据库表结构
   如果修改了model，需要同步到数据库，重新执行migrate和upgrade的命令
   ```shell
   # 初始化配置文件和迁移文件位置
   aerich init -t settings.TORTOISE_ORM
   # 初始化数据库
   aerich init-db
   # 更新模型并进行迁移
   # --name指定说明
   aerich migrate --name add_column
   # 更新数据库到最新模型
   aerich upgrade
   ```
   如果想要重新做迁移，删除`.migrations`和`migrations`目录，安装顺序执行上面4个命令即可
   其他命令将官方文档：[aerich](https://github.com/tortoise/aerich)


## 注意
关于`local_settings.py`, 里面定义一些私有的配置, 比如数据库链接, 比如:
```python
database_data = {
    "username": "root",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "3306",
    "database": "MemoryCard",
}

ASYNC_SQLALCHEMY_DATABASE_URL = 'mysql+aiomysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(
    **database_data)
```