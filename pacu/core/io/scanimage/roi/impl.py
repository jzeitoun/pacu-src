import time
import pandas as pd
from operator import itemgetter

from scipy import stats
import cv2
import numpy as np

from pacu.util.inspect import repr
from pacu.core.io.scanimage.fit.gasussian.sumof import SumOfGaussianFit
from pacu.core.io.scanimage.fit.gasussian.sfreqdog import SpatialFrequencyDogFit
from pacu.core.io.scanimage import util

def make_centroid(polygon):
    closed = np.array(list(polygon) + [polygon[0]])
    pointXs = closed[:, 0]
    pointYs = closed[:, 1]
    areadiff = (pointXs[:-1] * pointYs[1:]) - (pointYs[:-1] * pointXs[1:])
    area = np.sum(areadiff) / 2.
    cx = pointXs[:-1] + pointXs[1:]
    cy = pointYs[:-1] + pointYs[1:]
    center_x = np.sum(cx * (areadiff)) / (6. * area)
    center_y = np.sum(cy * (areadiff)) / (6. * area)
    return dict(x=int(center_x), y=int(center_y))

class ROI(object):
    """
    Bulk insert may introduce same-time-id instance. We need some salt.
    """
    vectors = ()
    polygon = ()
    neuropil = ()
    blank = None
    flicker = None
    responses = None
    best_sf_responses = None
    best_o_pref = None
    guess_params = None
    centroid = None
    __repr__ = repr.auto_strict
    def __init__(self, id=None, **kwargs):
        self.id = id or '{:6f}'.format(time.time())
        self.__dict__.update(kwargs)
        if self.responses is None:
            self.responses = {}
        if self.guess_params is None:
            self.guess_params = {}
    def toDict(self):
        v = vars(self)
        v.pop('centroid', None)
        return dict(v, 
            sfreqfit = self.sfreqfit,
            best_o_pref = self.best_o_pref,
            best_sf_responses = self.best_sf_responses,
            anova_all = self.anova_all)
    def mask(self, shape, dx=0, dy=0):
        mask = np.zeros(shape, dtype='uint8')
        cv2.drawContours(mask, [self.inner_contours(dx=dx, dy=dy)], 0, 255, -1)
        return mask
    def neuropil_mask(self, shape, others, dx=0, dy=0):
        mask = np.zeros(shape, dtype='uint8')
        cv2.drawContours(mask, [self.outer_contours(dx=dx, dy=dy)], 0, 255, -1)
        cv2.drawContours(mask, [self.inner_contours(dx=dx, dy=dy)], 0, 0, -1)
        for other in others:
            cv2.drawContours(mask, [other.inner_contours(dx=dx, dy=dy)], 0, 0, -1)
        return mask
    def outer_contours(self, dx=0, dy=0):
        if self.neuropil:
            return np.array(list(map(itemgetter('x', 'y'), self.neuropil))
                    ) + np.array([[dx, dy]])
        else:
            return np.array([])
    def inner_contours(self, dx=0, dy=0):
        return np.array(list(map(itemgetter('x', 'y'), self.polygon))
                ) + np.array([[dx, dy]])
    def trace(self, frames, dx=0, dy=0): # as in numpy array TODO: REFAC
        mask = self.mask(frames.shape[1:], dx, dy)
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames), mask
    def neuropil_trace(self, frames, others, dx=0, dy=0):
        mask = self.neuropil_mask(frames.shape[1:], others, dx, dy)
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
            for sf, resp in self.sorted_responses
            for ori in resp.orientations.responses]
        # print 'number of alll oris', len(all_oris)
        if self.flicker and self.blank:
            f_reps = [ont.array.mean() for ont in self.flicker.ontimes]
            b_reps = [ont.array.mean() for ont in self.blank.ontimes]
            matrix = np.array([b_reps, f_reps] + all_oris).T
            f, p = stats.f_oneway(f_reps, b_reps, *all_oris)
            return util.nan_for_json(dict(f=f, p=p, matrix=matrix))
        else:
            matrix = [[]]
            return util.nan_for_json(dict(matrix=matrix))
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
        sresps = sorted((sf, resp) for sf, resp in responses.items())
        return sresps
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
    @property
    def all_vectors(self):
        cnt = self.centroid or make_centroid(self.inner_contours())
        return [dict(cnt, index=0)] + list(self.vectors)
    def split_by_vectors(self, length):
        df = pd.DataFrame(self.all_vectors).set_index('index'
                ).reindex(range(length)).interpolate().astype(int).drop_duplicates()
        return df - df.ix[0]
