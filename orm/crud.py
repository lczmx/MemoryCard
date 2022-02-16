"""
增删改查数据库 数据
"""
import logging
from typing import List, TypeVar, Type, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from pydantic import BaseModel
from orm.models import Category, Plan
from orm.schemas.category import WriteCategoryModel
from orm.schemas.generic import QueryLimit

ModelT = TypeVar("ModelT")
DataT = TypeVar("DataT", bound=BaseModel)


def create_category(session: Session, data: WriteCategoryModel) -> Type[Category]:
    """创建分类"""
    logging.info("创建category数据")
    cate_obj = save_one_to_db(session=session, model_class=Category, data=data)
    return cate_obj


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


def query_plan_by_user(session: Session, uid: int,
                       query_prams: Optional[QueryLimit]) -> List[Plan]:
    """
    查询某个用户的复习曲线
    包括默认的
    """
    res = session.execute(
        select(Plan).where(
            or_(
                Plan.uid == uid,
                Plan.uid.is_(None)
            )
        ).limit(query_prams.limit).offset(query_prams.offset)
    )

    return res.scalars().all()


def query_plan_title_by_user(session: Session, *, uid: Optional[int] = None,
                             query_prams: Optional[QueryLimit]) -> List[str]:
    """查询某个用户的复习曲线名称"""
    res = session.execute(
        select(Plan.title).where(Plan.uid == uid).limit(query_prams.limit).offset(query_prams.offset)
    )

    return res.scalars().all()
