from pydantic import BaseModel
from typing import Optional


# class CreateUser(BaseModel):
#     is_created: bool
#
# class UserInfo(BaseModel):
#     id: int
#     user_name: str
#     password: str
#     full_name: str
#     email: str
#     phone: str
#     is_deleted: int
#     created_time: int
#     updated_time: int
#
#     class Config:
#         orm_mode: True

class ResponseSchema(BaseModel):
    result_code: str
    reply: Optional[dict] = None

