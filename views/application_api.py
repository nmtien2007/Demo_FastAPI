from sqlalchemy.orm import Session
from api_response_data import api_response_data
from manager import application_manager
from form_schema import RegisterAppSchema, UpdateAppSchema
from utils import parse_params, pre_process_header
from headers import PreLoginHeader


@parse_params(PreLoginHeader, RegisterAppSchema)
@pre_process_header()
def register_application(request, data, db: Session):
    app_name = data["app_name"]
    redirect_url = data.get("redirect_url", "")
    algorithm = data.get("algorithm", "HS256")
    enable_sso = data.get("enable_sso", False)

    # check application is existed or not
    app_model = application_manager.get_application_info_by_app_name(app_name, db)
    if app_model:
        return api_response_data("error_application_existed")
    affected_count = application_manager.register_application(
        db, app_name=app_name, redirect_url=redirect_url, algorithm=algorithm, enable_sso=enable_sso
    )

    return api_response_data("success", {"affected_count": affected_count})

@parse_params(PreLoginHeader, UpdateAppSchema)
@pre_process_header()
def update_application(request, data, db: Session):
    app_id = data["id"]
    app_name = data.get("app_name", None)
    redirect_url = data.get("redirect_url", None)
    algorithm = data.get("algorithm", None)
    enable_sso = data.get("enable_sso", None)

    app_info = application_manager.get_application_info_by_app_id(app_id, db)
    if not app_info:
        return api_response_data("error_application_not_existed")

    affected_count = application_manager.update_application(
        db=db, app_id=app_id, app_name=app_name, redirect_url=redirect_url, algorithm=algorithm, enable_sso=enable_sso
    )
    return api_response_data("success", {"affected_count": affected_count})
