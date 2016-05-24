import operator

from sqlalchemy import Column, UnicodeText

from pacu.core.io.scanbox.model.base import SQLite3Base

class Workspace(SQLite3Base):
    __tablename__ = 'workspaces'
    name = Column(UnicodeText)
    iopath = Column(UnicodeText) # should be relative because db.sqlite3 can move
                                 # around any locations.
    @property
    def io(self): # experimental
        from pacu.core.io.scanbox.impl import ScanboxIO
        return ScanboxIO(self.iopath).set_channel(0)
