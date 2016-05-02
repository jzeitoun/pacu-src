from pacu.core.io.scanbox.model.session import Session
from pacu.core.io.scanbox.model.roi import ROI
from pacu.core.io.scanbox.model.trace import Trace
from pacu.core.io.scanbox.model.base import SQLite3Base

def get_sessionmaker(dbpath):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///{}'.format(dbpath), echo=True)
    return sessionmaker(engine, autocommit=True)

# Session = sessionmaker(bind=engine, autocommit=True)
# session = Session()
# with session.begin():
#     item1 = session.query(Item).get(1)
#     item2 = session.query(Item).get(2)
#     item1.foo = 'bar'
#     item2.bar = 'foo'

def recreate(dbpath):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///{}'.format(dbpath), echo=True)
    SQLite3Base.metadata.drop_all(engine)
    SQLite3Base.metadata.create_all(engine)
