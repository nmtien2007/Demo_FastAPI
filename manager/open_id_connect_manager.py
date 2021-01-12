from datetime import datetime, timedelta
import uuid
import jwt
import config
from manager import token_manager, session_manager
from utils import get_timestamp, generate_authorization_code, convert_datetime_to_timestamp


class AuthorizationModel(object):
    def __init__(self, data):
        self.db = data["db"]
        self.app_id = data["app_id"]
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]
        self.algorithm = data["algorithm"]
        self.redirect_url = data["redirect_url"]
        self.scopes = data.get("scopes", ["openid", "profile", "email"])
        self.authorization_code = data.get("authorization_code", "")
        self.user_info = data.get("user_info", None)
        self.iss = data.get("iss", config.ISS)
        self.basic_object = None
        self.access_token = None
        self.id_token = None
        self.session_id = None
        self.refresh_token = None
        self.user_id = self._set_user_id()
        self.sso_session_obj = self._get_sso_session_obj()
        self.user_token = self._get_user_token()
        self.data_obj = self._generate_data_obj()

    # def _get_application_info_by_client_id(self):
    #     return application_manager.get_application_info_by_client_id(self.client_id, self.db)

    def _set_user_id(self):
        user_id = self.user_info.id
        return user_id

    def _generate_data_obj(self):
        data = {
            "iat": get_timestamp(),
            "jti": str(uuid.uuid1()),
            "iss": self.iss
        }
        return data

    def _get_sso_session_obj(self):
        session_obj = session_manager.get_session_by_user_id(self.user_id, self.db)
        return session_obj

    def get_token_obj(self):
        token_obj = {
            "token_type": "Bearer",
        }

        if self.access_token:
            token_obj["access_token"] = "%s %s" % ("Bearer" , self.access_token)

        if self.id_token:
            token_obj["id_token"] = self.id_token

        if self.refresh_token:
            token_obj["refresh_token"] = self.refresh_token

        return token_obj

    def _get_user_token(self):
        user_token = token_manager.get_access_token(self.user_id, self.app_id, self.db)
        return user_token

    def update_user_token(self, expiry_time):
        if not self.user_token:
            token_manager.create_new_access_token(self.user_id, self.access_token, self.app_id, expiry_time, self.db)
        else:
            token_manager.update_user_access_token(self.user_token.id, self.access_token, expiry_time, self.db)

class AuthorizationCodeModel(AuthorizationModel):
    def __init__(self, data):
        super().__init__(data)
        self.cache_key = data.get("cache_key", "authorization_code_%s")
        self.expiry_time = data.get("expiry_time", 60 * 5)  # Expiry time is 5 minutes
        self.cache_name = data.get("cache_name", "default")
        self.auth_code = data.get("authorization_code", "")
        self.nonce = data.get("nonce", None)

    def generate_authorization_code(self):
        nonce = "%s_%s" % (str(self.user_id), str(get_timestamp()))
        authorization_code = generate_authorization_code()
        self.cache_key = self.cache_key % nonce

        query_params = "/?state=%s&code=%s" % (nonce, authorization_code)
        self.redirect_url += query_params
        try:
            import memcache

            cache_obj = memcache.Client([('127.0.0.1', 11211)])
            cache_obj.set(self.cache_key, authorization_code, self.expiry_time)

        except Exception as err:
            print(err)

        return self.redirect_url

    def generate_access_token(self):
        current_ts = get_timestamp()
        if self.user_token and self.user_token.expired_time > current_ts:
            self.access_token = self.user_token.access_token
        else:
            expiry_time = convert_datetime_to_timestamp(datetime.now() + timedelta(hours=8))
            user_name = self.user_info.user_name
            user_id = self.user_info.id
            email = self.user_info.email

            data = self.data_obj
            data["subject"] = email[0: email.index("@")]
            data["aud"] = [self.client_id]
            data["user_id"] = user_id
            data["client_id"] = self.client_id
            data["user_name"] = user_name

            try:
                self.access_token = jwt.encode(data, self.client_secret, algorithm=self.algorithm)
            except Exception as err:
                print(err)

            # Update the access token of user
            self.update_user_token(expiry_time)

    def generate_id_token(self):
        data = self.data_obj
        email = self.user_info.email
        user_id = self.user_info.id
        phone = self.user_info.phone

        data["user_id"] = user_id

        if "profile" in self.scopes:
            data["phone"] = phone

        if 'email' in self.scopes:
            data["email"] = email

        # SSO Session
        if self.sso_session_obj:
            # check expiry time
            if self.sso_session_obj.expired_time > get_timestamp():
                self.session_id = self.sso_session_obj.session_id
            else:
                self.session_id, session = session_manager.generate_sso_session(
                    self.user_info, self.client_id
                )

                expired_time = convert_datetime_to_timestamp(datetime.now() + timedelta(hours=2))
                session_manager.update_session(self.user_id, session, expired_time, self.db)
        else:
            self.session_id, session = session_manager.generate_sso_session(
                self.user_info, self.client_id
            )

            expired_time = convert_datetime_to_timestamp(datetime.now() + timedelta(hours=2))
            session_manager.create_new_session(
                self.user_id, self.session_id, session, expired_time, self.db
            )

        data["session_id"] = self.session_id

        self.id_token = jwt.encode(data, self.client_secret, self.algorithm)

GRANT_TYPE = {
    1: AuthorizationCodeModel
}

def get_grant_type(grant_type, data):
    """
    :param data:
    :param grant_type:
    :return: Grant type Model
    """
    model = GRANT_TYPE.get(grant_type)
    return model(data)
