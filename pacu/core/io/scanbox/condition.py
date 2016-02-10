import numpy as np
from ipdb import set_trace

class Payload(object):
    def __init__(self, payload):
        kwargs = payload.pop('kwargs')
        self.__dict__ = payload
        self.__dict__.update(kwargs)
FRAMERATE = 30
class ScanboxCondition(object):
    def __init__(
        self,
        id,
        ran,
        order,
        clsname,
        pkgname,
        on_time,
        sequence,
        created_at,
        off_time,
        message,
        payload,
        **kwargs
    ):
        self.id         = id
        self.ran        = ran
        self.order      = order
        self.clsname    = clsname
        self.pkgname    = pkgname
        self.on_time    = on_time
        self.sequence   = sequence.T.flatten()
        self.created_at = created_at
        self.off_time   = off_time
        self.message    = message
        self._payload   = payload
        self.__dict__.update({
            key: Payload(val) for key, val in payload.items()
        })
    def extract(self):
        attributes = {
            key: getattr(self, key) for key in 'spatial_frequencies'.split()
        }
        return dict(attributes=attributes)
    @property
    def temporal_frequencies(self):
        return [1]
    @property
    def spatial_frequencies(self):
        return self.stimulus.sfrequencies
    @property
    def orientations(self):
        return self.stimulus.orientations
    @property
    def nConditions(self):
        return len(self.orientations) * len(self.spatial_frequencies)
    @property
    def blankOn(self):
        return 0
    @property
    def flickerOn(self):
        return 0
    @property
    def waitinterval_F(self):
        return np.array(self.stimulus.off_duration) * FRAMERATE
    @property
    def condition_F(self):
        return self.waitinterval_F * 2
    @property
    def ontimes_F(self):
        return (np.array(self.on_time) * FRAMERATE).flatten()
    @property
    def duration_F(self):
        return np.array(self.stimulus.off_duration) * FRAMERATE
    @property
    def captureFrequency(self):
        return FRAMERATE
    def __getitem__(self, item):
        return getattr(self, item)
    @property
    def start_times(self):
        start_times = np.array(self.ontimes_F)-self.waitinterval_F
        return start_times.astype('int')







