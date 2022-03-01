"""
定义表结构
"""
from datetime import date

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, func, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime, timedelta
from orm import Base


class User(Base):
    __tablename__ = 'User'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False, comment='用户名')
    email = Column(String(128), unique=True, nullable=False, comment='邮箱')
    hashed_pwd = Column(String(64), unique=True, nullable=False, comment='哈希后的密文')
    phone_number = Column(String(11), unique=True, nullable=True, comment='手机号')

    category = relationship("Category", backref="user", cascade="all, delete",
                            passive_deletes=True)  # 类别子表
    card = relationship("Card", backref="user", cascade="all, delete", passive_deletes=True)  # 卡片子表
    plan = relationship("Plan", backref="user", cascade="all, delete", passive_deletes=True)  # 计划子表
    recode = relationship("Recode", backref="user", cascade="all, delete", passive_deletes=True)  # 操作记录


class Category(Base):
    __tablename__ = 'Category'  # 卡片类别
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id", ondelete='CASCADE'), comment='类别所属用户')
    # !!! 删除plan时 pid默认为1
    pid = Column(Integer, ForeignKey("Plan.id"), comment='类别的复习曲线')
    name = Column(String(32), nullable=False, comment='类别名')
    icon = Column(String(32), nullable=False, comment='类别图标的类名')
    color = Column(String(7), nullable=False, comment='类别颜色')
    is_star = Column(Boolean, nullable=False, default=False, comment="是否星标")
    card = relationship("Card", backref="category", cascade="all, delete", passive_deletes=True)


class Card(Base):
    __tablename__ = 'Card'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id", ondelete='CASCADE'), comment="卡片所属用户")
    cid = Column(Integer, ForeignKey("Category.id", ondelete='CASCADE'), comment="卡片所属类别")
    title = Column(String(32), nullable=False, comment="卡片标题")
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    review_at = Column(DateTime, nullable=False, server_default=func.now(), comment='卡片这次复习时间')
    review_times = Column(Integer, nullable=False, default=0, comment='卡片这次复习的次数')
    summary = Column(String(1024), default="", comment='卡片的概要信息(提示信息)')
    description = Column(Text, nullable=False, comment='卡片的详细内容')
    is_star = Column(Boolean, nullable=False, default=False, comment="是否星标")

    @hybrid_property
    def is_review_date(self):
        content = self.category.plan.content
        plan_sec = content.split('-')
        if self.review_times >= len(plan_sec):
            return False
        sec = int(plan_sec[self.review_times])
        res_date = self.review_at + timedelta(seconds=sec)

        return res_date <= datetime.now()

    @hybrid_method
    def is_review_by_date(self, query_date: date):
        """
        复习日期为指定日期
        :return:
        """
        content = self.category.plan.content
        plan_sec = content.split('-')
        if self.review_times >= len(plan_sec):
            return False
        sec = int(plan_sec[self.review_times])
        res_date = self.review_at + timedelta(seconds=sec)
        return query_date == res_date.date()


class Plan(Base):
    __tablename__ = 'Plan'  # 复习计划/曲线
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id", ondelete='CASCADE'), default=None, comment="复习曲线所属用户")

    title = Column(String(32), nullable=False, comment='复习曲线的名称')
    content = Column(String(1024), nullable=False, comment='复习曲线内容, 以空格隔开, 单位s')

    category = relationship("Category", backref="plan")

    @hybrid_property
    def editable(self):
        # 是否可以编辑
        return bool(self.uid)


class Recode(Base):
    __tablename__ = "Recode"  # 记录复习时的记录
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False, comment="记录所属用户")
    oid = Column(Integer, ForeignKey("Operation.id", ondelete="CASCADE"), nullable=False, comment="该记录的操作类型")
    create_at = Column(Date, nullable=False, comment="记录时间")


class Operation(Base):
    __tablename__ = "Operation"  # 操作记录
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """
    1. delete_card
    2. create_card
    3. review_card
    
    4. delete_category
    5. create_category

    6. delete_plan
    7. create_plan

    """
    title = Column(String(32), nullable=True, comment="操作记录")
    recode = relationship("Recode", backref="operation")


class Doc(Base):
    __tablename__ = "Doc"  # 文档
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(64), nullable=False, comment="文档标题")
    tag = Column(String(128), nullable=False, comment="文档tag")
    content = Column(Text, nullable=False, comment="文档内容")
