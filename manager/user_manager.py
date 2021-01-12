from sqlalchemy.orm import Session
import time
import bcrypt
import models


def create_user_info(user_name, password, full_name, email, phone, db: Session):
    time_ts = round(int(time.time()))
    password = password
    salt_key = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt_key)
    user_name = user_name
    full_name = full_name
    email = email
    phone = phone
    is_deleted = 0
    created_time = time_ts
    updated_time = time_ts

    try:
        db_user = models.UserInfoTab(
            user_name=user_name,
            password=hash_password.decode("utf-8"),
            salt_key=salt_key.decode("utf-8"),
            full_name=full_name,
            email=email,
            phone=phone,
            is_deleted=is_deleted,
            created_time=created_time,
            updated_time=updated_time
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return 1
    except:
        return 0

def get_user_infos(db: Session):
    return db.query(models.UserInfoTab).all()

def get_user_info_by_user_name(user_name, db: Session):
    model = db.query(models.UserInfoTab).filter(
        models.UserInfoTab.user_name==user_name,
        models.UserInfoTab.is_deleted==0
    ).first()
    return model

def get_user_info_by_user_id(user_id, db: Session):
    model = db.query(models.UserInfoTab).filter(
        models.UserInfoTab.id == user_id,
        models.UserInfoTab.is_deleted == 0
    ).first()
    return model

def check_password_user(pass1, pass2):
    try:
        if bcrypt.checkpw(pass1.encode("utf-8"), pass2.encode("utf-8")):
            return True
    except Exception as err:
        return False

def filter_user_infos(db: Session, user_name=None, phone=None, email=None):
    user_ids = []
    ls_models = db.query(models.UserInfoTab)
    if user_name is not None:
        ls_models = ls_models.filter(models.UserInfoTab.user_name == user_name)
    if phone is not None:
        ls_models = ls_models.filter(models.UserInfoTab.phone == phone)
    if email is not None:
        ls_models = ls_models.filter(models.UserInfoTab.email == email)

    ls_models = ls_models.all()
    if ls_models:
        for item in ls_models:
            user_ids.append(item.id)

    return user_ids

def get_user_infos_by_ids(ids, db: Session):
    return list(db.query(models.UserInfoTab).filter(models.UserInfoTab.id.in_(ids)))
