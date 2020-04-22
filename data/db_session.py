import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

import os

SqlAlchemyBase = dec.declarative_base()
__factory = None

from .__all_models import *


def global_init():
    global __factory

    if __factory:
        return

    print(f"Подключение к базе данных по адресу {os.environ['DATABASE_URL']}")
    engine = sa.create_engine(os.environ['DATABASE_URL'],
                              connect_args={'sslmode': 'require'},
                              echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
