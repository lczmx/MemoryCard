"""
用户相关路由
"""

from datetime import timedelta, datetime

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from orm.schemas.user import ParamsSignUpModel, WriteSignUpModel, ReadUserModel, JWTModel
from dependencies.orm import get_session
from dependencies.auth import jwt_authenticate_user, create_access_token
from orm.schemas.generic import GenericResponse
from orm.crud import save_one_to_db
from orm.models import User
import settings

router = APIRouter(prefix="/user", tags=["用户相关"])


@router.get("/")
async def index():
    return {"index": "username"}


@router.post("/signup", response_model=GenericResponse[ReadUserModel], response_model_exclude_unset=True)
async def signup(sign_up_data: ParamsSignUpModel, session: Session = Depends(get_session)):
    """
    注册用户
    """
    # 哈希秘钥

    data = {
        "username": sign_up_data.username,
        "email": sign_up_data.email,
        "hashed_pwd": settings.pwd_context.hash(sign_up_data.password1)

    }

    user = save_one_to_db(session=session, model_class=User, data=WriteSignUpModel(**data))
    return {
        "status": 1,
        "msg": "注册成功",
        "data": user
    }


@router.post('/token', response_model=GenericResponse[JWTModel])
async def get_token(user: User = Depends(jwt_authenticate_user)):
    """
    获取token
    :return:
    """
    # 判断账户或密码是否正确
    if not user:
        return {
            "status": 0,
            "msg": "账号或密码错误",
            "data": {}
        }
    payload = {
        "sub": user.username,
        "uid": user.id,
        "email": user.email,
        "phoneNumber": user.phone_number,
    }
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=payload, expires_delta=access_token_expires)
    data = {"access_token": access_token, "token_type": "bearer"}
    return {
        "status": 1,
        "msg": "登录成功",
        "data": data
    }
