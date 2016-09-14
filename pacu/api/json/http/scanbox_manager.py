import ujson

from datetime import timedelta
from datetime import datetime
from pacu.util.path import Path
from pacu.profile import manager
from pacu.util import identity
from pacu.core.model.experiment import ExperimentV1 as EXPV1
from pacu.core.io.scanbox.model import db as schema
from pacu.core.io.scanbox.impl2 import ScanboxIO

opt = manager.instance('opt')
glab = manager.get('db').section('glab')

class Location(object):
    def __init__(self, path):
        self.path = path
    @property
    def json(self):
        return self.__json__()
    def __json__(self):
        return dict(root=self.path.str, exists=self.path.is_dir())

try:
    datastore = Location(opt.scanbox_root)
    workspace = Location(identity.path.userenv.joinpath('scanbox'))
    datastore.path.mkdir_if_none()
    workspace.path.mkdir_if_none()
except Exception as e:
    print e


class DataStoreLocator(object):
    def __init__(self, path, glob='*', delta=timedelta(180)):
        self.path = Path(path).resolve()
        self.glob = glob
        self.delta = delta
        self.now = datetime.now()
    def item_is_within(self, item):
        return self.now - datetime.fromtimestamp(item.stat().st_ctime) < self.delta
    @property
    def items_within(self):
        return (item for item in self.path.glob(self.glob)
            if self.item_is_within(item))
    @property
    def rendered(self):
        sbxs, dirs = [], []
        for item in self.items_within:
            if item.is_dir() and not item.suffix == '.io':
                dirs.append(self.render_dir(item))
            elif item.is_file() and item.suffix == '.sbx' and item.with_suffix('.mat').is_file():
                sbxs.append(self.render_sbx(item))
        return dict(sbxs=sbxs, dirs=dirs)
    def render_dir(self, item):
        return dict(name=item.name, ctime=item.stat().st_ctime)
    def render_sbx(self, item):
        return dict(name=item.stem, ctime=item.stat().st_ctime,
                path=item.str, size=item.size.str)

def get_path(req):
    return dict(
        datastore=datastore.json,
        workspace=workspace.json,
        datastore_nav='/api/json/scanbox_manager/nav_ds',
        workspace_nav='/api/json/scanbox_manager/nav_ws',
    )

def get_nav_ds(req, hops, glob, days):
    path = datastore.path.joinpath(*hops.split(','))
    locator = DataStoreLocator(path, glob, timedelta(int(days)))
    return locator.rendered

def get_conditions(req):
    try:
        query = glab().query(
            EXPV1.id, EXPV1.created_at, EXPV1.keyword, EXPV1.duration
        ).order_by(EXPV1.created_at.desc())
        # .filter_by(clock_clsname='LabJackClock')
        return [entity._asdict() for entity in query]
    except Exception as e:
        print 'Database not working', e
        return []

def get_ios(req):
    dataset = []
    for path in workspace.path.rglob('**/*.io'):
        try:
            data = ScanboxIO(path.relative_to(workspace.path)).toDict()
        except Exception as e:
            print path, e
        else:
            dataset.append(data)
    return dataset
    # return [ScanboxIO(path.relative_to(workspace.path)).toDict()
    #     for path in workspace.path.rglob('**/*.io')]

def delete_io(req, iopath):
    io = ScanboxIO(iopath)
    io.path.resolve()
    io.remove_io()

def post_workspace(req, iopath, name):
    io = ScanboxIO(iopath)
    io.path.resolve()
    session = io.db_session
    with session.begin():
        condition = session.query(schema.Condition).one()
        ws = schema.Workspace(name=name, condition=condition)
        ws.cur_sfreq = condition.sfrequencies[0]
        session.add(ws)
    return dict(name=name)

def delete_workspace(req, iopath, name):
    io = ScanboxIO(iopath)
    io.path.resolve()
    session = io.db_session
    with session.begin():
        ws = session.query(schema.Workspace).filter_by(name=name).one()
        session.delete(ws)
