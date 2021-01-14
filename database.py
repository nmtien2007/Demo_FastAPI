from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session


# DATABSE_URL = "mysql+mysqlconnector://root:12345678@localhost:3306/Fast_Api"
#
# engine = create_engine(DATABSE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# # Dependency
# def get_db():
#     db = None
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

DATABASE_URLS = {
    "master": "mysql+mysqlconnector://root:12345678@localhost:3306/Fast_Api",
    "slave": "mysql+mysqlconnector://root:12345678@localhost:3306/Fast_Api",
}

engines = {
    'master': create_engine(DATABASE_URLS["master"]),
    'slave': create_engine(DATABASE_URLS["slave"]),
}

Base = declarative_base()

class RoutingSession(Session):

    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return engines[self._name]
        else:
            return engines['master']

    _name = None

    def using_bind(self, name="master"):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s

def get_db():
    db = None
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, class_=RoutingSession))
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
