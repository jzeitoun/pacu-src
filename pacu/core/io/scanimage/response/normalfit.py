from collections import namedtuple

import numpy as np

from pacu.core.io.scanimage.fit.gasussian import sumof as sum_of_gaussians
from pacu.core.io.scanimage.fit.gasussian.sumof import SumOfGaussianFit

Fit = namedtuple('Fit', 'x y')

class NormalfitResponse(object):
    gaussian = None
    def __init__(self, array):
        self.array = array
    def toDict(self):
        return dict(
            measure = self.measure,
            stretched = self.measure_stretch,
            names = self.names,
            fit = self.fit._asdict(),
        )
    @classmethod
    def from_adaptor(cls, response, adaptor, best_o_pref):
        print 'make normalfit respo', best_o_pref
        print 'using initial guess', response.sog_initial_guess
        self = cls(response.trace)
        self.names = response.orientations.names
        # self.measure = response.orientations.ons[ # aka meanresponses
        #     ...,
        #     int(1*adaptor.capture_frequency):int(2*adaptor.capture_frequency)
        # ].mean(axis=(1, 2))
        self.measure = response.orientations.windowed_ontimes.mean(1)

        self.meanresponses_p   ,\
        self.residual          ,\
        self.meanresponses_fit ,\
        self.o_peaks           ,\
        self.measure_stretch   = sum_of_gaussians.fit(self.names, self.measure)
        # self.fit = Fit(*self.meanresponses_fit)
        self.gaussian = SumOfGaussianFit(self.names, self.measure,
            best_o_pref, response.sog_initial_guess)
        self.fit = Fit(self.gaussian.stretched.x, self.gaussian.y_fit)
        return self
    @property
    def max_orientation_index(self):
        return np.argmax(self.measure)

