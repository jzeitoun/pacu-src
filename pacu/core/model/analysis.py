from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy.types import PickleType

from . import Base

class AnalysisV1(Base):
    __tablename__ = 'analysis_v1'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(Unicode(256)) # for i3d
    title = Column(Unicode(256))
    user = Column(Unicode(256)) # relationship with users
    src = Column(Unicode(512)) # path
    host = Column(Unicode(512)) # path
    desc = Column(Unicode(1024)) # path
    index = Column(Integer) # path
    # relationsship with recordings/experiment
    # relationsship with ? rois?
    # relationsship with ? objects?
