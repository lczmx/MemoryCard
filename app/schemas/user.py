from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ValidationInfo


class ParamsSignUpModel(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str

    @field_validator('password2')
    @classmethod
    def passwords_match(cls, v, info: ValidationInfo):
        """
        比对两次密码
        """
        if 'password1' in info.data and v != info.data['password1']:
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
    phone_number: Optional[str] = Field(None, alias="phoneNumber")

    class Config:
        from_attributes = True
        validate_by_name = True


class JWTModel(BaseModel):
    access_token: str = Field("", alias="accessToken")
    token_type: str = Field("", alias="tokenType")

    class Config:
        validate_by_name = True  # 使用字段名设置数据


class UserProfileModel(BaseModel):
    username: str = Field("")
    email: EmailStr = Field("")


class DBUserModel(WriteSignUpModel):
    """数据库模型"""
    id: int
