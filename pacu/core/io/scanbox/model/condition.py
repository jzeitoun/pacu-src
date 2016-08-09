import cv2
import numpy as np
from sqlalchemy import Column, Integer, UnicodeText, Float
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class Condition(SQLite3Base):
    __tablename__ = 'conditions'
    pixel_x = Column(Integer)
    pixel_y = Column(Integer)
    dist = Column(Float)
    width = Column(Float)
    height = Column(Float)
    gamma = Column(Float)
    on_duration = Column(Float)
    off_duration = Column(Float)
    orientations = Column(PickleType, default=[])
    sfrequencies = Column(PickleType, default=[])
    tfrequencies = Column(PickleType, default=[])
    repetition = Column(Integer)
    projection = Column(UnicodeText)
    keyword = Column(UnicodeText)
    on_time = Column(PickleType, default=[])
    off_time = Column(PickleType, default=[])
    sequence = Column(PickleType, default=[])
    ran = Column(PickleType, default=[])
    order = Column(PickleType, default=[])
    trial_list = Column(PickleType, default=[])
    @classmethod
    def payload_from_expv1(cls, entity):
        """
        Read from pacu.core.model.experiment.ExperimentV1
        """
        init = {}
        init['on_time'] = entity.on_time.tolist()
        init['off_time'] = entity.off_time.tolist()
        init['sequence'] = entity.sequence.astype(int).tolist()
        init['ran'] = entity.ran.astype(int).tolist()
        init['order'] = entity.order.astype(int).tolist()
        init['trial_list'] = entity.trial_list.tolist()
        payload = entity.payload
        init.update(keyword = payload.get('handler').get('kwargs').get('exp_note'))
        init.update(projection = payload.get('projection').get('clsname'))
        init.update(**payload.get('monitor').get('kwargs'))
        init.update(**payload.get('stimulus').get('kwargs'))
        init.pop('name', None)
        init.pop('unit', None)
        return init
