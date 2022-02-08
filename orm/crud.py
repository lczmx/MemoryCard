"""
增删改查数据库 数据
"""
from typing import List, Any
from sqlalchemy.orm import Session
from orm.models import Tag
from orm.schemas import TagModel


def create_tag(session: Session, tag_data: TagModel) -> Tag:
    """
    创建单个标签数据
    :param session: 数据库连接
    :param tag_data: tag 数据
    :return:Tag
    """
    tag_obj = Tag(**tag_data.dict())
    save_to_db(session, tag_obj)
    return tag_obj


def create_tags(session: Session, tags_data: List[TagModel]) -> List[Tag]:
    """
    创建多个标签数据
    :param session:数据库连接
    :param tags_data:tag 数据的列表
    :return:List[Tag]
    """
    tag_objs = [Tag(**data.dict()) for data in tags_data]
    save_all_to_db(session, tag_objs)
    return tag_objs


def save_to_db(session: Session, obj: Any):
    """
    将obj保存到数据库
    :param session:
    :param obj:
    :return:
    """
    try:

        session.add(obj)
        session.commit()
        # 手动将 数据 刷新到数据库
        session.refresh(obj)
    except Exception as e:
        # 别忘记发生错误时回滚
        session.rollback()
        raise e


def save_all_to_db(session: Session, objs: List[Any]):
    """
    将obj列表保存到数据库
    :param session:
    :param objs:
    :return:
    """
    try:
        session.add_all(objs)
        session.commit()
    except Exception as e:
        # 别忘记发生错误时回滚
        session.rollback()
        raise e
