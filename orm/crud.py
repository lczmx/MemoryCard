"""
增删改查数据库 数据
"""
import logging
from typing import List, TypeVar, Type, Optional, NoReturn

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, not_, update
from pydantic import BaseModel
from orm.database import Base
from orm.models import Category, Plan, Card
from orm.schemas.category import WriteCategoryModel
from orm.schemas.generic import QueryLimit

ModelT = TypeVar("ModelT", bound=Base)
DataT = TypeVar("DataT", bound=BaseModel)


def save_one_to_db(session: Session, model_class: ModelT, data: DataT) -> ModelT:
    """
    保存一条到数据库
    :param session:
    :param model_class: sqlalchemy模型类
    :param data: pydantic模型对象
    :return: 对应sqlalchemy模型类的对象
    """
    try:
        obj = model_class(**data.dict())
        session.add(obj)
        session.commit()
        # 手动将 数据 刷新到数据库
        session.refresh(obj)
        return obj

    except Exception as e:
        # 别忘记发生错误时回滚
        session.rollback()
        logging.error(str(e))
        raise e


def save_all_to_db(session: Session, model_class: ModelT, data_list: List[DataT]) -> List[ModelT]:
    """
    将多条保存到数据库
    :param session:
    :param model_class: sqlalchemy模型类
    :param data_list: pydantic模型对象列表
    :return: 对应sqlalchemy模型类的对象列表
    """
    try:
        objs = [model_class(**data.dict()) for data in data_list]

        session.add_all(objs)
        session.commit()
        return objs
    except Exception as e:
        # 别忘记发生错误时回滚
        session.rollback()
        logging.error(str(e))
        raise e


def query_all_data_by_user(session: Session, uid: int,
                           model_class: ModelT,
                           query_params: Optional[QueryLimit],
                           allow_none=False
                           ) -> list[ModelT]:
    """
    通过uid, 查询用户的数据, 多条数据

    :param session: 数据连接
    :param uid: 用户id
    :param model_class: sqlalchemy模型类
    :param query_params: limit offset 参数
    :param allow_none: 是否将uid为null的情况纳入
    :return: 对应sqlalchemy模型类的对象 列表
    :return:
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    stmt = select(model_class).where(
        or_(model_class.uid == uid, Plan.uid.is_(None))) if allow_none else select(
        model_class).where(model_class.uid == uid)
    res = session.execute(stmt.limit(query_params.limit).offset(query_params.offset))

    return res.scalars().all()  # 对应之前的.all()


def query_one_data_by_user(session: Session,
                           uid: int,
                           target_id: int,
                           model_class: ModelT,
                           ) -> ModelT:
    """
    通过uid, 查询用户的数据, 一条数据

    :param session: 数据连接
    :param uid: 用户id
    :param target_id: model_class的主键id值
    :param model_class: sqlalchemy模型类
    :return: 对应sqlalchemy模型类的对象
    :return:
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    stmt = select(model_class).where(model_class.uid == uid, model_class.id == target_id).limit(1)
    res = session.scalars(stmt)

    return res.first()  # 对应之前的.all()


def query_plan_title_by_user(session: Session, *, uid: Optional[int] = None,
                             query_params: Optional[QueryLimit]) -> List[str]:
    """查询某个用户的复习曲线名称"""
    res = session.execute(
        select(Plan.title).where(Plan.uid == uid).limit(query_params.limit).offset(query_params.offset)
    )

    return res.scalars().all()


def toggle_star_status(session: Session, model_class: ModelT, target_id: int, star_status: bool) -> NoReturn:
    """
    切换卡片或分类的星标状态
    :param session: 数据连接
    :param model_class:  sqlalchemy模型类
    :param target_id: 主键值
    :param star_status: 目前星标状态
    :return:
    """
    try:

        session.execute(
            update(model_class).where(model_class.id == target_id
                                      ).values(is_star=not_(star_status)))
        session.commit()
        return not star_status
    except Exception as e:
        logging.error(str(e))
        # 返回原来的
        return star_status


def query_need_review_card(session: Session, uid: int, query_params: Optional[QueryLimit]) -> List[Card]:
    """
    查询所有需要复习的卡片
    :param session: 数据连接
    :param uid: 用户id
    :param query_params: limit offset 参数
    :return: 卡片模型类的对象列表
    """

    stmt = select(Card).where(
        Card.cid == Category.id,
        Category.pid == Plan.id,
        Card.uid == uid
    )

    res = session.execute(
        stmt.limit(query_params.limit).offset(query_params.offset)
    )
    temp = [i for i in res.scalars().all() if i.is_review_date]
    return temp


def update_data(session: Session, uid: int, target_id: int, model_class: ModelT, data: DataT) -> ModelT:
    """
      通过uid, target_id, 根更新一条数据

    :param session: 数据连接
    :param uid: 用户id
    :param target_id: model_class的主键id值
    :param model_class: sqlalchemy模型类
    :param data: pydantic数据模型类
    :return: 对应sqlalchemy模型类的对象
    """
    session.execute(
        update(model_class).where(model_class.id == target_id, model_class.uid == uid
                                  ).values(**data.dict()))
    session.commit()
    return query_one_data_by_user(session, uid, target_id, model_class)
