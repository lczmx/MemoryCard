"""
认证相关依赖
"""
from typing import Optional, Union
from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from orm.crud import query_account_by_username_or_email, query_user_by_id
from orm.models import User
from dependencies.orm import get_session
import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    生成jwt token
    :param data:
    :param expires_delta: 过期时间
    :return:
    """
    # data => payload
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    # 标准中注册的声明 过期时间
    to_encode.update({"exp": expire})

    # jwt.encode 的参数
    # claims     指定payload
    # key        指定signature的加密秘钥
    # algorithm  指定signature的加密算法
    encoded_jwt = jwt.encode(claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def jwt_authenticate_user(session: Session = Depends(get_session),
                          form_data: OAuth2PasswordRequestForm = Depends()) -> Union[User, None]:
    """
    检验jwt是否合法
    获取当前用户
    :param session:
    :param form_data:  jwt表单
    :return:
    """

    # 到数据库中获取
    user_lst = query_account_by_username_or_email(session=session, username=form_data.username,
                                                  email=form_data.username)
    # 检验密码是否合法
    for user in user_lst:
        # 假如通过, 则符合用户对象
        if settings.pwd_context.verify(form_data.password, user.hashed_pwd):
            return user
    return None


async def jwt_get_current_user(session: Session = Depends(get_session),
                               token: str = Depends(settings.oauth2_schema)) -> User:
    """
    根据jwt获取用户
    通过 OAuth2PasswordBearer 获得
    """
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 获取 数据

        # decode jwt token
        # 得到payload, 即 create_access_token 中的 to_encode
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        uid = payload.get("uid")
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = query_user_by_id(session=session, uid=uid)
    if not user:
        raise credentials_exception
    return user
