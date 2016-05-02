import cv2
import numpy as np
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class ROI(SQLite3Base):
    session_id = Column(Integer, ForeignKey('session.id'))
    # session = relationship('Session')
    polygon = Column(PickleType, default=[])
    centroid = Column(PickleType, default={})
    active = Column(Boolean, default=False)
    traces = relationship('Trace', order_by='Trace.id', lazy='joined')
    @property
    def contours(self):
        return np.array([[p['x'], p['y']] for p in self.polygon])
    def get_trace(self, frames):
        mask = np.zeros(frames.shape[1:], dtype='uint8')
        cv2.drawContours(mask, [self.contours], 0, 255, -1)
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames)
