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
            err = dict(type=str(type(e)), detail=str(e))
            return dict(err=err, info=self.mat.toDict())
    def fix_db_schema(self):
        meta = schema.SQLite3Base.metadata
        bind = self.db_session.bind
        schema.fix_incremental(meta, bind)

# import numpy as np
# q = ScanboxIO('day_ht/day5_003_020.io') # 638
# r = q.condition.workspaces.first.rois.first
# a = r.dtorientationsmeans.first

# q.initialize_db(638)
# q = ScanboxIO('day_ht/my4r_1_3_000_035.io')

# q = ScanboxIO('day1_000_002.io')
# r = q.condition.workspaces.first.rois.first
# w = q.condition.workspaces.first
# ipr = w.rois.first
# a = [
#     [np.array(rep.value['on']).mean() for rep in reps]
#     for sf, oris in r.dt_ori_by_sf.items()
#     for ori, reps in oris.items()
# ]

# a = r.dt_fit_diffof.refresh()

# r.dt_best_preferred.refresh()
# r.dt_overall.refresh()
# s = object_session(q.condition)
# s.bind.echo = True
# s.begin()
# s.add(schema.ROI(workspace=q.condition.workspaces.first))
# s.flush()
def ScanboxIOStream(files): # magic protocol... for damn `files` kwargs
    return ScanboxIO(files)

# from pacu.core.io.scanbox.model import minimalbase as mb
# old = '/Volumes/Users/ht/dev/current/pacu/tmp/legacydb/Kirstie/ka28/day1/Aligned_day1_000_002.io/db.sqlite3'
# engine = mb.create_engine('sqlite:///{}'.format(old), echo=True)
# session = mb.sessionmaker(engine)()

# [r.polygon for r in session.query(mb.ROI).order_by(mb.ROI.id).all()]
