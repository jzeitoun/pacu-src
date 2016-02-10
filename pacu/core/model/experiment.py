from datetime import datetime

import numpy as np
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy.types import PickleType
from sqlalchemy.types import UnicodeText

from . import Base

class ExperimentV1(Base):
    __tablename__ = 'experiment_v1'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clsname = Column(Unicode(265))
    pkgname = Column(Unicode(265))
    message = Column(UnicodeText)
    on_time = Column(PickleType, default={})
    sequence = Column(PickleType, default={})
    ran = Column(PickleType, default={})
    order = Column(PickleType, default={})
    off_time = Column(PickleType, default={})
    payload = Column(PickleType, default={})
    trial_list = Column(PickleType, default={})
    @property
    def as_ordered(self):
        trials = self.trial_list[self.sequence].T.flatten()
        on_time, off_time = [
            np.concatenate([
                data[indice]
                for data, indice
                in zip(getattr(self, attr).T, self.sequence.T)
            ]) for attr in 'on_time off_time'.split()]
        return [
            dict(on_time=on_time, off_time=off_time, **condition)
            for on_time, off_time, condition
            in zip(on_time, off_time, trials)
        ]
