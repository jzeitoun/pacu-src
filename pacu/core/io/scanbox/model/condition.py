import cv2
import numpy as np
from sqlalchemy import Column, Integer, UnicodeText, Float
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class Condition(SQLite3Base):
    __tablename__ = 'conditions'
    info = Column(PickleType)
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
    @classmethod
    def from_expv1(cls, entity):
        """
        Read from pacu.core.model.experiment.ExperimentV1
        """
        init = {}
        init['trial_list'] = entity.trial_list.tolist()
        payload = entity.payload
        init.update(keyword = entity.keyword)
        init.update(projection = entity.projection_clsname)
        init.update(**entity.monitor_kwargs)
        init.update(**entity.stimulus_kwargs)
        # init.update(keyword = payload.get('handler').get('kwargs').get('exp_note'))
        # init.update(projection = payload.get('projection').get('clsname'))
        # init.update(**payload.get('monitor').get('kwargs'))
        # init.update(**payload.get('stimulus').get('kwargs'))
        # init.pop('name', None)
        # init.pop('unit', None)
        # init.pop('flicker', None)
        # init.pop('blank', None)
        return cls.init_and_update(**init)
    @property
    def io(self):
        from pacu.core.io.scanbox.impl2 import ScanboxIO
        return ScanboxIO(self.info.get('iopath'))
