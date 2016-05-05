from sqlalchemy import Column, UnicodeText

from pacu.core.io.scanbox.model.base import SQLite3Base

class Workspace(SQLite3Base):
    name = Column(UnicodeText)
