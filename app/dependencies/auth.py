"""
认证相关依赖
"""
from typing import Optional, Union
from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

import settings
from service.models import User


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


async def jwt_authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Union[User, None]:
    """
    检验jwt是否合法
    获取当前用户

    :param form_data:  jwt表单
    :return:
    """

    # 到数据库中获取

    username_lst = await User.objects.filter(username=form_data.username).all()
    # 检验密码是否合法
    valid_user = verify_user_lst_pwd(username_lst, form_data.password)
    if valid_user and valid_user.active:
        return valid_user

    email_lst = await User.objects.filter(email=form_data.username).all()
    valid_user = verify_user_lst_pwd(email_lst, form_data.password)
    if valid_user and valid_user.active:
        return valid_user
    return None


def verify_user_lst_pwd(user_lst, pwd):
    for user in user_lst:
        if settings.pwd_context.verify(pwd, user.hashed_pwd):
            return user


async def jwt_get_current_user(token: str = Depends(settings.oauth2_schema)) -> User:
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
    user = await User.objects.filter(pk=uid, active=True).first()
    # 必须active为true
    if not user or not user.active:
        raise credentials_exception
    return user
