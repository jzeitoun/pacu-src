from __future__ import division

import time
from collections import namedtuple

import numpy as np
from scipy import io

from pacu.core.io.view.zero_dimension_array import ZeroDimensionArrayView
from pacu.util.path import Path
from pacu.profile import manager

opt = manager.instance('opt')

Dimension = namedtuple('Dimension', 'height, width')

class ScanboxMatView(ZeroDimensionArrayView):
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.mat')
        array = io.loadmat(self.path.str, squeeze_me=True).get('info')
        super(ScanboxMatView, self).__init__(array)
    @property
    def sbxsize(self):
        return self.path.with_suffix('.sbx').size
    @property
    def sbxtime(self):
        return self.path.with_suffix('.sbx').created_at
    @property
    def sbxpath(self):
        return self.path.with_suffix('.sbx').relative_to(opt.scanbox_root)
    @property
    def iopath(self):
        return self.sbxpath.with_suffix('.io')
    @property
    def shape(self):
        return tuple(reversed((self.nframes, self.channels) + self.dimension))
    @property
    def dimension(self):
        return Dimension(*self.sz)
    @property
    def nframes(self):
        nframes = int(self.sbxsize/self.recordsPerBuffer/
                self.dimension.width/2/self.channels)
        return nframes * (1 if self.scanmode else 2)
    @property
    def framerate(self):
        rate = self.resfreq / self.recordsPerBuffer
        return rate if self.scanmode else rate * 2
    @property
    def nchannels(self):
        return 2 if self.channels == 1 else 1
    @property
    def factor(self):
        return 1 if self.channels == 1 else 2
    @property
    def scanmodestr(self):
        return 'uni' if self.scanmode == 1 else 'bi'
    def get_max_idx(self, size):
        return int(size/self.recordsPerBuffer/self.sz[1]*self.factor/4 - 1)
    def get_shape(self, size):
        return self.get_max_idx(size) + 1, self.recordsPerBuffer, self.sz[1]
    @property
    def recordsPerBuffer(self):
        rpb = self._dict.get('recordsPerBuffer')
        return rpb * 2 if self.scanmode is 0 else rpb
#     def __dir__(self): # quick and dirty: need to use descriptor set
#         return super(ScanboxInfoView, self).__dir__() + \
#             'path nchan factor framerate recordsPerBuffer sz'.split()

    def toDict(self):
        data = self.items()
        data['iopath'] = str(self.iopath)
        data['framerate'] = self.framerate
        data['frameratestr'] = str(self.framerate) + ' fps'
        data['sbxsize'] = self.sbxsize.str
        data['sbxtime'] = time.mktime(self.sbxtime.timetuple())
        data['sbxpath'] = self.sbxpath.str
        data['nchannels'] = self.nchannels
        data['nframes'] = self.nframes
        data['nframesstr'] = str(self.nframes) + ' frames'
        data['scanmodestr'] = self.scanmodestr
        return data
    @property
    def duration(self):
        return self.nframes / self.framerate
        # return '{s.nframes} frames at {s.framerate} fps is 00:01:14:01'.format(s=self)
        #  duration = frame_count / frame_rate

# u0 = ScanboxMatView('/Volumes/Users/ht/Desktop/sbx/Day0_000_007.mat')
