"""
初始化标签数据
包括
1. 标签的图标类名
2. 标签的颜色
"""
import logging
from orm import SessionLocal
from orm.crud import create_tag_class_name, create_tag_color
from orm.schemas import TagClassNameModel, TagColorModel
from dependencies.orm import get_session


def gen_tag_class_name():
    """
    自动生成标签类名数据
    :return:
    """

    session = SessionLocal()
    data = [
        {"class_name": "location-o"},
        {"class_name": "like-o"},
        {"class_name": "star-o"},
        {"class_name": "phone-o"},
    ]
    tag_objs = [TagClassNameModel(**d) for d in data]
    create_tag_class_name(session, tag_objs)
    logging.info("已经创建标签类名数据")
    logging.debug(f"数据: {tag_objs}")  # pydantic有自己的repr
    session.close()


def gen_tag_color():
    """
    自动生成标签类的颜色
    :return:
    """
    session = SessionLocal()
    data = [
        {"color": "#02b340"},
        {"color": "#427371"},
        {"color": "#425140"},
    ]
    tag_color_objs = [TagColorModel(**d) for d in data]
    create_tag_color(session, tag_color_objs)
    logging.info("已经创建标签颜色数据")
    logging.debug(f"数据: {tag_color_objs}")  # pydantic有自己的repr
    session.close()


# gen_tag_class_name()
gen_tag_color()
