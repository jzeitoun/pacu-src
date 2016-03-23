import struct
from datetime import datetime
from collections import namedtuple

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.trajectory.log.impl import TrajectoryLog
from ipdb import set_trace

gene = '8s3I'
Meta = namedtuple('ScanimageMeta', 'dtype z y x')
TimeSpan = namedtuple('TimeSpan', 'sdt edt sts ets')
suffixes = '.mmap.npy', '.meta.bin', '.stat.npy', '.time.npy'

class TrajectoryTrial(object):
    def __init__(self, path):
        self.path = path
        self.datetime = datetime.fromtimestamp(float(path.name))
        mmappath, metapath, statpath, timepath = self.paths
        self.meta = Meta(*[
            (data.replace('\0', '') if hasattr(data, 'strip') else data)
            for data in struct.unpack(gene, metapath.read('rb'))
        ])
        shape = self.meta.z, self.meta.y, self.meta.x
        self.io = np.memmap(mmappath.str,
            dtype=self.meta.dtype, mode='r', shape=shape)
        stat = np.load(statpath.str)
        self.stat = np.rec.fromrecords(stat, dtype=stat.dtype)
        self.tss = np.load(timepath.str)
        self.tspan = TimeSpan(
            datetime.fromtimestamp(self.tss[0]),
            datetime.fromtimestamp(self.tss[-1]),
            self.tss[0], self.tss[-1]
        )
        self.set_cmap()
    @property
    def paths(self):
        return map(Path, [self.path.str + suf for suf in suffixes])
    @memoized_property
    def io8bit(self):
        return self.io.view('uint8')[..., 1::2]
    @memoized_property
    def log(self):
        l = TrajectoryLog.query(self.datetime)
        s, e = np.searchsorted(l.frame.E, [self.tspan.sts, self.tspan.ets], side='right')
        return l.frame[s:e]
    @memoized_property
    def log_aligned(self):
        if not self.log.size:
            return self.log
        return np.rec.array(
            map(tuple, signal.resample(self.log.tolist(), len(self.tss))),
            names=self.log.dtype.names)
    @memoized_property
    def log_aligned_json(self):
        return [
            dict(e=e, x=x, y=y, v=v) for e, x, y, v in self.log_aligned[['E', 'X', 'Y', 'V']]
        ]
    @property
    def dimension(self):
        return dict(width=self.meta.x, height=self.meta.y, depth=self.meta.z)
    def request_frame(self, index):
        return self.cmap.to_rgba(self.io8bit[index], bytes=True).tostring()
#     @memoized_property
#     def smap(self): # bad practice - change name
#         norm = Normalize(vmin=0, vmax=self.stat.MAX.max()/256)
#         return ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))
    def set_cmap(self, which=0):
        name = ['jet', 'gray', 'hot', 'hsv'][int(which)]
        norm = Normalize(vmin=0, vmax=self.stat.MAX.max()/256)
        self.cmap = ScalarMappable(norm=norm, cmap=plt.get_cmap(name))

# test = Path('/Volumes/Gandhi Lab - HT/Soyun/2016-02-04T14-27-00/1454624820.8')
# qwe = TrajectoryTrial(test)

