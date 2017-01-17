import cPickle
import operator

from sqlalchemy import Column, UnicodeText, Float, Integer, Binary
from sqlalchemy.types import PickleType

from pacu.ext.sqlalchemy.types.mutable import MutableDict
from pacu.core.io.scanbox.model.base import SQLite3Base

SOG_INITIAL_GUESS = dict(
    a1min=0  , a1max=1,
    a2min=0  , a2max=1,
    sigmin=15, sigmax=60,
    offmin=0 , offmax=0.01
)

class Workspace(SQLite3Base):
    SOG_INITIAL_GUESS=SOG_INITIAL_GUESS
    __tablename__ = 'workspaces'
    name = Column(UnicodeText, unique=True)
    cur_sfreq = Column(Float)
    cur_contrast = Column(Float)
    cur_chan = Column(Integer, default=0)
    baseline_duration = Column(Float, default=0.5)
    sog_initial_guess = Column(PickleType, default=lambda: SOG_INITIAL_GUESS)
    def other_rois(self, roi):
        rois = list(self.rois)
        rois.remove(roi)
        return rois
