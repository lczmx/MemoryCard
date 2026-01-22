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