from __future__ import division

import numpy as np

from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.fit import tau

class DecayResponse(object):
    tau = None
    x = ()
    y_fit = ()
    orientation = ()
    def __init__(self, orientation):
        self.orientation = orientation
    def toDict(self):
        return dict(
            traces = self.traces,
            mean = self.mean,
            name = self.orientation.value,
            tau = self.tau,
            x = self.x,
            y_fit = self.y_fit
        )
    @classmethod
    def from_adaptor(cls, response, adaptor):
        self = cls(response.trace)
        self.orientation = response.orientations.responses[
            response.normalfit.max_orientation_index]
        try:
            c_value, self.x, self.y_fit = tau.fit(self.mean)
            self.tau = 1.0 / (adaptor.capture_frequency * c_value)
        except Exception as e:
            raise Exception('Failed to get decay/tau fit: ' + str(e))
        return self
    @memoized_property
    def traces(self):
        return np.vstack([trace.array for trace in self.orientation.offtimes])
    @memoized_property
    def mean(self):
        return np.array(self.traces).mean(axis=0)
