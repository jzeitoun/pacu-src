import shutil
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
        path = self.db_path
        print 'fix', path
        shutil.copy2(path.str, path.with_suffix('.backup.sqlite3').str)
        meta = schema.SQLite3Base.metadata
        bind = self.db_session.bind
        schema.fix_incremental(meta, bind)
    def echo_on(self):
        self.db_session.bind.engine.echo=True
        return self
    def echo_off(self):
        self.db_session.bind.engine.echo=False
        return self
    @classmethod
    def iter_every_io(cls):
        return (cls(path) for path in userenv.joinpath('scanbox').rglob('*.io'))
    @classmethod
    def fix_db_schema_all(cls):
        meta = schema.SQLite3Base.metadata
        for io in ScanboxIO.iter_every_io():
            io.fix_db_schema()
            # bind = io.condition.object_session.bind
            # schema.fix_incremental(meta, bind)
    def export_sfreqfit_data_as_mat(self, wid, rid, contrast):
        roi = self.db_session.query(schema.ROI
            ).filter_by(id=rid, workspace_id=wid).one()
        return roi.export_sfreqfit_data_as_mat(contrast)
    @staticmethod
    def condition_by_file(filename='db.sqlite3'):
        Session = schema.get_sessionmaker(filename)
        s = Session()
        condition = s.query(schema.Condition).one()
        return s, condition
    def compute_all_rois_of_all_workspaces(self):
        for ws in self.condition.workspaces:
            for roi in ws.rois:
                try:
                    roi.refresh_all()
                except Exception as e:
                    print 'ERROR', e

"""
for io in ScanboxIO.iter_every_io():
    print io.db_path
    fix_contrasts_schema(upgrade_sqlite(io.db_path))
"""

def open_sqlite(path):
    return schema.get_sessionmaker(path, echo=False)

def upgrade_sqlite(path):
    import shutil
    path = Path(path)
    Session = open_sqlite(path.str)
    meta = schema.SQLite3Base.metadata
    bind = Session.kw.get('bind')
    shutil.copy2(path.str, path.with_suffix('.backup.sqlite3').str)
    schema.fix_incremental(meta, bind)
    return Session

def fix_contrasts_schema(Session):
    from sqlalchemy.orm import load_only
    session = Session()
    condition = session.query(schema.Condition).options(load_only('id')).one()
    contrast = condition.contrast
    if not condition.exp_id:
        print 'no cond, return'
        return
    exp = glab().query(ExperimentV1).get(condition.exp_id)
    ct = exp.stimulus_kwargs.get('contrast')
    cts = exp.stimulus_kwargs.get('contrasts')
    print ct, cts
    if ct:
        condition.contrast = ct
        condition.contrasts = [ct]
    if cts:
        condition.contrasts = cts
    for ws in session.query(schema.Workspace):
        ws.cur_contrast = contrast
        for roi in ws.rois:
            for dt in roi.dttrialdff0s:
                dt.trial_contrast = contrast
            for dt in roi.dtorientationsmeans:
                dt.trial_contrast = contrast
            for dt in roi.dtorientationbestprefs:
                dt.trial_contrast = contrast
            for dt in roi.dtorientationsfits:
                dt.trial_contrast = contrast
            for dt in roi.dtanovaeachs:
                dt.trial_contrast = contrast
            for dt in roi.dtsfreqfits:
                dt.trial_contrast = contrast
            for dt in roi.dtanovaalls:
                dt.trial_contrast = contrast
    for t in session.query(schema.Trial):
        t.contrast = condition.contrast
    condition.object_session.begin()

import re
import numpy as np
from matplotlib import pyplot
# import ujson
# qwe = glab()().query(ExperimentV1).get(1087)
# get_ipython().magic('pylab')
def plot_timing_diff(id=1087):
    qwe = glab()().query(ExperimentV1).get(id)
    asd = map(float,
        [re.match(r'(?P<num>[\d\.]+)\s.*', line).groupdict().get('num')
            for line in qwe.message.splitlines() if 'Entering' in line])
    ps = [e-asd[0] for e in asd]
    lj = [t.get('on_time') for t in qwe.ordered_trials]
    delayinfo = ('{} sec took to show the '
        'first trial after synchronization').format(lj[0])
    try:
        thediff = np.array(ps) - np.array(lj)
    except Exception as e:
        raise e
    else:
        pyplot.figure()
        pyplot.plot(thediff)
        pyplot.suptitle(qwe.keyword)
        pyplot.title(delayinfo)
        pyplot.ylabel('psychopy - labjack in second')
        pyplot.xlabel('trials in order')

# for io in ScanboxIO.iter_every_io():
#     for ws in io.condition.workspaces:
#         print ws.sog_initial_guess
        # ws.sog_initial_guess = ws.SOG_INITIAL_GUESS
#         print ws.sog_initial_guess
    # io.condition.object_session.begin()

# w = q.condition.workspaces.first
# r = q.condition.workspaces.first.rois.first
# a = r.dtorientationsmeans.first
# import cv2
# import numpy as np
# from matplotlib.pyplot import *
# from matplotlib.patches import Rectangle
# get_ipython().magic('pylab')

# import os
# import time
# print 'purge disk cache', os.system('sudo purge')

# q = ScanboxIO('test_ka50_lit_day1/day1_000_003.io')
# w = q.condition.workspaces.first
# r = w.rois.first
# dt = r.dtorientationsmeans.filter_by(trial_sf=0.12,trial_contrast=1).first
# for ct in q.condition.contrasts:
#     for sf in q.condition.sfrequencies:
#         print sf, ct
#         dt = r.dttrialdff0s.filter_by(
#             trial_sf=sf, trial_contrast=ct,
#             trial_blank=False, trial_flicker=False) #, trial_ori=90.0)
#         print sorted(set([d.trial_sequence for d in dt]))
#         print len(dt)

# dt = r.dttrialdff0s.filter_by(
#     trial_sf=0.12, trial_contrast=1.0,
#     trial_blank=False, trial_flicker=False) #, trial_ori=90.0)
# id_multiple_category = 1475 #1193 previous, single contrast
# debugger_condition_id = 1671
# session = glab()
# exp = session.query(ExperimentV1).get(1811)
# exp = session.query(ExperimentV1).get(debugger_condition_id)

# q = ScanboxIO('debugger/debugger_movie.io')
# q = ScanboxIO('Kirstie/ka28/day1/day1_000_002.io')

# r = q.condition.workspaces.last.rois.first
# fit = r.dtsfreqfit.refresh()
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

def redump(filename):
    """
    redump('2016-10-11_12_05_11.x.160921.1_P19_004_001.pickle')
    """
    import cPickle
    with open(filename, 'rb') as f:
        data = cPickle.load(f)
    print data.keys()
    result = data['result']
    keyword = data['keyword']
    payload = data['payload']
    errormsg = result.pop('errormsg', None)
    errortype = result.pop('errortype', None)
    model = ExperimentV1(**result)
    model.duration = max(t for ts in model.off_time for t in ts)
    model.keyword = keyword
    for key, val in payload.items():
        for attr in 'clsname pkgname kwargs'.split():
            ett_attr = key + '_' + attr
            ett_val = val.get(attr)
            setattr(model, ett_attr, ett_val)
    session = glab()
    session.add(model)
    session.commit()
    return model

# session = glab()
# exp = session.query(ExperimentV1).get(1836)
# c = schema.Condition()
# c.from_expv1(exp)
# c.trials.extend([
#     schema.Trial.init_and_update(**trial)
#     for trial in exp])
# c.imported = True

#     def initialize_db(self, condition_id=None):
#         # requires original location...
#         schema.recreate(self.db_path, echo=False)
#         session = self.db_session
#         with session.begin():
#             condition = schema.Condition(info=self.mat.toDict())
#             session.add(condition)
#         if condition_id:
#             self.import_condition(condition_id)

# condition = session.query(schema.Condition).one()
# condition.from_expv1(exp)
# condition.trials.extend([
#     schema.Trial.init_and_update(**trial)
#     for trial in exp])
# condition.imported = True
# condition.exp_id = int(id)
# session.add(condition)

# condition = schema.Condition()
# condition.from_expv1(exp)
# try:
#     with session.begin():
#         condition = session.query(schema.Condition).one()
#         condition.from_expv1(exp)
#         condition.trials.extend([
#             schema.Trial.init_and_update(**trial)
#             for trial in exp])
#         condition.imported = True
#         condition.exp_id = int(id)
#         session.add(condition)
# except Exception as e:
#     print 'Condition import failed with reason below,', str(e)
