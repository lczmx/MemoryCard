"""
用户相关路由
"""

from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pymysql.err import IntegrityError

import settings
from service.schemas.user import DBUserModel, ParamsSignUpModel, ReadUserModel, JWTModel, UserProfileModel
from service.schemas.generic import GenericResponse
from service.models import User
from dependencies.auth import jwt_authenticate_user, create_access_token, jwt_get_current_user

router = APIRouter(prefix="/user", tags=["用户相关"])


@router.get("/", response_model=GenericResponse[ReadUserModel])
async def get_user(user: DBUserModel = Depends(jwt_get_current_user)):
    """获取当前用户的数据"""
    return {
        "status": 1,
        "msg": "获取成功",
        "data": user

    }


@router.post("/signup", response_model=GenericResponse[ReadUserModel], response_model_exclude_unset=True)
async def signup(sign_up_data: ParamsSignUpModel):
    """
    注册用户
    """
    # 哈希秘钥

    data = {
        "username": sign_up_data.username,
        "email": sign_up_data.email,
        "hashed_pwd": settings.pwd_context.hash(sign_up_data.password1)

    }
    error_res = {}
    if await User.objects.filter(username=sign_up_data.username).first():
        error_res["username"] = "用户名已经存在"

    if await User.objects.filter(email=sign_up_data.email).first():
        error_res["email"] = "邮箱已经存在"

    if error_res:
        return JSONResponse({"status": 0, "msg": "注册失败", "data": error_res})

    # 保存数据
    await User.objects.create(**data)

    return {
        "status": 1,
        "msg": "注册成功",
        "data": data
    }


@router.post('/token', response_model=GenericResponse[JWTModel])
async def get_token(user: DBUserModel = Depends(jwt_authenticate_user)):
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
    return {"status": 1, "msg": "登录成功", "data": data}


@router.post("/profile", response_model=GenericResponse[UserProfileModel])
async def update_user_profile(user_profile: UserProfileModel, user: DBUserModel = Depends(jwt_get_current_user)):
    """
    修改用户配置
    """

    uid = user.id
    data = user_profile.dict(exclude_unset=True, exclude_defaults=True)
    if not data:
        return {"status": 0, "msg": "数据不能为空", "data": data}

    try:
        await User.objects.filter(pk=uid).update(**data)
        return {"status": 1, "msg": "修改成功", "data": data}
    except IntegrityError:
        return {"status": 0, "msg": "数据已经存在", "data": data}
