from pacu.util.path import Path
from pacu.profile import manager
from pacu.core.io.scanbox.view.sbx import ScanboxSBXView
from pacu.core.io.scanbox.view.mat import ScanboxMatView
from pacu.core.io.scanbox.channel import ScanboxChannel
from pacu.core.io.scanbox.model import db

opt = manager.instance('opt')

class ScanboxIO(object):
    session = None
    channel = None
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.io')
        self.Session = db.get_sessionmaker(self.dbpath)
    @property
    def is_there(self):
        return self.path.exists()
    @property
    def dbpath(self):
        return self.path.joinpath('db.sqlite3').absolute()
    @property
    def sessions(self):
        try:
            return self.read_session()
        except:
            return []
    def set_session(self, id):
        self.session = self.query_session(id=id).one()
        return self
    def get_session(self, id):
        return self.Session().query(db.Session).get(id)
    def query_session(self, **filter_by):
        return self.Session().query(db.Session).filter_by(**filter_by)
    def create_session(self, **payload):
        session = self.Session()
        session.add(db.Session(**payload))
        session.commit()
    def delete_session(self, id):
        session = self.Session()
        session.query(db.Session).filter_by(id=id).delete()
        session.commit()
    def read_session(self, **fby):
        return self.query_session(**fby).order_by(db.Session.id.desc()).all()
    @property
    def mat(self):
        return ScanboxMatView(self.path.with_suffix('.mat'))
    @property
    def sbx(self):
        return ScanboxSBXView(self.path.with_suffix('.sbx'))
    @property
    def meta(self):
        return dict(
            hops = self.path.relative_to(opt.scanbox_root).parts,
            path = self.path.str,
            exists = self.is_there,
            mat = self.mat,
            sbx = self.sbx,
            sessions = self.sessions if self.is_there else [])
    def get_channel(self, number):
        return ScanboxChannel(self.path.joinpath('{}.chan'.format(number)))
    def set_channel(self, number):
        self.channel = self.get_channel(number)
        return self
    def remove_io(self):
        self.path.rmtree()
        return self.meta
    def import_raw(self):
        self.path.mkdir()
        db.SQLite3Base.metadata.create_all(self.Session.kw.get('bind'))
        for chan in range(self.mat.channels):
            self.get_channel(chan).import_with_io(self)
        return self.meta
    def delete_roi(self, id):
        s = self.Session()
        s.delete(s.query(db.ROI).get(id))
        s.commit()
        s.close()
    def upsert_roi(self, payload):
        s = self.Session()
        pl = {key: payload[key]
            for key in db.ROI.__mapper__.c.keys()
            if key in payload}
        roi = db.ROI(session_id=self.session.id, **pl)
        roi = s.merge(roi)
        s.commit()
        data = {key: getattr(roi, key) for key in ['id'] + payload.keys()}
        s.close()
        return data
    def fetch_trace(self, roi_id, trace_id, category):
        s = self.Session()
        print 'ROI ID', roi_id
        print 'TRACE ID', trace_id
        roi = s.query(db.ROI).get(roi_id)
        array = roi.get_trace(self.channel.mmap)
        trace = db.Trace(id=trace_id, roi_id=roi_id, array=array, category=category)
        trace = s.merge(trace)
        s.commit()
        data = dict(array=trace.array, id=trace.id,
                category=trace.category,
                roi_id=trace.roi_id, created_at=trace.created_at)
        s.close()
        return data


# from pacu.dep.json import best as json
# from pacu.core.io.scanbox.model import session
# import numpy as np
# testpath = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_120_006.io'
# io = ScanboxIO(testpath).set_session(1).set_channel(0)
# io = ScanboxIO(testpath)
# noiopath = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_000_003.io'
# nosess = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_020_002.io'
# io = ScanboxIO(nosess)

# CREATE one big detailed global `relationship.py` it will define all ordered import and relationship


class sessionBinder(type):
    @classmethod
    def bind(mcl, session, orm):
        return mcl('SessionBound{}'.format(orm.__name__),
            (object, ), dict(db=session, orm=orm))
    def __call__(cls, *args, **kwargs):
        return cls.orm(*args, **kwargs)
    def get(cls, id):
        with cls.db.begin(): # as transaction
            return cls.db.query(cls.orm).get(id)
    create = NotImplemented
    read = NotImplemented
    update = NotImplemented
    delete = NotImplemented
    all = NotImplemented
    one = NotImplemented
    one_or_none = NotImplemented
    first = NotImplemented
    add = NotImplemented
    add_all = NotImplemented
    query = NotImplemented

class SessionBoundNamespace(object):
    def __init__(self, session, *orms):
        self.__dict__.update({
            orm.__name__: sessionBinder.bind(session, orm)
            for orm in orms})
# session = SessionBoundNamespace(io.Session(), db.Session, db.ROI)


def fixture(io):
    db.recreate(io.dbpath)
    session = io.Session()
    trace = db.Trace(category='df/f0')
    roi = db.ROI(polygon=[
        {'x':1,   'y':1},
        {'x':111, 'y':1},
        {'x':111, 'y':111},
        {'x':1,   'y':111},
    ], traces=[trace])
    session.add_all([
        db.Session(name=u"my first session", rois=[roi]),
        db.Session(name=u"my awesome session"),
    ])
    session.commit()
    session.close()

def ScanboxIOFetcher(base, io_name, session_id):
    root = manager.instance('opt').scanbox_root
    path = Path(root).joinpath(base, io_name)
    return ScanboxIO(path).set_session(session_id).set_channel(0)

# io = ScanboxIOFetcher('jc6', 'jc6_1_120_006.io', 1)




























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











# print s.record.toDict()

#     @property
#     def datetime(self):
#         return datetime.fromtimestamp(
#             float(self.tiffpath.stem))
#     @property
#     def tiffpath(self):
#         return self.path.with_suffix('.tif')
#     def toDict(self):
#         return dict(exists=self.exists, path=self.path.str, sessions=self.sessions)
#     @memoized_property
#     def tiff(self):
#         tiffpath = self.path.with_suffix('.tif')
#         file_size = tiffpath.lstat().st_size
#         print 'Import from {}...'.format(tiffpath)
#         print 'File size {:,} bytes.'.format(file_size)
#         return tifffile.imread(tiffpath.str)
#     def create_package_path(self):
#         self.path.mkdir()
#         print 'Path `{}` created.'.format(self.path.str)
#     def remove_package(self):
#         shutil.rmtree(self.path.str)
#         return self.toDict()
#     @memoized_property
#     def channel(self):
#         tfilter = self.session.opt.get('filter')
#         if tfilter:
#             if tfilter._indices is not None:
#                 return TrajectoryChannel(self.path.joinpath('channel')
#                     ).set_indices(tfilter._indices)
#         return TrajectoryChannel(self.path.joinpath('channel'))
#     @property
#     def sessions(self):
#         return map(TrajectorySession, sorted(self.path.ls('*.session')))
#     @memoized_property
#     def session(self):
#         return TrajectorySession(
#             self.path.joinpath(self.session_name).with_suffix('.session'))
#     @session.invalidator
#     def set_session(self, session_name):
#         self.session_name = session_name
#         return self
#     @memoized_property
#     def alog(self): # aligned log in JSON format
#         return [
#             dict(e=e, x=x, y=y, v=v)
#             for e, x, y, v in self.channel.alog[['E', 'X', 'Y', 'V']]]
#     @property
#     def main_response(self):
#         return TrajectoryResponse(self.channel.stat.MEAN)
#     def upsert_roi(self, roi_kwargs):
#         return self.session.roi.upsert(ROI(**roi_kwargs))
#     def upsert_filter(self, filter_kwargs):
#         tfilter = TrajectoryFilter(**filter_kwargs)
#         tfilter._indices = tfilter.make_indices(self.channel.original_velocity)
#         rv = self.session.opt.upsert(tfilter)
#         for roi in self.session.roi.values():
#             roi.invalidated = True
#         self.session.roi.save()
#         return rv
#     def make_response(self, id):
#         roi = self.session.roi[id]
#         extras = self.session.roi.values()
#         extras.remove(roi)
#         main_trace, main_mask = roi.trace(self.channel.mmap)
#         neur_trace, neur_mask = roi.neuropil_trace(self.channel.mmap, extras)
#         trace = main_trace - neur_trace*0.7
#         roi.invalidated = False
#         roi.response = TrajectoryResponse(trace)
#         return self.session.roi.upsert(roi)
#     @memoized_property
#     def velocity_stat(self):
#         return dict(
#             max = self.channel.alog.V.max(),
#             mean = self.channel.alog.V.mean(),
#             min = self.channel.alog.V.min(),
#         )
