import numpy as np
import psutil

import ujson as json
from pacu.util.inspect import repr
from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, jet, gray
from pacu.core.io.util.colormap.distorted2 import DistortedColormap2

class ScanboxChannelMeta(object):
    __repr__ = repr.auto_strict
    def __init__(self, dtype, z, y, x):
        self.dtype = dtype
        self.z = z
        self.y = y
        self.x = x
    def save(self, path):
        with open(path, 'w') as f:
            f.write(json.dumps(self.__dict__))
    @classmethod
    def load(cls, path):
        with open(path) as f:
            payload = json.loads(f.read())
        return cls(**payload)

class ScanboxChannel(object):
    n_focal_pane = 1 # 1 single pane
    c_focal_pane = 0 # 0 first
    def __init__(self, path, n_focal_pane=1, c_focal_pane=0):
        self.n_focal_pane = n_focal_pane
        self.c_focal_pane = c_focal_pane
        self.path = Path(path).ensure_suffix('.chan')
        self.channel = int(self.path.stem)
        self.maxppath = self.path.join_suffixes('.maxp.npy')
        self.mmappath = self.path.join_suffixes('.mmap.npy')
        self.statpath = self.path.join_suffixes('.stat.npy')
        self.metapath = self.path.join_suffixes('.meta.json')
    def import_with_io(self, io):
        print 'Import channel {}.'.format(self.channel)
        if io.mat.scanmode == 0:
            print 'Bi-directional recording.'
        else:
            print 'Uni-directional recording.'
        return self._import_with_io3(io)
    def _import_with_io3(self, io):
        height, width = io.mat.sz
        shape = io.mat.get_shape(io.sbx.path.size)
        raw = np.memmap(io.sbx.path.str, dtype='uint16', mode='r', shape=shape)
        chan = raw[self.channel::io.mat.nchannels]
        depth = len(chan)
        max = np.zeros(depth, dtype='uint16')
        min = np.zeros(depth, dtype='uint16')
        mean = np.zeros(depth, dtype='float64')
        print 'Iterating over {} frames...'.format(depth)
        with open(self.mmappath.str, 'w') as npy:
            for i, frame in enumerate(chan):
                if (i % 100) == 0:
                    used_pct = psutil.virtual_memory().percent
                    if used_pct > 90:
                        raise MemoryError('Too much memory used.')
                    print ('Processing frames at ({}/{}). '
                            'Memory usage {}%').format(i, depth, used_pct)
                f = ~frame
                f[f == 65535] = 0
                npy.write(f.tostring())
                max[i] = f.max()
                min[i] = f.min()
                mean[i] = f.mean()
        meta = ScanboxChannelMeta(raw.dtype.name, depth, int(height), int(width))
        stat = np.rec.fromarrays([max, min, mean], names='MAX, MIN, MEAN')
        meta.save(self.metapath.str)
        np.save(self.statpath.str, stat)
        print 'Converting done!'
        return self
    def request_frame(self, index):
        return self.cmap8bit.to_rgba(self.mmap8bit[index], bytes=True).tostring()
    @memoized_property
    def mmap8bit(self):
        return self._mmap.view('uint8'
            )[self.c_focal_pane::self.n_focal_pane, :, 1::2]
    @memoized_property
    def cmap8bit(self):
        return ScalarMappable(norm=self.norm, cmap=self.dcmap.distorted)
    @memoized_property
    def norm(self):
        return Normalize(
            vmin=self.stat.MIN.min()/256, vmax=self.stat.MAX.max()/256)
    @memoized_property
    def dcmap(self):
        return DistortedColormap2('jet', xmid1=0.35, ymid1=0.65)
    @cmap8bit.invalidator
    def update_colormap(self, name, xmid1, ymid1, xmid2, ymid2):
        x1 = float(xmid1) / 100
        y1 = float(ymid1) / 100
        x2 = float(xmid2) / 100
        y2 = float(ymid2) / 100
        self.dcmap = DistortedColormap2(name,
            xmid1=x1, ymid1=y1, xmid2=x2, ymid2=y2)
    def request_maxp(self):
        return gray(
            self.maxp.view('uint8')[..., 1::2], bytes=True).tostring()
    @property
    def has_maxp(self):
        return self.maxppath.is_file()
    @memoized_property
    def maxp(self):
        return np.load(self.maxppath.str) if self.maxppath.is_file() else None
#     @maxp.invalidator
#     def create_maxp(self):
#         print 'Create max projection image...could take up from a few minutes to hours.'
#         frame = self.mmap.max(0)
#         np.save(self.maxppath.str, frame)
#         print 'done!'
    @maxp.invalidator
    def create_maxp(self):
        print 'Create max projection image...could take up from a few minutes to hours.'
        chan = self.mmap
        depth = len(chan)
        image = np.zeros_like(chan[0])
        for i, frame in enumerate(chan):
            if (i % 500) == 0:
                used_pct = psutil.virtual_memory().percent
                if used_pct > 90:
                    raise MemoryError('Too much memory used.')
                print ('Processing frames at ({}/{}). '
                        'Memory usage {}%').format(i, depth, used_pct)
            image = np.maximum(image, frame)
        np.save(self.maxppath.str, image)
        print 'done!'
    @memoized_property
    def stat(self):
        stat = np.load(self.statpath.str)
        return np.rec.fromrecords(stat, dtype=stat.dtype)
    @memoized_property
    def meta(self):
        return ScanboxChannelMeta.load(self.metapath.str)
    @memoized_property
    def _mmap(self):
        shape = (self.meta.z, self.meta.y, self.meta.x)
        return np.memmap(self.mmappath.str,
            mode='r', dtype=self.meta.dtype, shape=shape
        )
    @memoized_property
    def mmap(self):
        return self._mmap[self.c_focal_pane::self.n_focal_pane, ...]
    @property
    def dimension(self):
        z, y, x = self.mmap.shape
        return dict(depth=z, height=y, width=x)
    @property
    def shape(self):
        return (self.meta.z/self.n_focal_pane, self.meta.y, self.meta.x)
