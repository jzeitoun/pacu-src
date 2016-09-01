import operator

from sqlalchemy import Column, UnicodeText, Float

from pacu.core.io.scanbox.model.base import SQLite3Base

class Workspace(SQLite3Base):
    __tablename__ = 'workspaces'
    name = Column(UnicodeText)
    iopath = Column(UnicodeText) # should be relative because db.sqlite3 can move
                                 # around any locations.
    cur_sfreq = Column(Float)
    baseline_duration = Column(Float, default=0.5)
    @property
    def io(self): # experimental
        from pacu.core.io.scanbox.impl import ScanboxIO
        return ScanboxIO(self.iopath).set_channel(0)
