from __future__ import division

import numpy as np

from pacu.util.path import Path
from pacu.profile import manager
from pacu.core.io.scanbox.view.sbx import ScanboxSBXView
from pacu.core.io.scanbox.view.mat import ScanboxMatView
from pacu.core.io.scanbox.view.ephys import ScanboxEphysView
from pacu.core.io.scanbox.channel import ScanboxChannel
from pacu.core.io.scanbox.model import db

opt = manager.instance('opt')

class sessionBinder(type):
    @classmethod
    def bind(mcl, session, orm):
        return mcl('SessionBound{}'.format(orm.__name__),
            (object, ), dict(session=session, orm=orm))
    def __call__(cls, *args, **kwargs):
        return cls.orm(*args, **kwargs)
    @property
    def queried(cls):
        return cls.session.query(cls.orm)
    def get(cls, id):
        return cls.queried.get(id)
    def all(cls):
        return cls.queried.all()
    def one(cls, **kwargs):
        return cls.queried.filter_by(**kwargs).one()
    def one_or_none(cls, **kwargs):
        return cls.queried.filter_by(**kwargs).one_or_none()
    def first(cls):
        return cls.queried.first()
    # direct SQL command
    def create(cls, payload):
        with cls.session.begin() as t:
            inst = cls(**payload)
            cls.session.add(inst)
            return inst
    def delete(cls, payload):
        return cls.queried.filter_by(**payload).delete()
    def upsert(cls, payload):
        with cls.session.begin() as t:
            roi = t.session.merge(cls(**payload))
            t.session.flush()
            return {key: getattr(roi, key) for key in payload.keys()}
    read = NotImplemented
    def __dir__(self):
        return ['queried', 'get', 'all', 'one',
            'one_or_none', 'first', 'create',
            'read', 'upsert', 'delete']

class SessionBoundNamespace(object):
    """
    session = SessionBoundNamespace(session, db.Session, db.ROI)
    """
    def __init__(self, session, *orms):
        self._session = session
        self.__dict__.update({
            orm.__name__: sessionBinder.bind(session, orm)
            for orm in orms})
    def __enter__(self):
        return self._session, self._session.begin()
    def __exit__(self, *args):
        print 'SESSION BOUND NAMESPACE __EXIT__'
        print args

from sqlalchemy import event

class ScanboxIO(object):
    session = None
    channel = None
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.io')
        self.session = SessionBoundNamespace(
            self.db_session_factory(),
            db.Workspace, db.ROI, db.Trace)
    @property
    def is_there(self):
        return self.path.exists()
    @property
    def db_path(self):
        return self.path.joinpath('db.sqlite3').absolute()
    @property
    def db_session_factory(self):
        maker = db.get_sessionmaker(self.db_path)
        # sessionmaker can configure without bind(engine)
        # so setup event first. it's doable.
        # event.remove(maker, 'before_attach', db.SQLite3Base.before_attach)
        event.listen(maker, 'before_flush', db.before_flush)
        event.listen(maker, 'after_commit', db.after_commit)

        return maker
    def set_workspace(self, id):
        self.workspace_id = id
        return self
    @property
    def workspace(self):
        return self.session.Workspace.one_or_none(id=self.workspace_id)
    @property
    def mat(self):
        return ScanboxMatView(self.path.with_suffix('.mat'))
    @property
    def sbx(self):
        return ScanboxSBXView(self.path.with_suffix('.sbx'))
    @property
    def ephys(self):
        return ScanboxEphysView(self, self.path.with_suffix('.txt'))
    @property
    def attributes(self):
        error = None
        try:
            workspaces = self.session.Workspace.all()
        except Exception as e:
            notable = 'no such table' in str(e)
            nocolumn = 'no such column' in str(e)
            workspaces = []
            error = dict(notable=notable, nocolumn=nocolumn,
                    detail=str(e), type=type(e).__name__)
        return dict(
            hops = self.path.relative_to(opt.scanbox_root).parts,
            path = self.path.str,
            is_there = self.is_there,
            mat = self.mat,
            sbx = self.sbx,
            error = error,
            mode = 'uni' if self.mat.scanmode else 'bi',
            workspaces = workspaces)
    def get_channel(self, number):
        return ScanboxChannel(self.path.joinpath('{}.chan'.format(number)))
    def set_channel(self, number):
        self.channel = self.get_channel(number)
        return self
    def remove_io(self):
        self.path.rmtree()
        self.session = SessionBoundNamespace( # unnecessary implementation
            self.db_session_factory(),
            db.Workspace, db.ROI, db.Trace)
        return self.attributes
    def import_raw(self):
        self.path.mkdir_if_none()
        db.recreate(self.db_path)
        for chan in range(self.mat.nchannels):
            self.get_channel(chan).import_with_io(self)
        return self.attributes
    def upgrade_db_schema(self):
        db.upgrade(db.SQLite3Base.metadata,
            self.db_session_factory.kw.get('bind'))
        return self.attributes



# from pacu.profile import manager
# from pacu.core.model.experiment import ExperimentV1
# db = manager.instance('db')
# s = manager.get('db').section('glab')()

# from matplotlib.pyplot import *
# get_ipython().magic(u'pylab')
# 
# testpath = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jzg1/day_ht/my4r_1_3_000_007.io'
# io = ScanboxIO(testpath)

# testpath = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jzg1/day1/day3_022_000.io'

# io = ScanboxIO(testpath).set_workspace(3).set_channel(0)
# w = io.workspace
# r1 = w.rois[0]
# r2 = w.rois[1]
# io = ScanboxIO(testpath)

# import matplotlib
# matplotlib.use('svg')
# from matplotlib import pyplot
# fig = pyplot.figure(figsize=(20, 4))
# plt = fig.add_subplot(111)
# plt.plot(io.ephys.trace, linewidth=0.5)
# fig.savefig('ephys.pdf', bbox_inches='tight')

# ep = io.workspace.ecorrs.first
# from sqlalchemy.orm import load_only
# s = io.db_session_factory()
# entities = s.query(db.find_orm(table.name)).options(load_only(*ref_cols)).all()


# io = ScanboxIO(testpath).set_workspace(1).set_channel(0)
# r = io.workspace.rois[0]
# w = io.workspace
# t = io.workspace.rois[0].traces[0]



# risings = risings[:len(io.channel.mmap)]
# np.save(wavenpy, risings)

# first_frame = find_nth_rising(raw['TTL'])
# last_frame = int(np.ceil(io.mat.duration * 20000))
# data = raw[first_frame:first_frame+last_frame]
# ds = data[::len(data)//len(io.channel.mmap)]
# resampled = signal.resample(data['ON'], len(io.channel.mmap))
# np.save(wavenpy, resampled)
# data = np.load(wavenpy)
# iomean = io.channel.stat['MEAN']

# from pacu.core.io.scanbox.model import session
# import numpy as np

# import ujson
# from sqlalchemy import inspect

# t = io.session.Trace.all()[4]
# rels = inspect(type(t)).relationships
# roirel = rels['roi']

# io = ScanboxIO(testpath)
# no = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_000_003.io'
# no = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_020_002.io'
# io = ScanboxIO(no)


# from sqlalchemy import inspect
# Session = db.get_sessionmaker('')
# event.listen(Session, 'after_begin', db.after_begin)
# event.listen(Session, 'before_flush', db.before_flush)
# event.listen(Session, 'after_flush', db.after_flush)
# event.listen(Session, 'after_commit', db.after_commit)
# event.listen(Session, 'after_rollback', db.after_rollback)
# s = Session()
# s.bind.engine.echo = False
# s.begin()
# trace = db.Trace(category=u'df/f0', array=[1,2,3])
# roi = db.ROI(polygon=[
#     {'x':1,   'y':1},
#     {'x':111, 'y':1},
#     {'x':111, 'y':111},
#     {'x':1,   'y':111},
# ], traces=[trace])
# # ri = inspect(roi)
# s.add(roi)
# s.commit()
# s.begin()
# roi.polygon = roi.polygon[1:]
# roi.active = True
# s.commit()
# print 'ROI', roi.__committed_attrs__
# print 'TRACE', roi.traces[0].__committed_attrs__

def fixture(io):
    db.recreate(io.db_path)
    with io.session as (s, t):
        roi1 = db.ROI(polygon=[
            {'x':1,   'y':1},
            {'x':111, 'y':1},
            {'x':111, 'y':111},
            {'x':1,   'y':111},
        ], traces=[db.Trace(category='df/f0')])
        # roi2 = db.ROI(polygon=[
        #     {'x':210, 'y':201},
        #     {'x':321, 'y':201},
        #     {'x':311, 'y':311},
        #     {'x':210, 'y':311},
        # ], traces=[db.Trace(category='df/f0')])
        t.session.add_all([
            db.Workspace(
                name=u"main",
                iopath=testpath,
                colormaps=[db.Colormap(), db.Colormap()],
                rois=[roi1]),
        ])
        s.commit()
    with io.session as (s, t):
        s.add(db.Action(
            model_name = u'Trace',
            model_id = 1,
            action_name = u'refresh',
        ))
        s.commit()

def ScanboxIOFetcher(mouse, day, io_name, workspace_id):
    root = manager.instance('opt').scanbox_root
    path = Path(root).joinpath(mouse, day, io_name)
    return ScanboxIO(path).set_workspace(workspace_id).set_channel(0)
#     x, y, _, z = sbx.shape
#     rgb = np.zeros((z, y, x, 3), dtype=sbx.io.dtype)
#     if nchan == 2:
#         rgb[..., 1] = ~sbx.ch0
#         rgb[..., 0] = ~sbx.ch1
#     elif nchan == 1:
#         rgb[..., 1] = ~sbx.ch0
#     tiffpath = sbx.path.with_name('tiff').mkdir_if_none()
#     dest = tiffpath.joinpath(sbx.path.name).with_suffix('.tiff')
#     tifffile.imsave(dest.str, rgb)
