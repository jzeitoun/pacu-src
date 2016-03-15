from collections import namedtuple

import numpy as np

from pacu.core.io.scanimage.fit.gasussian import sumof as sum_of_gaussians

Fit = namedtuple('Fit', 'x y')

class NormalfitResponse(object):
    def __init__(self, array):
        self.array = array
    def toDict(self):
        return dict(
            measure = self.measure,
            stretched = self.stretched,
            names = self.names,
            fit = self.fit._asdict(),
        )
    @classmethod
    def from_adaptor(cls, response, adaptor):
        self = cls(response.trace)
        self.names = response.orientations.names
        self.measure = np.array(response.orientations.ons)[
            ...,
            int(1*adaptor.capture_frequency):int(2*adaptor.capture_frequency)
        ].mean(axis=(1, 2))
        meanresponses_p   ,\
        residual          ,\
        meanresponses_fit ,\
        o_peaks           ,\
        measure_stretch   = sum_of_gaussians.fit(self.names, self.measure)
        self.fit = Fit(*meanresponses_fit)
        self.stretched = measure_stretch
        return self
