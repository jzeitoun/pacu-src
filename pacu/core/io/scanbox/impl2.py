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
    def import_raw(self, cond=None):
        if self.path.is_dir():
            raise OSError('{} already exists!'.format(self.path))
        else:
            self.path.mkdir_if_none()
        print 'Converting raw data...'
        for nchan in range(self.mat.nchannels):
            ScanboxChannel(self.path.joinpath('{}.chan'.format(nchan))
            ).import_with_io(self)
        print 'Create local database...'
        schema.recreate(self.db_path, echo=False)
        if cond and 'id' in cond and cond['id']:
            condition = glab().query(ExperimentV1).get(cond['id'])
            if condition:
                print 'There is matching condition data in ED.'
                print 'Parse and bind condition data..'
                self.import_condition(condition)
            else:
                print 'No matching condition found!'
        print 'Done!'
        return self.toDict()
    @memoized_property
    def sessionmaker(self):
        maker = schema.get_sessionmaker(self.db_path, echo=False)
        event.listen(maker, 'before_flush', schema.before_flush)
        event.listen(maker, 'after_commit', schema.after_commit)
        return maker
    @property
    def db_session(self):
        return self.sessionmaker()
    def import_condition_by_id(self, id):
        schema.recreate(self.db_path, echo=False)
        condition = glab().query(ExperimentV1).get(id)
        self.import_condition(condition)
    def import_condition(self, exp):
        session = self.db_session
        try:
            with session.begin():
                condition = schema.Condition.from_expv1(exp)
                condition.info = self.mat.toDict()
                condition.trials.extend([
                    schema.Trial.init_and_update(**trial)
                    for trial in exp])
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
                workspaces=[ws.name for ws in self.condition.workspaces])
        except Exception as e:
            err = dict(type=str(type(e)), detail=str(e))
            return dict(err=err, info=self.mat.toDict())

# import numpy as np

# q = ScanboxIO('jzg1/day1_000_002.io')
# q.db_session.query(schema.Datatag).filter_by(method='dff0', trial_flicker=False, trial_blank=False).count()
# exp_id = 923
# q = ScanboxIO('jzg1/day_ht/day5_003_020.io')
# w = q.condition.workspaces.first
# r = w.rois.first
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

def ScanboxIOStream(files): # magic protocol...
    return ScanboxIO(files)
