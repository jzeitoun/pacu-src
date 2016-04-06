import time
from operator import itemgetter

from scipy import stats
import cv2
import numpy as np

from pacu.util.inspect import repr
from pacu.core.io.scanimage.fit.gasussian.sumof import SumOfGaussianFit
from pacu.core.io.scanimage.fit.gasussian.sfreqdog import SpatialFrequencyDogFit
from pacu.core.io.scanimage import util

class ROI(object):
    """
    Bulk insert may introduce same-time-id instance. We need some salt.
    """
    polygon = ()
    neuropil = ()
    blank = None
    flicker = None
    responses = None
    best_sf_responses = None
    best_o_pref = None
    guess_params = None
    __repr__ = repr.auto_strict
    def __init__(self, id=None, **kwargs):
        self.id = id or '{:6f}'.format(time.time())
        self.__dict__.update(kwargs)
        if self.responses is None:
            self.responses = {}
        if self.guess_params is None:
            self.guess_params = {}
    def toDict(self):
        return dict(vars(self),
            sfreqfit = self.sfreqfit,
            best_o_pref = self.best_o_pref,
            best_sf_responses = self.best_sf_responses,
            anova_all = self.anova_all)
    def mask(self, shape):
        mask = np.zeros(shape, dtype='uint8')
        cv2.drawContours(mask, [self.inner_contours], 0, 255, -1)
        return mask
    def neuropil_mask(self, shape, others):
        mask = np.zeros(shape, dtype='uint8')
        cv2.drawContours(mask, [self.outer_contours], 0, 255, -1)
        cv2.drawContours(mask, [self.inner_contours], 0, 0, -1)
        for other in others:
            cv2.drawContours(mask, [other.inner_contours], 0, 0, -1)
        return mask
    @property
    def outer_contours(self):
        return np.array(list(map(itemgetter('x', 'y'), self.neuropil)))
    @property
    def inner_contours(self):
        return np.array(list(map(itemgetter('x', 'y'), self.polygon)))
    def trace(self, frames): # as in numpy array TODO: REFAC
        mask = self.mask(frames.shape[1:])
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames), mask
    def neuropil_trace(self, frames, others):
        mask = self.neuropil_mask(frames.shape[1:], others)
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames), mask
    def trim_bounding_mask(self, outer, inner):
        bounding = np.argwhere(outer)
        if len(bounding):
            ystart, xstart = bounding.min(0) - 1
            ystop, xstop = bounding.max(0) + 2
            return outer[ystart:ystop, xstart:xstop], inner[ystart:ystop, xstart:xstop]
    @property
    def anova_all(self):
        blank = self.blank.meantrace if self.blank else []
        flicker = self.flicker.meantrace if self.flicker else []
        all_oris = [
            # ori.meantrace
            [ont.array.mean() for ont in ori.ontimes]
            for resp in self.responses.values()
            for ori in resp.orientations.responses]
        print 'number of alll oris', len(all_oris)
        # print 'number of alll oris', len(all_oris)
        f, p = stats.f_oneway(blank, flicker, *all_oris)
        return util.nan_for_json(dict(f=f, p=p))
    def updates_by_io(self, io):
        return io.update_responses(self.id)
    def trace_by_io(self, io):
        return io.make_trace(self)
    @property
    def sfreqfit(self): # this is new.
        if not self.responses:
            return
        try:
            rmax = list(sorted(
                (sfreq, resp.stats['r_max'])
                for sfreq, resp in self.responses.items()))
            # rmax = self.best_sf_responses
            flicker = self.flicker.mean if self.flicker else None
            blank = self.blank.mean if self.flicker else None
            return SpatialFrequencyDogFit(rmax, flicker, blank)
        except:
            return {}
    @property
    def sorted_responses(self):
        responses = self.responses or {}
        return sorted((sf, resp) for sf, resp in responses.items())
    def meanresponse_over_sf(self, adaptor):
        cfreq = adaptor.capture_frequency
        return np.array([
            resp.orientations.ons[...,
            int(1*cfreq):int(2*cfreq)
        ].mean(axis=(1, 2)) for sf, resp in self.sorted_responses]).mean(axis=0)
    def update_with_adaptor(self, adaptor):
        gaussian = SumOfGaussianFit(
            adaptor.orientations,
            self.meanresponse_over_sf(adaptor)
        )
        self.best_o_pref = gaussian.o_pref
