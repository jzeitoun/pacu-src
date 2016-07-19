from __future__ import division

from collections import namedtuple

import numpy as np
from scipy import io

from pacu.core.io.view.zero_dimension_array import ZeroDimensionArrayView
from pacu.util.path import Path

Dimension = namedtuple('Dimension', 'height, width')

class ScanboxMatView(ZeroDimensionArrayView):
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.mat')
        array = io.loadmat(self.path.str, squeeze_me=True).get('info')
        super(ScanboxMatView, self).__init__(array)
    channels = 1 # hardcoding!
    @property
    def sbxsize(self):
        return self.path.with_suffix('.sbx').size
    @property
    def shape(self):
        return tuple(reversed((self.nframes, self.channels) + self.dimension))
    @property
    def dimension(self):
        return Dimension(*self.sz)
    @property
    def nframes(self):
        return int(self.sbxsize/self.recordsPerBuffer/
                self.dimension.width/2/self.channels)
    @property
    def framerate(self):
        return self.resfreq / self.recordsPerBuffer
#     @property
#     def recordsPerBuffer(self):
#         rpb = self._namedtuple.recordsPerBuffer
#         return rpb * 2 if self.scanmode is 0 else rpb
#     def __dir__(self): # quick and dirty: need to use descriptor set
#         return super(ScanboxInfoView, self).__dir__() + \
#             'path nchan factor framerate recordsPerBuffer sz'.split()
    def toDict(self):
        return self.items()
    @property
    def duration(self):
        return self.nframes / self.framerate
        # return '{s.nframes} frames at {s.framerate} fps is 00:01:14:01'.format(s=self)
        #  duration = frame_count / frame_rate

# for scanmode
# uni-direction is 1
# bi-direction is 0
u0 = ScanboxMatView('/Volumes/Users/ht/Desktop/sbx/uni-Day0_000_007.mat')
b0 = ScanboxMatView('/Volumes/Users/ht/Desktop/sbx/bi-Day7_010_007.mat')
b1 = ScanboxMatView('/Volumes/Users/ht/Desktop/sbx/bi-day1_100_003.mat')

