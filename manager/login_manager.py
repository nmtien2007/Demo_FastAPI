from manager import open_id_connect_manager, user_manager, token_manager
from sqlalchemy.orm import Session
from utils import decrypt_access_token, get_timestamp


def generate_authorization_code(app_id, client_id, client_secret, redirect_url, user_info, algorithm, db: Session):
    data = {
        "app_id": app_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_url": redirect_url,
        "user_info": user_info,
        "algorithm": algorithm,
        "db": db
    }

    open_id_model = open_id_connect_manager.get_grant_type(1, data)
    return open_id_model.generate_authorization_code()

def get_authorization_code(state):
    import memcache

    cache_obj = memcache.Client([('127.0.0.1', 11211)])
    cache_key = "authorization_code_%s" % state
    code = cache_obj.get(cache_key)
    return code

def get_token_obj(app_id, client_id, client_secret, redirect_url, user_info, algorithm, db: Session):
    data = {
        "app_id": app_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_url": redirect_url,
        "user_info": user_info,
        "algorithm": algorithm,
        "db": db
    }
    open_id_model = open_id_connect_manager.get_grant_type(1, data)
    open_id_model.generate_access_token()
    open_id_model.generate_id_token()
    open_id_model.get_token_obj()
    return open_id_model.get_token_obj()

def check_access_token(access_token, app_id, client_id, client_secret, algorithm, db: Session):
    is_valid = True
    result_code = "success"
    object_data = decrypt_access_token(
        access_token[str(access_token).index(" ") + 1:], client_id, client_secret, algorithms=[algorithm]
    )
    if not object_data:
        is_valid = False
        result_code = "error_access_token_incorrect"

    else:
        user_info = user_manager.get_user_info_by_user_id(object_data["user_id"], db)
        if not user_info:
            is_valid = False
            result_code = "error_user_not_existed"

        user_token = token_manager.get_access_token(object_data["user_id"], app_id, db)
        if not user_token or access_token[str(access_token).index(" ") + 1:] != user_token.access_token:
            is_valid = False
            result_code = "error_access_token_incorrect"
        else:
            current_ts = get_timestamp()
            if user_token.expired_time == 0 or current_ts > user_token.expired_time:
                is_valid = False
                result_code = "error_access_token_expired"

            object_data["token_id"] = user_token.id

    return is_valid, result_code, object_data
