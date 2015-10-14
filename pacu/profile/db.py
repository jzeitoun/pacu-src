import tempfile

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

def get_scoped(engine):
    from pacu.ext.sqlalchemy.orm import session
    return session.get_scoped(engine)

def default(profile):
    interpolated = profile.formatter.format(**vars(profile))
    engine = create_engine(interpolated, echo=profile.echo.bool)
    engine.__pacu_protect__ = profile.PROTECT.bool
    return get_scoped(engine)

def _create_sqlite_engine(uri, echo):
    return create_engine(uri, echo=echo,
        connect_args = dict(check_same_thread=False),
        poolclass = StaticPool)

def ephemeral(profile):
    from pacu.util import identity
    resource = identity.formattempfile('%s-db-engine-ephemeral.db')
    engine = _create_sqlite_engine(profile.uri + resource, profile.echo.bool)
    engine.__pacu_protect__ = profile.PROTECT.bool
    return get_scoped(engine)

def memory(profile):
    from pacu.core.model import fixture
    engine = _create_sqlite_engine(profile.uri, profile.echo.bool)
    engine.echo = False
    engine.__pacu_protect__ = profile.PROTECT.bool
    s = get_scoped(engine)
    fixture.base.setup(s)
    engine.echo = profile.echo.bool
    return s

def interim(profile):
    return memory(profile)
