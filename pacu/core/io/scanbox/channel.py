import numpy as np

import ujson as json
from pacu.util.inspect import repr
from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
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
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.chan')
        self.channel = int(self.path.stem)
        self.mmappath = self.path.join_suffixes('.mmap.npy')
        self.statpath = self.path.join_suffixes('.stat.npy')
        self.metapath = self.path.join_suffixes('.meta.json')
    def import_with_io(self, io):
        print 'Import channel {}.'.format(self.channel)
        if io.mat.scanmode == 0:
            print 'Bi-directional recording.'
            return self._import_with_io3(io)
        else:
            print 'Uni-directional recording.'
        raw = np.memmap(io.sbx.path.str, shape=io.mat.shape,
            dtype='uint16', mode='r', order='F'
        ).transpose(3, 1, 0, 2)[..., self.channel]
        print 'Extracting metadata'
        meta = ScanboxChannelMeta(raw.dtype.name, *raw.shape)
        print 'Convert raw data'
        mmap = np.memmap(self.mmappath.str,
            mode='w+', dtype=raw.dtype, shape=raw.shape)
        print 'Write to disk...'
        mmap[:] = ~raw
        print 'Calculating basic statistics'
        max = mmap.max(axis=(1,2))
        min = mmap.min(axis=(1,2))
        mean = mmap.mean(axis=(1,2))
        stat = np.rec.fromarrays([max, min, mean], names='MAX, MIN, MEAN')
        meta.save(self.metapath.str)
        np.save(self.statpath.str, stat)
        print 'Converting done!'
        return self
    def _import_with_io3(self, io):
        width = io.mat.sz[1]
        height = io.mat.sz[0] / 2
        raw = np.memmap(io.sbx.path.str, dtype='uint16', mode='r', order='F')
        chan = raw[self.channel::io.mat.nchannels].reshape(-1, height, width*2)
        depth = chan.shape[0] * 2
        max = np.zeros(depth, dtype='uint16')
        min = np.zeros(depth, dtype='uint16')
        mean = np.zeros(depth, dtype='float64')
        print 'Iterating over {} frames...'.format(chan.shape[0])
        print 'Aligning {} frames in total.'.format(depth)
        with open(self.mmappath.str, 'w') as npy:
            for i, frame in enumerate(chan):
                if (i % 100) == 0:
                    print 'Processing frames at #{} index...'.format(i)
                f = ~frame
                f[f == 65535] = 0
                left = f[:, :width]
                right = f[:, width:]
                npy.write(left.tostring())
                npy.write(right.tostring())
                first = i*2
                second = first + 1
                max[first] = left.max()
                max[second] = right.max()
                min[first] = left.min()
                min[second] = right.min()
                mean[first] = left.mean()
                mean[second] = right.mean()
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
        return self.mmap.view('uint8')[..., 1::2]
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
    @memoized_property
    def stat(self):
        stat = np.load(self.statpath.str)
        return np.rec.fromrecords(stat, dtype=stat.dtype)
    @memoized_property
    def meta(self):
        return ScanboxChannelMeta.load(self.metapath.str)
    @memoized_property
    def mmap(self):
        shape = (self.meta.z, self.meta.y, self.meta.x)
        return np.memmap(self.mmappath.str,
            mode='r', dtype=self.meta.dtype, shape=shape)
    @property
    def dimension(self):
        z, y, x = self.mmap.shape
        return dict(depth=z, height=y, width=x)
