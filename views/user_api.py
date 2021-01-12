from sqlalchemy.orm import Session
from api_response_data import api_response_data
from manager import user_manager
from form_schema import CreateUserSchema, GetUserInfosSchema, GetUserIdsSchema
from utils import parse_params, pre_process_header, verify_access_token
from headers import PreLoginHeader, LoginHeader


@parse_params(PreLoginHeader, CreateUserSchema)
@pre_process_header()
def create_user(request, data, db: Session):
    affected_count = user_manager.create_user_info(
        data["user_name"], data["password"], data["full_name"], data["email"], data["phone"]
        , db
    )
    return api_response_data("success", {"affected_count": affected_count})

@parse_params(LoginHeader, GetUserIdsSchema)
@pre_process_header()
@verify_access_token()
def get_user_ids(request, data, db: Session):
    user_name = data.get("user_name", None)
    email = data.get("email", None)
    phone = data.get("phone", None)

    user_ids = user_manager.filter_user_infos(db, user_name, email=email, phone=phone)

    return api_response_data("success", {"user_ids": user_ids})

@parse_params(LoginHeader, GetUserInfosSchema)
@pre_process_header()
@verify_access_token()
def get_user_infos(request, data, db: Session):
    user_ids = data["user_ids"]
    user_infos = user_manager.get_user_infos_by_ids(user_ids, db)
    ls_data = []
    if user_infos:
        for info in user_infos:
            ls_data.append({
                "id": info.id,
                "user_name": info.user_name,
                "full_name": info.full_name,
                "email": info.email,
                "phone": info.phone,
                "is_deleted": info.is_deleted,
                "created_time": info.created_time,
                "updated_time": info.updated_time
            })

    return api_response_data("success", {"user_infos": ls_data})
