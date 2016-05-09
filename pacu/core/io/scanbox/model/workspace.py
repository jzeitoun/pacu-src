from sqlalchemy import Column, UnicodeText

from pacu.core.io.scanbox.model.base import SQLite3Base

class Workspace(SQLite3Base):
    __tablename__ = 'workspaces'
    name = Column(UnicodeText)
