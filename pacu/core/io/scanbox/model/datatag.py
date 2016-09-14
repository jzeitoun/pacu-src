import runpy
import sys
import traceback
import importlib

from sqlalchemy.sql import func
from sqlalchemy import Column, Unicode, Float, Boolean, Integer, DateTime
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

basemodule = 'pacu.core.io.scanbox.method'

class Datatag(SQLite3Base):
    __tablename__ = 'datatags'
    updated_at = Column(DateTime, onupdate=func.now())
    # exception
    etype = Column(Unicode(128))
    etext = Column(Unicode)
    # dynamic
    value = Column(PickleType, default=None)
    # search criteria
    category = Column(Unicode(128))
    method = Column(Unicode(128))

    # search trials
    trial_on_time = Column(Float)
    trial_off_time = Column(Float)
    trial_ori = Column(Float)
    trial_sf = Column(Float)
    trial_tf = Column(Float)
    trial_sequence = Column(Integer)
    trial_order = Column(Integer)
    trial_ran = Column(Integer)
    trial_flicker = Column(Boolean)
    trial_blank = Column(Boolean)

    def invalidate(self):
        self.value = None
    def refresh(self):
        roi = self.roi
        workspace = roi.workspace
        condition = roi.workspace.condition
        module = '.'.join((basemodule, self.category, self.method))
        try:
            runpy.run_module(module, run_name='__sbx_main__', init_globals=dict(
                workspace=workspace,
                condition=condition,
                roi=roi,
                datatag=self,
            ))
        except Exception as e:
            print '\n======== exception on datatag ========'
            traceback.print_exception(*sys.exc_info())
            print '======== exception on datatag ========\n'
            self.etype = unicode(type(e))
            self.etext = unicode(e)
            raise e
        else:
            self.etype = None
            self.etext = None
        return self
