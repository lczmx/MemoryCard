用惯了django的迁移命令后, 发现SQLAlchemy默认没有对应的迁移命令, 但是SQLAlchemy作者为SQLAlchemy开发了迁移工具: `Alembic`, 其官方文档见: [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)  
> 使用这个工具的需要前提安装数据库链接库,如:`pymysql`

# 安装
我这里使用`virtualenv`创建虚拟环境, 所以使用`pip`命令安装:
```shell
$pip install alembic
```
# 初始化项目并配置alembic
在项目的根目录执行初始化命令:
```shell
$alembic init alembic
```
上述命令的第二个`alembic`指的是存放配置和迁移历史等数据的目录, 设置自己喜欢的目录名  

此时`alembic`会生成以下目录与文件:
```bash
<project-name>
+--- alembic
|   +--- env.py
|   +--- README
|   +--- script.py.mako
|   +--- versions
|   
+--- alembic.ini

```
接下来需要配置`alembic.ini`和`env.py`:  
1. `alembic.ini`配置数据库链接  
    修改`sqlalchemy.url`配置, 这个和创建`engine`的`url`是一样的, 如:
    ```ini
    sqlalchemy.url = mysql+pymysql://demo_user:demo123456@127.0.0.1:3306/demo_db
    ```
2. `env.py`配置`metadata`
    ```python
    from orm.database import Base

    target_metadata = Base.metadata
    ```
    这里的`Base`是`BaseModel`即由`declarative_base`创建的基类  

# 第一次执行迁移命令
执行: `alembic upgrade head`命令,  
该命令指的是: 将数据库升级(切换)到最新版本, 该过程会创建没有表  
你可以类比`git`  


# 执行迁移命令
假如不是第一次执行迁移命令了, 你可以执行以下命令:
`alembic revision --autogenerate -m "init db"`  

`-m`指定此次迁移的注释, `alembic`会根据这个注释在`versions`目录生成一个`py`文件, 用于记录操作  
# 其他命令
## 查看迁移历史
```shell
$alembic history --verbose
Rev: fe3dcb76f464 (head)
Parent: 8bb0bf479f9d
Path: E:\code\Project\alembic\versions\fe3dcb76f464_测试.py
    Create Date: 2022-02-19 21:59:22.473262

Rev: 8bb0bf479f9d
Parent: <base>
Path: E:\code\Project\alembic\versions\8bb0bf479f9d_init_db.py

    init db

    Revision ID: 8bb0bf479f9d
    Revises:
    Create Date: 2022-02-19 21:22:46.521491

```
我们主要需要关注`head`即头指针的位置和` Revision ID`即该迁移的哈希值, 对应着该版本的指针  
    
## 查看当前指针的指向
```shell
$alembic current
2022-02-19 22:12:39,749 INFO sqlalchemy.engine.Engine BEGIN (implicit)
...
2022-02-19 22:12:39,755 INFO sqlalchemy.engine.Engine COMMIT
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
8bb0bf479f9d
```
最后一行的值为当前版本的指向
    
## 切换到对应的迁移版本
> 这里对应向上和向下切换
> 通过`Parent`确定此次迁移的父版本

```bash
# 向上切换
alembic upgrade <version>

# 向下切换
alembic downgrade <version>
```
如:
```shell
$alembic downgrade 8bb0bf479f9d
$alembic upgrade fe3dcb76f464
```
当然也可以使用命令直接切换到最新/老的版本:
```shell
# 切换到最新版本
$alembic upgrade head

# 切换到最老版本
$alembic downgrade base

```
## 生成sql文件
在某些不适合在线更新的情况，可以采用生成`sql`脚本的形式，进行离线更新：

```bash
alembic upgrade <version> --sql > migration.sql
```

```shell
$alembic upgrade 8bb0bf479f9d--sql > migration.sql
```

从特定起始版本生成sql脚本：

```bash
alembic upgrade <vsersion>:<vsersion> --sql > migration.sql
```
```shell
$alembic upgrade 8bb0bf479f9d:fe3dcb76f464--sql > migration.sql

```
