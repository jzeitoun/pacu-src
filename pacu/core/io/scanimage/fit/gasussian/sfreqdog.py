from collections import namedtuple
from scipy import optimize
from scipy import interpolate
import numpy as np

from pacu.core.io.scanimage import util

Stretched = namedtuple('Stretched', 'x y')
DogParam = namedtuple('DogParam', 'amp1 sig1 amp2 sig2')
Point = namedtuple('Point', 'x y')

TWOPI = np.pi * 2

class SpatialFrequencyDogFit(object):
    ballpark_dog = [(1, 20), (1, 80), (1, 10), (1, 80)]
    visual_field = np.linspace(-50, 50, 200) # in degrees in visual angle
    _dog_param = None # for memoization
    def __init__(self, rmax, fff, blank=None):
        self.flicker = fff
        self.blank = blank
        xfreq, ymeas = zip(*([(0.0, fff)] + rmax))
        self.xfreq = np.array(xfreq)
        self.ymeas = np.array(ymeas)
        self.stretched = self.stretch()
        self.xstim = np.array(map(self.stimulus, self.stretched.x))
        # negative visual field squared
        self.nvfs = -np.square(self.visual_field)
    def stretch(self, n=100):
        func = interpolate.interp1d(self.xfreq, self.ymeas)
        stretched = np.linspace(self.lowest_freq, self.highest_freq, n)
        return Stretched(stretched, func(stretched))
    def stimulus(self, sfreq):
        return np.cos(self.visual_field*TWOPI*sfreq)
    @property
    def lowest_freq(self):
        return self.xfreq[0]
    @property
    def highest_freq(self):
        return self.xfreq[-1]
    def ballpark_residuals_dog(self, params):
        err = self.stretched.y - self.response_dog_bulk(params)
        return np.square(err).sum()
    def lsq_residuals_dog(self, params):
        err = self.stretched.y - self.response_dog_bulk(params)
        np.square(err, err) # in-place
        err[0] = err[0]*100 # this to force the fit to match FFF.
        return err # should not perform sum
    def response_dog_bulk(self, params):
        return (self.xstim * self.get_dog(*params)).sum(axis=1)
    def get_dog(self, amp1=10, sig1=10, amp2=5, sig2=30):
        gauss1 = amp1 * np.exp(self.nvfs/(TWOPI*sig1))
        gauss2 = amp2 * np.exp(self.nvfs/(TWOPI*sig2))
        return gauss1 - gauss2
    def fit_dog(self, initial_guess=None):
        print 'try to fit dog parameter...'
        params_brute, _, _, _ = optimize.brute(
            self.ballpark_residuals_dog,
            initial_guess or self.ballpark_dog,
            Ns = 5,
            full_output = True,
        )
        params_lsq, _, _, _, _ = optimize.leastsq(
            self.lsq_residuals_dog,
            params_brute,
            ftol = 0.001,
            maxfev = 5000,#DXFV changed to 5000 from 1000
            full_output = True,
        )
        return DogParam(*params_lsq)
    @property
    def dog_param(self):
        if not self._dog_param:
            self._dog_param = self.fit_dog()
        return self._dog_param
    @property
    def dog_xy(self):
        return self.stretched.x, self.response_dog_bulk(self.dog_param)
    @property
    def dog_x(self):
        return self.stretched.x
    @property
    def dog_y(self):
        return self.response_dog_bulk(self.dog_param)
    def dog_function(self, sf, offset=0):
        return (self.stimulus(sf) * self.get_dog(*self.dog_param)).sum() - offset
    @property
    def preferred_sfreq(self):
        x, y = self.dog_xy
        pindex = y.argmax()
        return Point(x[pindex], y[pindex])
    @property
    def peak_sfreq(self):
        pindex = self.ymeas.argmax()
        return Point(self.xfreq[pindex], self.ymeas[pindex])
    @property
    def y_for_bandwidth(self):
        return self.preferred_sfreq.y/2
    def solve_bandwidth(self):
        left, right = None, None
        x, y = self.dog_xy
        indice = np.abs(y - self.y_for_bandwidth).argsort()
        center_index = y.argmax()
        for index in indice:
            if index < center_index:
                left = index
                break
        for index in indice:
            if index > center_index:
                right = index
                break
        xleft = optimize.fsolve(self.dog_function, x[left], args=self.y_for_bandwidth, factor=0.1)[0]
        xright= optimize.fsolve(self.dog_function, x[right], args=self.y_for_bandwidth, factor=0.1)[0]
        return [
            (xleft, self.dog_function(xleft)),
            (xright, self.dog_function(xright))
        ]
    @property
    def bandwidth_ratio(self):
        try:
            left, right = self.solve_bandwidth()
            return np.sqrt(right[0] / left[0])
        except Exception as e:
            print 'exception in bandwidth_ratio:', type(e), str(e)
            return np.nan
    def toDict(self):
        return util.nan_for_json(dict(
            pref = self.preferred_sfreq.x,
            peak = self.peak_sfreq.x,
            ratio = self.bandwidth_ratio,
            dog_x = self.dog_x,
            dog_y = self.dog_y,
            blank = self.blank,
            flicker = self.flicker,
            sfx = self.xfreq,
            sfy = self.ymeas
        ))
# from matplotlib.pyplot import *
#     def plot_psf(self): # preferred spatial frequency
#         px, py = self.preferred_sfreq
#         plot(px, py, 'o', label='pref-sf')
#         legend()
#     def plot_Psf(self): # peak spatial frequency
#         px, py = self.peak_sfreq
#         plot(px, py, 'o', label='peak-sf')
#         legend()
#     def plot_dog(self):
#         x, y = self.dog_xy
#         plot(x, y, label='fit')
#         legend()
#     def plot(self):
#         plot(self.xfreq, self.ymeas, label='original')
#         legend()
#     def plot_all(self):
#         self.plot()
#         self.plot_dog()
#         self.plot_psf()
#         self.plot_Psf()
#         howmany = len(self.stretched.x)
#         plot(self.stretched.x, [self.preferred_sfreq.y]*howmany, linewidth=0.25, color='grey')
#         plot(self.stretched.x, [self.preferred_sfreq.y/2]*howmany, linewidth=0.25, color='grey')
#         band_left, band_right = self.solve_bandwidth()
#         plot(*band_left, marker='o', label='l')
#         plot(*band_right, marker='o',  label='r')
#         legend()
