from pacu.util.path import Path
from pacu.profile import manager
from pacu.core.io.scanbox.model.relationship import *
from pacu.core.io.scanbox.model.base import SQLite3Base

opt = manager.instance('opt')

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

def Session(dirname, ioname):
    """
    dirname = "jc6"
    ioname = "jc6_1_120_006.io"
    sm = sessionmaker(dirname, ioname)
    Session = sm()
    session = Session()
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    dbpath = opt.scanbox_root.joinpath(dirname, ioname, 'db.sqlite3')
    engine = create_engine('sqlite:///{}'.format(dbpath), echo=True)
    return sessionmaker(engine, autocommit=True)
