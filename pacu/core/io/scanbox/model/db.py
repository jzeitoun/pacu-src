from pacu.util.path import Path
from pacu.profile import manager
from pacu.core.io.scanbox.model.relationship import *
from pacu.core.io.scanbox.model.base import SQLite3Base
from sqlalchemy import inspect

opt = manager.instance('opt')

def fix_incremental():
    pass

def upgrade(metadata, bind):
    metadata.create_all(bind)
    fix_incremental()

def recreate(dbpath=''):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://{}'.format(
        '/' + str(dbpath) if dbpath else ''
    ), echo=True)
    SQLite3Base.metadata.drop_all(engine)
    SQLite3Base.metadata.create_all(engine)
    return engine

def get_sessionmaker(dbpath, echo=True, **kw):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    path = Path(dbpath)
    engine = create_engine('sqlite:///{}'.format(dbpath),
        echo=echo, **kw) if path.is_file() else recreate('')
    return sessionmaker(engine, autocommit=True)

def Session(mouse, day, ioname):
    """
    dirname = "jc6"
    ioname = "jc6_1_120_006.io"
    sm = sessionmaker(dirname, ioname)
    Session = sm()
    session = Session()
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    dbpath = opt.scanbox_root.joinpath(mouse, day, ioname, 'db.sqlite3')
    engine = create_engine('sqlite:///{}'.format(dbpath), echo=True)
    return sessionmaker(engine, autocommit=True)


def find_orm(tablename):
    return {c.__tablename__: c
            for c in SQLite3Base.__subclasses__()}.get(tablename)

def before_flush(session, flush_context, instances):
    for dirty in session.dirty:
        if hasattr(dirty, 'before_flush_dirty'):
            dirty.before_flush_dirty(session, flush_context)
    for new in session.new:
        if hasattr(new, 'before_flush_new'):
            new.before_flush_new(session, flush_context)
    for deleted in session.deleted:
        if hasattr(deleted, 'before_flush_deleted'):
            deleted.before_flush_deleted(session, flush_context)
def after_flush(session, flush_context):
    print 'AFTER FLUSH'
    for dirty in session.dirty:
        keys = [attr.key for attr in inspect(dirty).attrs
            if attr.history.has_changes()]
        dirty.__flushed_attrs__ = tuple(keys)
        dirty.__committed_attrs__.extend(keys)
def after_begin(session, transaction, connection):
    print 'AFTER BEGIN'
    for model in session.identity_map.values():
        model.__flushed_attrs__ = ()
        model.__committed_attrs__ = []
def after_commit(session):
    print 'AFTER COMMIT'
    for model in session.identity_map.values():
        model.__flushed_attrs__ = ()
        model.__committed_attrs__ = tuple(model.__committed_attrs__)
def after_rollback(session):
    print 'AFTER ROLLBACK'
    for model in session.identity_map.values():
        model.__flushed_attrs__ = ()
        model.__committed_attrs__ = []

SQLite3Base.__flushed_attrs__ = ()
SQLite3Base.__committed_attrs__ = ()
