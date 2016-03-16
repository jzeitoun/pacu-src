import time
from operator import itemgetter

import cv2
import numpy as np
from ipdb import set_trace

from pacu.util.inspect import repr

class ROI(object):
    """
    Bulk insert may introduce same-time-id instance. We need salt.
    """
    __repr__ = repr.auto_strict
    def __init__(self, polygon=None, id=None, **kwargs):
        self.polygon = polygon or []
        self.id = id or time.time()
    @property
    def hashed(self):
        return 'roi.{}'.format(self.id)
    def trace(self, frames): # as in numpy array TODO: REFAC
        contours = np.array(list(map(itemgetter('x', 'y'), self.polygon)))
        mask = np.zeros(frames.shape[1:], dtype='uint8')
        cv2.drawContours(mask, [contours], 0, 255, -1)
        return np.array([cv2.mean(frame, mask)[0] for frame in frames])

def test_get_roi():
    polygon = [
        {u'y': 80, u'x': 63},
        {u'y': 74, u'x': 71},
        {u'y': 75, u'x': 79},
        {u'y': 85, u'x': 77},
        {u'y': 86, u'x': 68}]
    return ROI(polygon=polygon)
def test():
    np.random.seed(1234)
    frames = np.random.randint(0, 256*256, (64, 128, 128))
    return test_get_roi(), frames
def test_trace():
    pass
    # np.random.seed(1234)
    # contours = np.array([[point['x'], point['y']] for point in polygon])
    # frames = np.random.randint(0, 256*256, (64, 128, 128))
    # mask = np.ma.zeros(frames.shape[1:], dtype='uint8')
    # cv2.drawContours(mask, [contours], 0, 255, -1)
    # trace = np.array([cv2.mean(frame, mask)[0] for frame in frames])
