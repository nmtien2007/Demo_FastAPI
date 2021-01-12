from fastapi import Request, Depends, Header
from sqlalchemy.orm import Session
from database import get_db
from api_response_data import api_response_data
from functools import wraps
from manager import application_manager, login_manager
from random import SystemRandom
import time
import jwt


UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

SECRET_KEY_SESSION = "8ddb6af8df74496a868579f824b3bd8e1250c2d7ed67769bb7470ebc0809bda1"

# async def get_body_from_request(request):
#     body = await request.json()
#     return body

def get_header(header_schema):
    def _parse_params(func, *args, **kwargs):
        def _func(request: Request, db: Session = Depends(get_db), header=Depends(header_schema)):
            data = {}
            try:
                data["authorization_code"] = header.Authorization_Code
                data["client_id"] = header.Client_Id
                if hasattr(header, 'Access_Token'):
                    data["access_token"] = header.Access_Token
            except Exception as err:
                return api_response_data("error_header")

            # get application info
            app_info = application_manager.get_application_info_by_client_id(data["client_id"], db)
            if not app_info:
                return api_response_data("error_client_id_incorrect")

            data["app_id"] = app_info.id
            data["redirect_url"] = app_info.redirect_url
            data["client_secret"] = app_info.client_secret
            data["algorithm"] = app_info.algorithm

            return func(request, data, db, *args, **kwargs)

        return _func
    return _parse_params

def parse_params(header_schema, item):
    def _parse_params(func, *args, **kwargs):
        def _func(request: Request, data: item, db: Session = Depends(get_db), header=Depends(header_schema)):
            from fastapi.encoders import jsonable_encoder

            data_body = jsonable_encoder(data)
            return func(request, data_body, db, header, *args, **kwargs)
        return _func
    return _parse_params

def pre_process_header():
    def _pre_process_header(func):
        @wraps(func)
        def _func(request: Request, data, db, header, *args, **kwargs):
            data_body = data
            try:
                data_body["authorization_code"] = header.Authorization_Code
                data_body["client_id"] = header.Client_Id
                if hasattr(header, 'Access_Token'):
                    data_body["access_token"] = header.Access_Token
            except Exception as err:
                return api_response_data("error_header")

            # get application info
            app_info = application_manager.get_application_info_by_client_id(data_body["client_id"], db)
            if not app_info:
                return api_response_data("error_client_id_incorrect")

            data_body["app_id"] = app_info.id
            data_body["redirect_url"] = app_info.redirect_url
            data_body["client_secret"] = app_info.client_secret
            data_body["algorithm"] = app_info.algorithm

            return func(request, data_body, db, *args, **kwargs)
        return _func
    return _pre_process_header

def verify_access_token():
    def _verify_access_token(func):
        def _func(request: Request, data, db, *args, **kwargs):
            if not data.get("access_token"):
                return api_response_data("error_access_token_not_found")

            if "Bearer" not in data["access_token"]:
                return api_response_data("error_access_token_wrong_format")

            is_valid, result_code, object_data = login_manager.check_access_token(
                data["access_token"], data["app_id"], data["client_id"], data["client_secret"], data['algorithm'], db
            )

            if not is_valid or result_code != "success":
                return api_response_data(result_code)

            data["_session"] = object_data
            return func(request, data, db, *args, **kwargs)
        return _func
    return _verify_access_token

def generate_token(length=40, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))

def generate_authorization_code(length=10, chars=UNICODE_ASCII_CHARACTER_SET):
    return generate_token(length, chars)

def get_timestamp():
    return int(time.time())

def convert_datetime_to_timestamp(date_time):
    if not date_time:
        return None
    else:
        return int(date_time.timestamp())

def decrypt_access_token(access_token, client_id, secret_key, algorithms=None):
    if algorithms is None:
        algorithms = ['HS256']
    try:
        decrypted_access_token = jwt.decode(access_token, secret_key, algorithms=algorithms, audience=[client_id])
        return decrypted_access_token
    except Exception as err:
        return {}
