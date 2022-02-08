"""
定义表结构
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from orm import Base


class User(Base):
    __tablename__ = 'User'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False, comment='用户名')
    email = Column(String(128), unique=True, nullable=False, comment='邮箱')
    hashed_pwd = Column(String(64), unique=True, nullable=False, comment='哈希后的密文')
    phone_number = Column(String(11), unique=True, nullable=False, comment='手机号')

    tag = relationship("Tag", backref="user")  # 标签子表
    card = relationship("Card", backref="user")  # 卡片子表
    plan = relationship("Plan", backref="user")  # 计划子表
    current_plan = relationship("CurrentPlan", backref="user")  # 目前的计划子表


class Tag(Base):
    __tablename__ = 'Tag'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id"))
    icon = Column(String(32), nullable=False, default="", comment='图标的类名')
    color = Column(String(7), nullable=False, default="#205580", comment='标签颜色')

    card = relationship("Card", backref="tag")


class Card(Base):
    __tablename__ = 'Card'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id"))
    tid = Column(Integer, ForeignKey("Tag.id"))

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    summary = Column(String(64), default="", comment='卡片的概要信息(提示信息)')
    description = Column(Text, nullable=False, comment='卡片的详细内容')

    current_plan = relationship("CurrentPlan", backref="card")  # 目前的计划子表


class Plan(Base):
    __tablename__ = 'Plan'  # 复习计划
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id"))

    title = Column(String(32), nullable=False, comment='复习记录的名称')
    content = Column(String(1024), nullable=False, comment='复习计划内容')
    current_plan = relationship("CurrentPlan", backref="plan")  # 目前的计划子表


class CurrentPlan(Base):
    __tablename__ = 'CurrentPlan'  # 当前要复习的计划
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id"))
    cid = Column(Integer, ForeignKey("Card.id"))
    pid = Column(Integer, ForeignKey("Plan.id"))

    review_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='复习时间')
    next_review_at = Column(DateTime, comment='下次复习时间')
