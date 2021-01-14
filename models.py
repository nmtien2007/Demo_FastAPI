from sqlalchemy import Column, Integer, SmallInteger, String, BigInteger, TypeDecorator, MetaData
from database import Base


class CustomerBoolean(TypeDecorator):

    impl = SmallInteger

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = 1 if value is True else 0

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = True if value == 1 else False
        return value

class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData()


class OtherBase(Base):
    __abstract__ = True
    metadata = MetaData()

class ApplicationTab(DefaultBase):
    __tablename__ = "application_tab"

    id = Column(BigInteger, primary_key=True, index=True)
    app_name = Column(String(50))
    client_id = Column(String(100), nullable=False)
    client_secret = Column(String(200), nullable=False)
    redirect_url = Column(String(500))
    algorithm = Column(String(10), default="HS256")
    enable_sso = Column(CustomerBoolean, default=False)
    # is_deleted = Column(SmallInteger, default=0)
    is_deleted = Column(CustomerBoolean, default=False)
    created_time = Column(Integer)
    updated_time = Column(Integer)

class AccessTokenTab(DefaultBase):
    __tablename__ = "access_token_tab"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(2000), nullable=False)
    expired_time = Column(Integer, default=0)
    app_id = Column(Integer, nullable=False)
    created_time = Column(Integer, nullable=False)
    updated_time = Column(Integer, nullable=False)

class UserInfoTab(DefaultBase):
    __tablename__ = "user_info_tab"

    id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    password = Column(String)
    salt_key = Column(String(100))
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    # is_deleted = Column(SmallInteger, default=0)
    is_deleted = Column(CustomerBoolean, default=False)
    created_time = Column(Integer)
    updated_time = Column(Integer)

class SsoSessionTab(DefaultBase):
    __tablename__ = "sso_session_tab"

    id = Column(BigInteger, primary_key=True, index=True)
    session_id = Column(String(500), nullable=False, default="")
    session = Column(String(2000), nullable=False, default="")
    user_id = Column(Integer, nullable=False)
    expired_time = Column(Integer, nullable=False, default=0)
    created_time = Column(Integer, nullable=False)
    updated_time = Column(Integer, nullable=False)
