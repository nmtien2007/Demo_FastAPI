from sqlalchemy.orm import Session
from utils import get_timestamp
import models

def get_access_token(user_id, app_id, db: Session):
    model = db.query(models.AccessTokenTab).filter(
        models.AccessTokenTab.user_id == user_id,
        models.AccessTokenTab.app_id == app_id
    ).first()

    return model

def create_new_access_token(user_id, token, app_id, expired_time, db: Session):
    created_time = updated_time = get_timestamp()
    try:
        db_token = models.AccessTokenTab(
            user_id=user_id,
            access_token=token,
            expired_time=expired_time,
            app_id=app_id,
            created_time=created_time,
            updated_time=updated_time
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return 1
    except:
        return 0

def update_user_access_token(token_id, token, expired_time, db: Session):
    updated_time = get_timestamp()
    model = db.query(models.AccessTokenTab).filter(models.AccessTokenTab.id == token_id).first()
    if not model:
        return 0
    try:
        model.access_token = token
        model.expired_time = expired_time
        model.updated_time = updated_time
        db.commit()
        db.flush()
        return 1
    except:
        return 0




