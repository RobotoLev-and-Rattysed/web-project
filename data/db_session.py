import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

import settings

import os

SqlAlchemyBase = dec.declarative_base()
__factory = None

from .__all_models import *


def global_init():
    global __factory

    if __factory:
        return

    if 'DATABASE_URL' in os.environ:
        database_url = os.environ['DATABASE_URL']
    else:
        database_url = settings.database_url
    print(f"Подключение к базе данных по адресу {database_url}")
    engine = sa.create_engine(database_url,
                              connect_args={'sslmode': 'require'},
                              pool_size=20,
                              echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
