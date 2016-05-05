from pacu.util.path import Path
from pacu.core.io.scanbox.model.relationship import *
from pacu.core.io.scanbox.model.base import SQLite3Base

def recreate(dbpath=''):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://{}'.format(
        '/' + str(dbpath) if dbpath else ''
    ), echo=True)
    SQLite3Base.metadata.drop_all(engine)
    SQLite3Base.metadata.create_all(engine)
    return engine

def get_sessionmaker(dbpath):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    path = Path(dbpath)
    engine = create_engine('sqlite:///{}'.format(dbpath),
        echo=True) if path.is_file() else recreate('')
    return sessionmaker(engine, autocommit=True)
