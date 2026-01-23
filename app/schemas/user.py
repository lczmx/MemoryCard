from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator


# from service.database import SessionLocal
class SessionLocal:
    pass


class ParamsSignUpModel(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        """
        比对两次密码
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


class DBUserModel(WriteSignUpModel):
    """数据库模型"""
    id: int
