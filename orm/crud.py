"""
增删改查数据库 数据
"""
import logging
from typing import List, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from orm.models import Tag, TagClassName, TagColor
from orm.database import Base
from orm.schemas import TagModel, TagClassNameModel, TagColorModel


def create_tag(session: Session, tag_data: TagModel) -> Tag:
    """
    创建单个标签数据
    :param session: 数据库连接
    :param tag_data: tag 数据
    :return:Tag
    """

    logging.info("创建tag数据")
    tag_obj = save_one_to_db(session=session, model_class=Tag, data=tag_data)
    logging.debug(f"已经tag创建数据: {tag_obj:r}")
    return tag_obj


def create_tag_class_name(session: Session, tag_class_name_models: List[TagClassNameModel]) -> List[TagClassName]:
    """
    创建多条标签类名数据
    :return:
    """
    tag_class_name_objs = save_all_to_db(session, TagClassName, tag_class_name_models)
    return tag_class_name_objs


def create_tag_color(session: Session, tag_color_models: List[TagColorModel]) -> List[TagColor]:
    """
    创建多条标签类颜色
    :return:
    """
    tag_color_objs = save_all_to_db(session, TagColor, tag_color_models)
    return tag_color_objs


def save_one_to_db(session: Session, model_class: Base, data: BaseModel) -> Base:
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


def save_all_to_db(session: Session, model_class: Base, data_list: List[BaseModel]) -> List[Base]:
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
