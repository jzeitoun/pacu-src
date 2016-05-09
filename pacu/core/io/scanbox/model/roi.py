import cv2
import numpy as np
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class ROI(SQLite3Base):
    __tablename__ = 'rois'
    polygon = Column(PickleType, default=[])
    centroid = Column(PickleType, default={'x': -1, 'y': -1})
    active = Column(Boolean, default=False)
    @property
    def contours(self):
        return np.array([[p['x'], p['y']] for p in self.polygon])
    def get_trace(self, frames):
        mask = np.zeros(frames.shape[1:], dtype='uint8')
        cv2.drawContours(mask, [self.contours], 0, 255, -1)
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames)
