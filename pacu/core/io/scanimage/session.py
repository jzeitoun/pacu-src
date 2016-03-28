from datetime import datetime
import shutil

import ujson

from pacu.util.path import Path
from pacu.util.inspect import repr
from pacu.util.prop.memoized import memoized_property
from pacu.profile import manager
from pacu.core.model.ed.visstim2p import VisStim2P
from pacu.core.model.analysis import AnalysisV1
from pacu.core.io.scanimage.nmspc import HybridNamespace

ED = manager.get('db').section('ed')()
# print 'dev overide: pacu.core.io.scanimage.session'
class ScanimageSession(object):
    roi = None
    opt = None
    __repr__ = repr.auto_strict
    def __init__(self, path):
        self.path = Path(path).with_suffix('.session')
        self.package, self.mouse, self.date, self.user = self.path.parts[::-1][1:5]
        self.roi = HybridNamespace.from_path(self.path.joinpath('roi'))
        self.opt = HybridNamespace.from_path(self.path.joinpath('opt'))
    def toDict(self):
        return dict(name=self.path.stem, path=self.path.str)
    def query_experiment_db(self):
        return ED().query(VisStim2P).filter_by(
            date=self.datetime.date(),
            filename=self.package.rstrip('.imported'))
    @property
    def datetime(self):
        return datetime.strptime(self.date, '%Y.%m.%d')
    @memoized_property
    def ed(self):
        # return Path('ed.2015.12.02.bV1_Contra_004.pickle').load_pickle()
        return self.query_experiment_db().one()
    @property
    def has_ed(self):
        return bool(self.query_experiment_db().count())
    @property
    def exists(self):
        return self.path.is_dir()
    def create(self):
        self.path.mkdir()
    def remove(self):
        shutil.rmtree(self.path.str)

# testpath = 'tmp/Dario/2015.12.02/x.151101.2/bV1_Contra_004.imported/main.session'
# qwe = ScanimageSession(testpath)
