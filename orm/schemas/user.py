from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from orm.crud import query_user_username_exists, query_user_email_exists
from orm.database import SessionLocal


class ParamsSignUpModel(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str

    @validator('username')
    def is_username_exists(cls, v, **kwargs):
        with SessionLocal() as session:
            # 跳过已经有的
            exists = query_user_username_exists(session=session, username=v)
            if exists:
                raise ValueError('用户名已经存在')
        return v

    @validator('email')
    def is_email_exists(cls, v, **kwargs):
        with SessionLocal() as session:
            # 跳过已经有的
            exists = query_user_email_exists(session=session, email=v)
            if exists:
                raise ValueError('邮箱已经存在')
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        """
        :param v: 当前字段的值: zxcvbn2
        :param values: 已经验证的数据: {'username': 'scolvin', 'password1': 'zxcvbn'}
        :param kwargs: {'field': ModelField(name='password2', type=str, required=True),
                            'config': <class '__main__.Config'>}
        :return:
        """
        if 'password1' in values and v != values['password1']:
            raise ValueError('两次密码不一致')
        return v


class WriteSignUpModel(BaseModel):
    username: str
    email: EmailStr
    hashed_pwd: str
    phone_number: Optional[str] = None


class ReadUserModel(BaseModel):
    username: str
    email: EmailStr
    phone_number: str = Field(None, alias="phoneNumber")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class JWTModel(BaseModel):
    access_token: str = Field("", alias="accessToken")
    token_type: str = Field("", alias="tokenType")

    class Config:
        allow_population_by_field_name = True  # 使用字段名设置数据


class UserProfileModel(BaseModel):
    username: str = Field("")
    email: EmailStr = Field("")
