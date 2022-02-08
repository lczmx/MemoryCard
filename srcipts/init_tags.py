"""
初始化标签数据
包括
1. 标签的图标类名
2. 标签的颜色
"""
from sqlalchemy.orm import Session
from fastapi import Depends
from orm.crud import create_tag
from dependencies.orm import get_session


def gen_tags(session: Session = Depends(get_session)):
    pass
