from sqlalchemy import Column, Unicode
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class Trace(SQLite3Base):
    array = Column(PickleType, default=[])
    category = Column(Unicode(64))
