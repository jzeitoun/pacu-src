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
    clsname = Column(Unicode(256))
    pkgname = Column(Unicode(256))
    keyword = Column(Unicode(256))
    message = Column(UnicodeText)
    on_time = Column(PickleType, default={})
    off_time = Column(PickleType, default={})
    sequence = Column(PickleType, default={})
    ran = Column(PickleType, default={})
    order = Column(PickleType, default={})
    payload = Column(PickleType, default={})
    trial_list = Column(PickleType, default={})
    def __iter__(self):
        return iter(self.ordered_trials)
    @property
    def ordered_trials(self):
        trials = self.trial_list[self.sequence].T.flatten()
        on_time, off_time , sequence, ran, order = [
            np.concatenate([
                data[indice]
                for data, indice
                in zip(getattr(self, attr).T, self.sequence.T)
            ]) for attr in 'on_time off_time sequence ran order'.split()]
        return [
            dict(on_time=float(on_time), off_time=float(off_time),
                sequence=int(sequence), ran=int(ran), order=int(order), **condition)
            for on_time, off_time, sequence, ran, order, condition
            in zip(on_time, off_time, sequence, ran, order, trials)
        ]
