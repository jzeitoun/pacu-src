import cv2
import numpy as np

from sqlalchemy import Column, Integer, UnicodeText, Float, Boolean
from sqlalchemy.orm import object_session
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class Condition(SQLite3Base):
    __tablename__ = 'conditions'
    info = Column(PickleType)
    exp_id = Column(Integer)
    imported = Column(Boolean, default=False)
    pixel_x = Column(Integer)
    pixel_y = Column(Integer)
    dist = Column(Float)
    width = Column(Float)
    height = Column(Float)
    gamma = Column(Float)
    on_duration = Column(Float)
    off_duration = Column(Float)
    repetition = Column(Integer)
    projection = Column(UnicodeText)
    keyword = Column(UnicodeText)
    trial_list = Column(PickleType, default=[])
    orientations = Column(PickleType, default=[])
    sfrequencies = Column(PickleType, default=[])
    tfrequencies = Column(PickleType, default=[])
    object_session = property(object_session)
    def from_expv1(self, entity):
        """
        Read from pacu.core.model.experiment.ExperimentV1
        """
        init = {}
        self.trial_list = entity.trial_list.tolist()
        payload = entity.payload
        self.keyword = entity.keyword
        self.projection = entity.projection_clsname
        for k, v in entity.monitor_kwargs.items():
            setattr(self, k, v)
        for k, v in entity.stimulus_kwargs.items():
            setattr(self, k, v)
    @property
    def io(self):
        from pacu.core.io.scanbox.impl2 import ScanboxIO
        # TODO: still has problem with relative paths
        return ScanboxIO(self.info.get('iopath'))
    def append_workspace(self, name):
        from pacu.core.io.scanbox.model import db as schema
        with self.object_session.begin():
            ws = schema.Workspace(name=name, condition=self)
            if self.sfrequencies:
                ws.cur_sfreq = self.sfrequencies[0]
