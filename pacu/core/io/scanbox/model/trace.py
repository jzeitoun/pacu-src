from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base


class Trace(SQLite3Base):
    roi_id = Column(Integer, ForeignKey('roi.id'))
    # roi = relationship('ROI')
    array = Column(PickleType, default=[])
    category = Column(Unicode(64))
