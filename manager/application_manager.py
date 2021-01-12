from sqlalchemy.orm import Session
import models
import time
import random

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


def generate_token(length=40, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))


def generate_client_id(length=7):
    min_length = pow(10, length - 1)
    max_length = pow(10, length) - 1
    random_number = random.randint(min_length, max_length)
    return str(random_number)


def generate_client_secret(length=40, chars=UNICODE_ASCII_CHARACTER_SET):
    current_ts = round(int(time.time()))
    chars += str(current_ts)
    return generate_token(length, chars)


def get_application_info_by_app_name(app_name, db: Session):
    model = db.query(models.ApplicationTab).filter(models.ApplicationTab.app_name == app_name).first()
    return model


def get_application_info_by_client_id(client_id, db: Session):
    model = db.query(models.ApplicationTab).filter(models.ApplicationTab.client_id == client_id).first()
    return model


def register_application(db: Session, app_name, redirect_url=None, algorithm="HS256", enable_sso=False):
    redirect_url = redirect_url if redirect_url is not None else ""
    client_id = generate_client_id()
    client_secret = generate_client_secret()
    created_time = round(int(time.time()))
    updated_time = created_time
    is_deleted = 0

    try:
        app = models.ApplicationTab(
            app_name=app_name,
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            algorithm=algorithm,
            enable_sso=enable_sso,
            is_deleted=is_deleted,
            created_time=created_time,
            updated_time=updated_time
        )
        db.add(app)
        db.commit()
        db.refresh(app)

        return 1
    except:
        return 0

def get_list_enable_sso_client_ids(db: Session):
    client_ids = list(map(lambda x: x[0], db.query(models.ApplicationTab.client_id).filter(
        models.ApplicationTab.is_deleted == False,
        models.ApplicationTab.enable_sso == True
    ).all()))

    return client_ids
