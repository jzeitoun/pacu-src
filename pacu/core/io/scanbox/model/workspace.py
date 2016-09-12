import operator

from sqlalchemy import Column, UnicodeText, Float, Integer

from pacu.core.io.scanbox.model.base import SQLite3Base

class Workspace(SQLite3Base):
    __tablename__ = 'workspaces'
    name = Column(UnicodeText, unique=True)
    cur_sfreq = Column(Float)
    cur_chan = Column(Integer, default=0)
    baseline_duration = Column(Float, default=0.5)
    def other_rois(self, roi):
        rois = list(self.rois)
        rois.remove(roi)
        return rois
