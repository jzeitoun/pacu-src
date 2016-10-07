import ujson
from sqlalchemy import event
from sqlalchemy.orm import object_session

from pacu.util.path import Path
from pacu.util import identity
from pacu.util.prop.memoized import memoized_property
from pacu.profile import manager

from pacu.core.io.scanbox.view.sbx import ScanboxSBXView
from pacu.core.io.scanbox.view.mat import ScanboxMatView
from pacu.core.io.scanbox.channel import ScanboxChannel
from pacu.core.io.scanbox.model import db as schema
from pacu.core.model.experiment import ExperimentV1

opt = manager.instance('opt')
glab = manager.get('db').section('glab')
userenv = identity.path.userenv

class ScanboxIO(object):
    def __init__(self, path):
        self.path = userenv.joinpath('scanbox', path).ensure_suffix('.io')
        self.db_path = self.path.joinpath('db.sqlite3').absolute()
        self.mat_path = opt.scanbox_root.joinpath(path).with_suffix('.mat')
        self.sbx_path = opt.scanbox_root.joinpath(path).with_suffix('.sbx')
    @property
    def mat(self):
        return ScanboxMatView(self.mat_path)
    @property
    def sbx(self):
        return ScanboxSBXView(self.sbx_path)
    def remove_io(self):
        self.path.rmtree()
    def import_raw(self, condition_id=None):
        if self.path.is_dir():
            raise OSError('{} already exists!'.format(self.path))
        else:
            self.path.mkdir_if_none()
        print 'Converting raw data...'
        for nchan in range(self.mat.nchannels):
            ScanboxChannel(self.path.joinpath('{}.chan'.format(nchan))
            ).import_with_io(self)
        print 'Initialize local database...'
        self.initialize_db(condition_id)
        print 'Done!'
        return self.toDict()
    @memoized_property
    def sessionmaker(self):
        maker = schema.get_sessionmaker(self.db_path, echo=False)
        event.listen(maker, 'before_flush', schema.before_flush)
        event.listen(maker, 'after_commit', schema.after_commit)
        return maker
    @memoized_property
    def db_session(self):
        return self.sessionmaker()
    def initialize_db(self, condition_id=None):
        # requires original location...
        schema.recreate(self.db_path, echo=False)
        session = self.db_session
        with session.begin():
            condition = schema.Condition(info=self.mat.toDict())
            session.add(condition)
        if condition_id:
            self.import_condition(condition_id)
    def import_condition(self, id):
        session = self.db_session
        exp = glab().query(ExperimentV1).get(id)
        try:
            with session.begin():
                condition = session.query(schema.Condition).one()
                condition.from_expv1(exp)
                condition.trials.extend([
                    schema.Trial.init_and_update(**trial)
                    for trial in exp])
                condition.imported = True
                condition.exp_id = int(id)
                session.add(condition)
        except Exception as e:
            print 'Condition import failed with reason below,', str(e)

    @memoized_property
    def condition(self):
        # Session = schema.get_sessionmaker(self.db_path, echo=False)
        return self.db_session.query(schema.Condition).one()
    @memoized_property
    def ch0(self):
        return ScanboxChannel(self.path.joinpath('0.chan'))
    @memoized_property
    def ch1(self):
        return ScanboxChannel(self.path.joinpath('1.chan'))
    def toDict(self):
        try:
            return dict(info=self.condition.info,
                    has_condition = self.condition.imported,
                workspaces=[ws.name for ws in self.condition.workspaces])
        except Exception as e:
            if 'no such column' in str(e):
                self.fix_db_schema()
                print 'Fixing DB Schema'
                return dict(info=self.condition.info, dbfixed=True,
                        has_condition = self.condition.imported,
                    workspaces=[ws.name for ws in self.condition.workspaces])
            err = dict(type=str(type(e)), detail=str(e))
            return dict(err=err, info=self.mat.toDict())
    def fix_db_schema(self):
        meta = schema.SQLite3Base.metadata
        bind = self.db_session.bind
        schema.fix_incremental(meta, bind)
#        session = self.condition.object_session
#         session.begin()
#         for ws in self.condition.workspaces:
#             for roi in ws.rois:
#                 print roi.initialize_datatags()
#        session.commit()
    def echo_on(self):
        self.db_session.bind.engine.echo=True
        return self
    def echo_off(self):
        self.db_session.bind.engine.echo=False
        return self
    @classmethod
    def iter_every_io(cls):
        return (cls(path) for path in userenv.joinpath('scanbox').rglob('*.io'))


# import cv2
# import numpy as np
# import time
# 
# # q = ScanboxIO('day_ht/Aligned_day1_000_001.io').echo_off()
# 
# def trace(frames, mask):
#     return np.stack(cv2.mean(frame, mask)[0] for frame in frames)
# 
# def test_m0(io, index=0):
#     r = io.condition.workspaces.first.rois[index]
#     cnt = r.contours
#     shape = io.ch0.shape
# 
#     frames = np.memmap(io.ch0.mmappath.str,
#         mode='r', dtype=io.ch0.meta.dtype, shape=shape)
# 
#     mask = np.zeros(shape[1:], dtype='uint8')
#     cv2.drawContours(mask, [cnt], 0, 255, -1)
#     x, y, w, h = cv2.boundingRect(np.array([cnt]))
# 
#     small_frames = frames[:, y:y+h, x:x+w]
#     small_cnt = cnt - [x, y]
#     small_mask = np.zeros(small_frames.shape[1:], dtype='uint8')
#     cv2.drawContours(small_mask, [small_cnt], 0, 255, -1)
#     print (mask > 0).sum(), (small_mask > 0).sum(), len(cnt)
#     s = time.time()
#     print 'result', trace(frames, mask).sum()
#     print time.time() - s
# 
# def test_m1(io, index=0):
#     r = io.condition.workspaces.first.rois[index]
#     cnt = r.contours
#     shape = io.ch0.shape
# 
#     frames = np.memmap(io.ch0.mmappath.str,
#         mode='r', dtype=io.ch0.meta.dtype, shape=shape)
# 
#     mask = np.zeros(shape[1:], dtype='uint8')
#     cv2.drawContours(mask, [cnt], 0, 255, -1)
#     x, y, w, h = cv2.boundingRect(np.array([cnt]))
# 
#     small_frames = frames[:, y:y+h, x:x+w]
#     small_cnt = cnt - [x, y]
#     small_mask = np.zeros(small_frames.shape[1:], dtype='uint8')
#     cv2.drawContours(small_mask, [small_cnt], 0, 255, -1)
#     print (mask > 0).sum(), (small_mask > 0).sum(), len(cnt)
#     s = time.time()
#     print 'result', trace(small_frames, small_mask).sum()
#     print time.time() - s








# import numpy as np
# import ujson
# q = ScanboxIO('day_ht/day5_003_020.io') # 638
# q = ScanboxIO('Kirstie/day1_000_002.io').echo_on() # 70
# qwe = glab()().query(ExperimentV1).get(923)
# exp = glab().query(ExperimentV1).get(997)
# q = ScanboxIO('day_ht/Aligned_dm27_000_000.io') # aligned
# w = q.condition.workspaces.first
# r = q.condition.workspaces.first.rois.first
# a = r.dtorientationsmeans.first
# import cv2
# import numpy as np
# from matplotlib.pyplot import *
# from matplotlib.patches import Rectangle
# get_ipython().magic('pylab')
# 
# # q = ScanboxIO('day_ht/my4r_1_3_000_007.io').echo_off()

# import os
# import time
# print 'purge disk cache', os.system('sudo purge')
# 
# 
# q = ScanboxIO('Kirstie/ka28/day1/day1_000_002.io')
# # q = ScanboxIO('day_ht/Aligned_day1_000_001.io').echo_off()
# # q = ScanboxIO('day_ht/my4r_1_3_000_007.io').echo_off()
# r = q.condition.workspaces.first.rois.first
# cnt = r.contours
# frames = q.condition.io.ch0.mmap # going 8bit does not help
# shape = frames.shape[1:]
# mask = np.zeros(shape, dtype='uint8')
# cv2.drawContours(mask, [cnt], 0, 255, -1)
# x, y, w, h = cv2.boundingRect(np.array([cnt]))
# 
# b_frames = frames[::, y:y+h, x:x+w] # down sampling also could work for large
# print 'FRAME LENGTH', len(b_frames)
# b_mask = mask[y:y+h, x:x+w]
# 
# def trace2(frames, mask):
#     s = time.time()
#     rv = np.array([cv2.mean(frame, mask)[0] for frame in frames], dtype='float64')
#     print 'ELAPSED:', time.time() - s
#     return rv


# f = np.memmap(q.condition.io.ch0.mmappath.str, dtype='uint16')

# gca().invert_yaxis()
# scatter(*zip(*cnt))
# r = Rectangle((x, y), w-1, h-1, fill=False)
# gca().add_artist(r)
# 
# 
# figure()
# 
# gca().invert_yaxis()
# scatter(*zip(*small_cnt))
# r = Rectangle((0, 0), w-1, h-1, fill=False)
# gca().add_artist(r)
# 

# print (mask > 0).sum(), (small_mask > 0).sum(), len(cnt)

def ScanboxIOStream(files): # magic protocol... for damn `files` kwargs
    return ScanboxIO(files)
