"""
增删改查数据库 数据
"""
import datetime
import logging
from typing import List, TypeVar, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, not_, update, delete
from pydantic import BaseModel
from orm.database import Base
from orm.models import Category, Plan, Card
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
        return None


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
        raise None


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
    :return: 数据列表
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    try:
        stmt = select(model_class).where(
            or_(model_class.uid == uid, Plan.uid.is_(None))) if allow_none else select(
            model_class).where(model_class.uid == uid)
        res = session.execute(stmt.limit(query_params.limit).offset(query_params.offset))

        return res.scalars().all()  # 对应之前的.all()
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


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
    :return: 对应sqlalchemy模型类的对象, 没有值时为None
    :return:
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    try:
        stmt = select(model_class).where(model_class.uid == uid, model_class.id == target_id).limit(1)
        res = session.scalars(stmt)
        return res.first()

    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return None


def query_plan_title_by_user(session: Session, *, uid: Optional[int] = None,
                             query_params: Optional[QueryLimit]) -> List[str]:
    """查询某个用户的复习曲线名称"""
    try:
        res = session.execute(
            select(Plan.title).where(Plan.uid == uid).limit(query_params.limit).offset(query_params.offset)
        )

        return res.scalars().all()
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


def toggle_star_status(session: Session, model_class: ModelT, target_id: int, star_status: bool) -> bool:
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
    try:
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
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


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
    try:
        result = session.execute(
            update(model_class).where(model_class.id == target_id, model_class.uid == uid
                                      ).values(**data.dict()))
        session.commit()
        if result.rowcount == 0:
            return None
        return query_one_data_by_user(session, uid, target_id, model_class)
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return None


def update_review_times(session: Session, cid: int, review_times: int, review_at: datetime
                        ) -> int:
    """
    更新卡片复习
    :param session: 数据连接
    :param cid: 卡片ID
    :param review_times: 新的复习次数
    :param review_at: 更新时间
    :return: 受影响行数
    """

    # 需要更新review_at 和 review_times
    try:
        result = session.execute(
            update(Card).where(Card.id == cid).values(
                review_at=review_at,
                review_times=review_times
            )
        )
        session.commit()
        return result.rowcount
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return 0


def delete_data_by_user(session: Session,
                        uid: int,
                        target_id: int,
                        model_class: ModelT,
                        ) -> int:
    """
    根据用户删除数据
    :param session: 数据库链接
    :param uid: 用户ID
    :param target_id: SQLAlchemy表ID
    :param model_class: 目标SQLAlchemy表
    :return: 所影响的行数
    """
    try:
        result = session.execute(
            delete(model_class).where(model_class.id == target_id, model_class.uid == uid)
        )
        session.commit()
        return result.rowcount
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return 0
