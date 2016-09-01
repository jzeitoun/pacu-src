import runpy
import importlib

from sqlalchemy import Column, Unicode, Float, Boolean, Integer
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

basemodule = 'pacu.core.io.scanbox.method'

class Datatag(SQLite3Base):
    __tablename__ = 'datatags'
    # exception
    etype = Column(Unicode(128))
    etext = Column(Unicode)
    # dynamic
    value = Column(PickleType, default=None)
    # search criteria
    category = Column(Unicode(128))
    method = Column(Unicode(128))
    # ori = Column(Float)
    # sf = Column(Float)
    # tf = Column(Float)
    # tid = Column(Integer)

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
            self.etype = unicode(type(e))
            self.etext = unicode(e)
        else:
            self.etype = None
            self.etext = None
        return self
