from fastapi import Depends, Request
from sqlalchemy.orm import Session
from api_response_data import api_response_data
from manager import user_manager, login_manager, token_manager, session_manager, application_manager
from form_schema import LoginSchema, VerifyAuthorizationCode, LoginSsoSchema
from utils import parse_params, pre_process_header, get_header, get_timestamp
from headers import PreLoginHeader, LoginHeader


@parse_params(PreLoginHeader, LoginSchema)
@pre_process_header()
def login(request, data, db: Session):
    user_info = user_manager.get_user_info_by_user_name(data["user_name"], db)
    if not user_info:
        return api_response_data("error_user_not_existed", {})

    # check password
    if user_manager.check_password_user(data["password"], user_info.password):
        url = login_manager.generate_authorization_code(
            app_id=data["app_id"],
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            redirect_url=data["redirect_url"],
            user_info=user_info,
            algorithm=data["algorithm"],
            db=db
        )
        return api_response_data("success", {"redirect_url": url})

    return api_response_data("error_password_not_correct", None)

def authorization(request: Request, header=Depends(PreLoginHeader)):
    from fastapi.templating import Jinja2Templates

    templates = Jinja2Templates(directory="templates")
    
    return templates.TemplateResponse(
        "new_login.html",
        {
            "request": request,
            "client_id": header.Client_Id,
            "auth_code": header.Authorization_Code
        }
    )

@parse_params(PreLoginHeader, VerifyAuthorizationCode)
@pre_process_header()
def verify_authorization_code(request, data, db: Session):
    state = data["state"]
    code = data["code"]
    if code != login_manager.get_authorization_code(state):
        return api_response_data("error_auth_code_incorrect")

    user_id = int(state.split("_")[0])
    user_info = user_manager.get_user_info_by_user_id(user_id, db)
    if not user_info:
        return api_response_data("error_user_not_existed")

    token_obj = login_manager.get_token_obj(
        data["app_id"], data["client_id"], data["client_secret"], data["redirect_url"], user_info, data["algorithm"], db
    )

    return api_response_data("success", {"token_obj": token_obj})

@get_header(LoginHeader)
@pre_process_header()
def logout(request, data, db: Session):
    token_id = data["_session"]["token_id"]
    token_manager.update_user_access_token(token_id, "", 0, db)
    return api_response_data("success")

@parse_params(PreLoginHeader, LoginSsoSchema)
@pre_process_header()
def login_sso(request, data, db: Session):
    session_id = data["session_id"]
    user_id = int(str(session_id).split("@")[0])

    user_info = user_manager.get_user_info_by_user_id(user_id, db)
    if not user_info:
        return api_response_data("error_user_not_existed")

    client_ids = application_manager.get_list_enable_sso_client_ids(db)

    if data["client_id"] not in client_ids:
        return api_response_data("error_application_not_enable_sso")

    sso_session_obj = session_manager.get_session_by_user_id(user_id, db)
    if not sso_session_obj:
        return api_response_data("error_sso_session_not_found")

    if sso_session_obj.expired_time < get_timestamp():
        return api_response_data("error_sso_session_expired")

    token_obj = login_manager.get_token_obj(
        data["app_id"], data["client_id"], data["client_secret"], data["redirect_url"], user_info, data["algorithm"], db
    )

    return api_response_data("success", {"token_obj": token_obj})
