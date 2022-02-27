"""
建立数据库连接
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import SQLALCHEMY_DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"  # MySQL或PostgreSQL的连接方法

engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True)

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base(bind=engine, name='Base')
