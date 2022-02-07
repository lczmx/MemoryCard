"""
定义对数据库的操作
"""
from database import SessionLocal, Base, engine
from models import *

# 创建表, 已经存在的将被忽略
Base.metadata.create_all(bind=engine)
