from sqlalchemy import Column, UnicodeText
from sqlalchemy.orm import relationship

from pacu.core.io.scanbox.model.base import SQLite3Base

class Session(SQLite3Base):
    name = Column(UnicodeText)
    rois = relationship('ROI', order_by='ROI.id', lazy='joined')
