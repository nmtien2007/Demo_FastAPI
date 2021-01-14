from common.logger import log
from sqlalchemy.orm import Session
from utils import get_timestamp, SECRET_KEY_SESSION
import models
import jwt
import uuid


def get_session_by_id(session_id, db: Session):
    model = db.using_bind("slave").query(models.SsoSessionTab).filter(models.SsoSessionTab.session_id == session_id).first()
    return model

def get_session_by_user_id(user_id, db: Session):
    model = db.using_bind("slave").query(models.SsoSessionTab).filter(models.SsoSessionTab.user_id == user_id).first()
    return model

def create_new_session(user_id, session_id, session, expired_time, db: Session):
    created_time = updated_time = get_timestamp()
    try:
        db_token = models.SsoSessionTab(
            session_id=session_id,
            session=session,
            user_id=user_id,
            expired_time=expired_time,
            created_time=created_time,
            updated_time=updated_time
        )
        db = db.using_bind("master")
        db.add(db_token)
        db.commit()
        # db.refresh(db_token)
        return 1
    except Exception as err:
        log.warn("create_new_session_fail|error=%s", err)
        return 0

def update_session(user_id, session, expired_time, db: Session):
    updated_time = get_timestamp()
    model = get_session_by_user_id(user_id, db)
    if not model:
        return 0

    try:
        model.session = session
        model.expired_time = expired_time
        model.updated_time = updated_time
        db = db.using_bind("master")
        db.commit()
        db.flush()
        return 1
    except Exception as err:
        log.warn("update_session_fail|err=%s", err)
        return 0

def generate_sso_session(user_info, client_id, algorithm="HS256"):
    create_time = get_timestamp()
    data = {
        "client_id": client_id,
        "organization": "localhost:8001",
        "user_id": user_info.id,
        "user_name": user_info.user_name,
        "create_time": create_time
    }

    session_id = "%s@%s" % (str(user_info.id), str(uuid.uuid4()))
    data["session_id"] = session_id

    session = jwt.encode(data, SECRET_KEY_SESSION, algorithm=algorithm)
    return session_id, session

