from __future__ import division

import ujson

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from ipdb import set_trace

from pacu.util.path import Path
from pacu.util.inspect import repr
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.legacy.cfaan import driftcorrect

class ScanimageChannelMeta(object):
    __repr__ = repr.auto_strict
    def __init__(self, dtype, z, y, x):
        self.dtype = dtype
        self.z = z
        self.y = y
        self.x = x
    def save(self, path):
        with open(path, 'w') as f:
            f.write(ujson.dumps(self.__dict__))
    @classmethod
    def load(cls, path):
        with open(path) as f:
            payload = ujson.loads(f.read())
        return cls(**payload)

class ScanimageChannel(object):
    cmap_name = 'jet'
    def __init__(self, path):
        self.path = Path(path)
    @property
    def mmappath(self):
        return self.path.with_suffix('.mmap.npy')
    @memoized_property
    def cmap8bit(self):
        norm = Normalize(
            vmin=self.stat.MIN.min()/256, vmax=self.stat.MAX.max()/256)
        return ScalarMappable(norm=norm, cmap=plt.get_cmap(self.cmap_name))
    @memoized_property
    def mmap(self):
        shape = (self.meta.z, self.meta.y, self.meta.x)
        return np.memmap(self.mmappath.str,
            mode='r', dtype=self.meta.dtype, shape=shape)
    @memoized_property
    def mmap8bit(self):
        return self.mmap.view('uint8')[..., 1::2]
    @property
    def metapath(self):
        return self.path.with_suffix('.meta.json')
    @memoized_property
    def meta(self):
        return ScanimageChannelMeta.load(self.metapath.str)
    @property
    def statpath(self):
        return self.path.with_suffix('.stat.npy')
    @memoized_property
    def stat(self):
        stat = np.load(self.statpath.str)
        return np.rec.fromrecords(stat, dtype=stat.dtype)
    def import_raw(self, tiff):
        print 'Drift correct...it may take a few minutes...'
        drift = driftcorrect.getdrift3(tiff)
        corr = driftcorrect.driftcorrect2(tiff, drift)
        print 'Extracting metadata...'
        meta = ScanimageChannelMeta(corr.dtype.name, *corr.shape)
        print 'Calculating basic statistics...'
        max = corr.max(axis=(1,2))
        min = corr.min(axis=(1,2))
        mean = corr.mean(axis=(1,2))
        stat = np.rec.fromarrays([max, min, mean], names='MAX, MIN, MEAN')
        mmap = np.memmap(self.mmappath.str,
            mode='w+', dtype=corr.dtype, shape=corr.shape)
        print 'Write to disk...'
        mmap[:] = corr[:]
        meta.save(self.metapath.str)
        np.save(self.statpath.str, stat)
        print 'Converting done!'
        return self
    def toDict(self):
        z, y, x = self.mmap.shape
        return dict(depth=z, height=y, width=x)
    def request_frame(self, index):
        return self.cmap8bit.to_rgba(self.mmap8bit[index], bytes=True).tostring()