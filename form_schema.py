from typing import Optional
from pydantic import BaseModel, validator
from typing import List


class LoginSchema(BaseModel):
    user_name: str
    password: str

    # @validator("user_name")
    # def validate_user_name(cls, name):
    #     if not isinstance(name, str):
    #         raise ValueError('user name must be string')
    #     return name
    #
    # @validator("password")
    # def validate_password(cls, password):
    #     if not isinstance(password, str):
    #         raise ValueError('password must be string')
    #     return password

class CreateUserSchema(LoginSchema):
    full_name: str
    email: str
    phone: str

class GetUserIdsSchema(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class GetUserInfosSchema(BaseModel):
    user_ids: List[int]

class RegisterAppSchema(BaseModel):
    app_name: str
    redirect_url: Optional[str] = None
    algorithm: Optional[str] = None
    enable_sso: Optional[bool] = None

class VerifyAuthorizationCode(BaseModel):
    state: str
    code: str

class LoginSsoSchema(BaseModel):
    session_id: str

class UpdateAppSchema(BaseModel):
    id: int
    app_name: Optional[str] = None
    redirect_url: Optional[str] = None
    algorithm: Optional[str] = None
    enable_sso: Optional[bool] = None
