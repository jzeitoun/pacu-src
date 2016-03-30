import time
from operator import itemgetter

import cv2
import numpy as np

from pacu.util.inspect import repr
from pacu.core.io.scanimage.fit.gasussian.sfreqdog import SpatialFrequencyDogFit

class ROI(object):
    """
    Bulk insert may introduce same-time-id instance. We need some salt.
    """
    polygon = ()
    neuropil = ()
    blank = None
    flicker = None
    responses = None
    __repr__ = repr.auto_strict
    def __init__(self, id=None, **kwargs):
        self.id = id or '{:6f}'.format(time.time())
        self.__dict__.update(kwargs)
        if self.responses is None:
            self.responses = {}
    def toDict(self):
        return dict(vars(self), sfreqfit=self.sfreqfit)
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
    def sfreqfit(self):
        if not self.responses:
            return
        rmax = list(sorted(
            (sfreq, resp.stats['r_max'])
            for sfreq, resp in self.responses.items()))
        flicker = self.flicker.mean if self.flicker else None
        blank = self.blank.mean if self.flicker else None
        return SpatialFrequencyDogFit(rmax, flicker, blank)
    def updates_by_io(self, io):
        return io.update_responses(self.id)
    def trace_by_io(self, io):
        return io.make_trace(self)
