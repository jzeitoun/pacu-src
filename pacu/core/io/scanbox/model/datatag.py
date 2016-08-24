from sqlalchemy import Column, Unicode, Float, Boolean
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class Datatag(SQLite3Base):
    __tablename__ = 'datatags'
    # anything
    value = Column(PickleType, default=None)
    # search criteria
    category = Column(Unicode(128))
    method = Column(Unicode(128))
    ori = Column(Float)
    sf = Column(Float)
    tf = Column(Float)
    def invalidate(self):
        self.value = None
#     def refresh(self):
#         self.value = self.roi.compute(self.category)
