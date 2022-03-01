"""
增删改查数据库 数据
"""
import datetime
import logging
from typing import List, TypeVar, Optional, Dict, Type, Union

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, not_, update, delete, func, desc
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel
from orm.database import Base
from orm.models import Category, Plan, Card, User, Operation, Recode

from orm.schemas.category import ReadCategoryModel, ParamsCategoryModel
from orm.schemas.plan import ParamsPlanModel
from orm.schemas.card import ParamsCardModel
from orm.schemas.generic import QueryLimit, CardDateQueryLimit
from orm.schemas.analyse import WriteRecodeModel
import settings

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
                           allow_none=False,
                           order=None
                           ) -> list[ModelT]:
    """
    通过uid, 查询用户的数据, 多条数据

    :param session: 数据连接
    :param uid: 用户id
    :param model_class: sqlalchemy模型类
    :param query_params: limit offset 参数
    :param allow_none: 是否将uid为null的情况纳入
    :param order: 排序条件
    :return: 对应sqlalchemy模型类的对象 列表
    :return: 数据列表
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    try:
        stmt = select(model_class).where(
            or_(model_class.uid == uid, model_class.uid.is_(None))) if allow_none else select(
            model_class).where(model_class.uid == uid)
        if order:
            res = session.execute(stmt.limit(query_params.limit).offset(query_params.offset).order_by(order()))
        else:
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


def toggle_star_status(session: Session, model_class: ModelT, uid: int, target_id: int, star_status: bool) -> int:
    """
    切换卡片或分类的星标状态
    :param session: 数据连接
    :param model_class:  sqlalchemy模型类
    :param uid: 用户ID
    :param target_id: 主键值
    :param star_status: 目前星标状态
    :return: 所影响行数
    """
    try:

        result = session.execute(
            update(model_class).where(model_class.id == target_id, model_class.uid == uid
                                      ).values(is_star=not_(star_status)))
        session.commit()
        return result.rowcount
    except Exception as e:
        logging.error(str(e))
        # 返回原来的
        return 0


def query_need_review_card(session: Session, uid: int, query_params: Optional[QueryLimit],
                           cid: int = 0) -> List[Card]:
    """
    查询所有需要复习的卡片
    :param session: 数据连接
    :param uid: 用户id
    :param cid: 分类id
    :param query_params: limit offset 参数
    :return: 卡片模型类的对象列表
    """
    try:
        if cid == 0:
            stmt = select(Card).where(Card.cid == Category.id, Card.uid == uid)
        else:
            stmt = select(Card).where(Card.cid == cid, Card.uid == uid)

        res = session.execute(stmt)
        temp = [i for i in res.scalars().all() if i.is_review_date]
        # TODO: 优化一下
        return temp[query_params.offset: query_params.offset + query_params.limit]
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


def query_review_card_by_date(session: Session, uid: int, query_params: CardDateQueryLimit) -> List[Card]:
    """
    查询所有需要复习的卡片
    :param session: 数据连接
    :param uid: 用户id
    :param query_params: limit offset date 参数
    :return: 卡片模型类的对象列表
    """
    try:
        stmt = select(Card).where(Card.uid == uid)

        res = session.execute(stmt)
        # 首先是可以复习, 然后才是指定日期
        temp = [i for i in res.scalars().all() if
                i.is_review_date and i.is_review_by_date(query_date=query_params.date)]
        # TODO: 优化一下
        return temp[query_params.offset: query_params.offset + query_params.limit]
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


def update_category_data(session: Session, uid: int, cid: int,
                         data: ParamsCategoryModel) -> Union[Type[Category], None]:
    """
    更新类别的数据
    修改plan时 重置 review_at和review_times
    :param session:
    :param uid:
    :param cid:
    :param data:
    :return:
    """
    try:
        # 对比pid
        old_category_data = query_one_data_by_user(session, uid, cid, Category)
        if old_category_data.pid != data.pid:
            # 重置卡片的review_at和review_times
            reset_cards_review(session=session, uid=uid, cards=old_category_data.card)
            session.commit()

        return update_data(session=session, uid=uid, target_id=cid, model_class=Category, data=data)
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return None


def update_card_data(session: Session, uid: int, cid: int, data: ParamsCardModel) -> Union[Type[Card], None]:
    """
    更新卡片的数据
    修改plan时 重置 review_at和review_times
    :param session:
    :param uid:
    :param cid:
    :param data:
    :return:
    """
    try:
        # 对比pid
        old_card_data = query_one_data_by_user(session, uid, cid, Card)
        if old_card_data.cid != data.cid:
            # 重置卡片的review_at和review_times=
            reset_cards_review(session=session, uid=uid, cards=[old_card_data])
            session.commit()

        return update_data(session=session, uid=uid, target_id=cid, model_class=Card, data=data)
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return None


def update_plan_data(session: Session, uid: int, pid: int, data: ParamsPlanModel) -> Union[Type[Plan], None]:
    """
    更新复习曲线
    修改plan时 重置 review_at和review_times
    :param session:
    :param uid:
    :param pid:
    :param data:
    :return:
    """
    try:
        # 对比pid
        old_plan_data = query_one_data_by_user(session, uid, pid, Plan)
        if old_plan_data.content != data.content:
            # 重置卡片的review_at和review_times=
            for category in old_plan_data.category:
                reset_cards_review(session=session, uid=uid, cards=category.card)
        return update_data(session=session, uid=uid, target_id=pid, model_class=Plan, data=data)
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


def reset_cards_review(session: Session, uid: int, cards: List[Card]):
    """
    重置卡片复习数据
    :param session:
    :param uid:
    :param cards:
    :return:
    """
    for card in cards:
        if card.uid != uid:
            continue
        card.review_times = 0
        card.review_at = datetime.datetime.now()
    session.commit()


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


def delete_category_data(session: Session,
                         uid: int,
                         cid: int,
                         ) -> int:
    """
    根据用户删除类别数据
    :param session: 数据库链接
    :param uid: 用户ID
    :param cid: CategoryID
    :return: 所影响的行数
    """
    try:
        # TODO: 优化
        result = session.execute(
            delete(Category).where(Category.id == cid, Category.uid == uid)
        )
        session.execute(
            delete(Card).where(Card.uid == uid, Card.cid == cid)
        )
        session.commit()
        return result.rowcount
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return 0


def query_category_by_user_order_card_count(session: Session, uid: int,
                                            query_params: Optional[QueryLimit],
                                            order: str
                                            ) -> list[ModelT]:
    """
    通过uid, 查询用户的数据, 多条数据, 根据卡片数量排序

    :param session: 数据连接
    :param uid: 用户id
    :param query_params: limit offset 参数
    :param order: 排序条件
    :return: 对应sqlalchemy模型类的对象 列表
    :return: 数据列表
    """
    # 判断是否allow_none, 选择对应的语句
    # Statement
    try:
        if order == "cardCount":
            stmt = select(Category, func.count(Category.id).label("count")).where(Category.uid == uid).select_from(
                Category).join(Card).group_by(
                Category.id).order_by("count")
        else:
            stmt = select(Category, func.count(Category.id).label("count")).where(Category.uid == uid).select_from(
                Category).join(Card).group_by(
                Category.id).order_by(desc("count"))

        res = session.execute(stmt.limit(query_params.limit).offset(query_params.offset))

        return res.scalars().all()  # 对应之前的.all()
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


def query_review_category_by_user(session: Session, uid: int, query_params: Optional[QueryLimit]) -> list[Dict]:
    """

    :param session:
    :param uid:
    :param query_params:
    :return:
    """

    stmt = select(Card).where(
        Card.cid == Category.id,
        Category.pid == Plan.id,
        Card.uid == uid
    )

    res = session.execute(stmt)
    # TODO: 优化一下
    need_review_card = [i.id for i in res.scalars().all() if i.is_review_date]

    # 利用子查询 查询类别
    stmt = select(Category, func.count(Category.id).label("count")
                  ).where(Category.uid == uid, Card.id.in_(need_review_card)
                          ).select_from(Category).join(Card).group_by(Category.id).order_by(desc("count"))

    rows = session.execute(stmt.limit(query_params.limit).offset(query_params.offset))
    # 拼接列表
    result = []
    for row in rows:
        temp = {}
        res = ReadCategoryModel.from_orm(row.Category)
        res.count = row.count
        temp.update(res.dict())
        result.append(temp)

    return result  # 对应之前的.all()


def query_user_username_exists(session: Session, username: str) -> bool:
    """
    用户名是否存在
    :param session:
    :param username:  用户名
    :return:
    """
    res = session.execute(
        select(User.id).where(User.username == username)
    )
    return bool(res.first())


def query_user_email_exists(session: Session, email: str) -> bool:
    """
    邮箱是否存在
    :param session:
    :param email:  邮箱
    :return:
    """
    res = session.execute(
        select(User.id).where(User.email == email)
    )
    return bool(res.first())


def query_account_by_username_or_email(session: Session, username: str, email: str) -> List[User]:
    """
    获取符合用户名和邮箱要求的用户对象
    :param session:
    :param username:
    :param email:
    :return:
    """
    try:
        res = session.execute(
            select(User).where(or_(User.username == username, User.email == email))
        )
        return res.scalars().all()
    except Exception as e:
        logging.error(str(e))
        return []


def query_user_by_id(session: Session, uid: int) -> Union[User, None]:
    """
   获取用户对象
    :param session:
    :param uid:
    :return:
    """
    try:
        stmt = select(User).where(User.id == uid).limit(1)
        res = session.scalars(stmt)
        return res.first()

    except Exception as e:
        logging.error(str(e))
        return None


def query_operation_title(session: Session) -> List[str]:
    """查询全部操作名称"""
    try:
        res = session.execute(select(Operation.title))

        return res.scalars().all()
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return []


def recode_operation(session: Session, uid: int, oid: int):
    """
    记录用户的操作记录数据
    :param session:
    :param uid:
    :param oid:
    :return:
    """
    if 0 < oid <= 9:
        save_one_to_db(session, model_class=Recode,
                       data=WriteRecodeModel(uid=uid, oid=oid, create_at=datetime.datetime.now().date()))


def query_recode_by_date_user(session: Session, uid: int, oid: int, min_date: datetime.date,
                              max_date: datetime.date) -> List[Recode]:
    """
    根据日期查询数据
    :param session:
    :param uid: 用户ID
    :param oid: 操作ID
    :param min_date:
    :param max_date:
    :return:
    """
    try:
        result = session.execute(
            select(func.count(Recode.id).label("count"), Recode.create_at).where(
                Recode.oid == oid, Recode.uid == uid, Recode.create_at >= min_date,
                Recode.create_at <= max_date).group_by(Recode.create_at).order_by(Recode.create_at))
        return result.all()
    except Exception as e:
        logging.error(str(e))
        return []


def query_summary_analyse_data(session: Session, uid: int, ):
    """
    获取分析数据的概览
    :param session:
    :param uid:
    """
    temp = {
        "review": {"today": 0, "incr": 0},
        "create": {"today": 0, "incr": 0},
        "category_count": 0
    }
    now = datetime.datetime.now()
    today = now.date()
    yesterday = (now - datetime.timedelta(days=1)).date()

    recode_review_data = session.execute(
        select(func.count(Recode.id).label("count"), Recode.create_at).where(
            Recode.uid == uid, or_(Recode.create_at == today, Recode.create_at == yesterday),
            Recode.oid == settings.OPERATION_DATA["review_card"]).group_by(Recode.create_at))
    for recode_review in recode_review_data.all():
        if recode_review.create_at == today:
            temp["review"]["today"] += recode_review.count
            temp["review"]["incr"] += recode_review.count
        elif recode_review.create_at == yesterday:
            temp["review"]["incr"] -= recode_review.count

    recode_create_data = session.execute(
        select(func.count(Recode.id).label("count"), Recode.create_at).where(
            Recode.uid == uid, or_(Recode.create_at == today, Recode.create_at == yesterday),
            Recode.oid == settings.OPERATION_DATA["create_card"]).group_by(Recode.create_at))

    for recode_create in recode_create_data.all():
        # create
        if recode_create.create_at == today:
            temp["create"]["today"] += recode_create.count
            temp["create"]["incr"] += recode_create.count
        elif recode_create.create_at == yesterday:
            temp["create"]["incr"] -= recode_create.count
    # 获取category
    category_data = session.execute(
        select(func.count(Category.id).label("count")).where(Category.uid == uid)
    )
    category_count = category_data.scalar()
    if category_count:
        temp["category_count"] = category_count
    return temp


def update_user_profile_data(session: Session, uid: int, data: Dict) -> str:
    """
      更新用户配置

    :param session: 数据连接
    :param uid: 用户id
    :param data: 要要更新的数据
    :return: 异常提示
    """
    try:
        session.execute(
            update(User).where(User.id == uid).values(**data))
        session.commit()
        return ""

    except IntegrityError as e:
        logging.error(str(e))
        session.rollback()
        if e.orig.errno == 1062:
            return "数据已经存在"
        return "未知异常"
    except Exception as e:
        logging.error(str(e))
        session.rollback()
        return "未知异常"
