import numpy as np
import ujson

from pacu.util.inspect import repr
from pacu.util.path import Path

class ScanboxChannelMeta(object):
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

class ScanboxChannel(object):
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.chan')
        self.channel = int(self.path.stem)
        self.mmappath = self.path.join_suffixes('.mmap.npy')
        self.statpath = self.path.join_suffixes('.stat.npy')
        self.metapath = self.path.join_suffixes('.meta.json')
    def import_with_io(self, io):
        print 'Import channel {}.'.format(self.channel)
        raw = np.memmap(io.sbxpath.str, shape=io.mat.shape,
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
